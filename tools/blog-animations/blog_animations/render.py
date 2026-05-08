"""Reusable Playwright-driven animation renderer.

Captures frames from a self-contained HTML animation (which must expose
`window.renderAt(t_ms)` and `window.__palette`) and bakes them to animated
WebP and/or GIF.

`window.__palette` is the structured colour declaration the renderer reads
to build a fixed quantisation palette. Format:

    window.__palette = {
      bg: "#ffffff",
      fg: ["#1e1e1e", "#6c6c6c", "#d6d6d6"],
    };

Each `fg` entry gets a `ramp_steps`-step ramp blending toward `bg`, since
that is where antialiasing happens for stroked lines and small shapes on
a flat canvas.

Optimisations applied:
  * exact nearest-neighbour quantisation against the declared palette
    (the declared bg survives untouched, matching the browser's render),
  * consecutive-identical-frame deduplication,
  * lossless WebP encoding at the slowest/best method.
"""

from __future__ import annotations

import hashlib
import io
import subprocess
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image
from playwright.sync_api import Page, Playwright, sync_playwright

RGB = tuple[int, int, int]


@dataclass
class RenderConfig:
    html: Path
    out: Path
    phase_durations_ms: list[int]
    fps: int = 24
    viewport: tuple[int, int] = (720, 540)
    device_scale_factor: int = 2
    stage_selector: str = ".stage"
    hide_selectors: tuple[str, ...] = (".controls",)
    url_fragment: str = ""
    formats: tuple[str, ...] = ("webp",)
    # Per-anchor anti-alias ramp resolution. Set to 0 to ship the raw capture
    # without quantisation (lossless but larger).
    ramp_steps: int = 16
    dedupe: bool = True
    # libwebp encode method. 4 is fast (~0.5s/animation), 6 is slow (~90s) for
    # ~0.5% smaller output. Use 6 for final publish, 4 during iteration.
    webp_method: int = 4


def render(cfg: RenderConfig) -> dict[str, Path]:
    total_ms = sum(cfg.phase_durations_ms)
    n_frames = round(total_ms / 1000 * cfg.fps)
    frame_ms = round(1000 / cfg.fps)

    with sync_playwright() as pw:
        frames, palette = _capture(pw, cfg, n_frames)

    if cfg.ramp_steps > 0:
        pal_rgb = _build_palette(palette, cfg.ramp_steps)
        frames = [_quantise_nn(f, pal_rgb) for f in frames]
        n_entries = len(pal_rgb)
    else:
        n_entries = 0

    if cfg.dedupe:
        frames, durations = _dedupe(frames, frame_ms)
    else:
        durations = [frame_ms] * len(frames)

    outputs: dict[str, Path] = {}
    for fmt in cfg.formats:
        out = cfg.out.with_suffix(f".{fmt}")
        out.parent.mkdir(parents=True, exist_ok=True)
        if fmt == "webp":
            _write_webp(out, frames, durations, cfg.webp_method)
        elif fmt == "gif":
            _write_gif(out, frames, durations)
        else:
            raise ValueError(f"unsupported format: {fmt}")
        outputs[fmt] = out
        size_kb = out.stat().st_size / 1024
        palette_note = f", {n_entries}-colour palette" if n_entries else ""
        print(
            f"wrote {out.name} ({len(frames)} unique frames, "
            f"{total_ms}ms loop, {size_kb:.0f} KB{palette_note})"
        )
    return outputs


def _capture(
    pw: Playwright, cfg: RenderConfig, n_frames: int
) -> tuple[list[Image.Image], dict]:
    browser = pw.chromium.launch()
    context = browser.new_context(
        viewport={"width": cfg.viewport[0], "height": cfg.viewport[1]},
        device_scale_factor=cfg.device_scale_factor,
    )
    page = context.new_page()
    url = cfg.html.as_uri() + (f"#{cfg.url_fragment}" if cfg.url_fragment else "")
    page.goto(url)
    page.wait_for_function("typeof window.renderAt === 'function'")
    if cfg.hide_selectors:
        css = "".join(f"{s}{{display:none !important;}}" for s in cfg.hide_selectors)
        page.add_style_tag(content=css)

    palette = _read_palette(page, cfg.html)

    frames: list[Image.Image] = []
    for i in range(n_frames):
        t_ms = (i / cfg.fps) * 1000
        page.evaluate(
            "(t) => { window.__virtualTimeMs = t; window.renderAt(t); }",
            t_ms,
        )
        png_bytes = page.locator(cfg.stage_selector).screenshot(type="png")
        img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
        if img.size != cfg.viewport:
            img = img.resize(cfg.viewport, Image.Resampling.LANCZOS)
        frames.append(img)

    browser.close()
    return frames, palette


def _read_palette(page: Page, html: Path) -> dict:
    pal = page.evaluate("() => window.__palette || null")
    if pal is None:
        raise RuntimeError(
            f"{html.name} does not declare window.__palette. "
            "Add a structured palette block to the <script> section."
        )
    if "bg" not in pal or "fg" not in pal:
        raise RuntimeError(f"window.__palette in {html.name} must have bg and fg keys")
    return pal


def _hex_to_rgb(h: str) -> RGB:
    h = h.lstrip("#").lower()
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _build_palette(palette: dict, ramp_steps: int) -> np.ndarray:
    bg = _hex_to_rgb(palette["bg"])
    fgs = [_hex_to_rgb(c) for c in palette["fg"]]

    entries: list[RGB] = [bg]
    seen: set[RGB] = {bg}

    def add(c: RGB) -> None:
        if c not in seen and len(seen) < 256:
            entries.append(c)
            seen.add(c)

    for c in fgs:
        if c == bg:
            continue
        add(c)
        for i in range(1, ramp_steps):
            t = i / ramp_steps
            blend: RGB = (
                round(bg[0] * (1 - t) + c[0] * t),
                round(bg[1] * (1 - t) + c[1] * t),
                round(bg[2] * (1 - t) + c[2] * t),
            )
            add(blend)

    return np.array(entries, dtype=np.int16)


def _quantise_nn(img: Image.Image, palette_rgb: np.ndarray) -> Image.Image:
    """Exact nearest-neighbour quantisation. Returns a P-mode image whose
    palette index 0 is `palette_rgb[0]`, etc."""
    arr = np.asarray(img.convert("RGB"), dtype=np.int16)
    h, w, _ = arr.shape
    flat = arr.reshape(-1, 3)
    pal = palette_rgb
    pal_sq = (pal.astype(np.int32) ** 2).sum(axis=1)

    indices = np.empty(h * w, dtype=np.uint8)
    chunk = 100_000
    for start in range(0, h * w, chunk):
        end = min(start + chunk, h * w)
        block = flat[start:end].astype(np.int32)
        block_sq = (block ** 2).sum(axis=1, keepdims=True)
        dot = block @ pal.astype(np.int32).T
        dist = block_sq + pal_sq[None, :] - 2 * dot
        indices[start:end] = dist.argmin(axis=1).astype(np.uint8)

    out = Image.fromarray(indices.reshape(h, w), mode="P")
    pal_bytes = palette_rgb.astype(np.uint8).tobytes()
    pal_bytes += b"\x00" * (768 - len(pal_bytes))
    out.putpalette(pal_bytes)
    return out


def _frame_hash(img: Image.Image) -> bytes:
    return hashlib.blake2b(img.tobytes(), digest_size=16).digest()


def _dedupe(
    frames: list[Image.Image], frame_ms: int
) -> tuple[list[Image.Image], list[int]]:
    if not frames:
        return [], []
    out_frames = [frames[0]]
    out_durations = [frame_ms]
    last_hash = _frame_hash(frames[0])
    for img in frames[1:]:
        h = _frame_hash(img)
        if h == last_hash:
            out_durations[-1] += frame_ms
        else:
            out_frames.append(img)
            out_durations.append(frame_ms)
            last_hash = h
    return out_frames, out_durations


def _write_webp(
    out: Path, frames: list[Image.Image], durations: list[int], method: int
) -> None:
    rgb = [f.convert("RGB") if f.mode != "RGB" else f for f in frames]
    head, *tail = rgb
    head.save(
        out,
        format="WEBP",
        save_all=True,
        append_images=tail,
        duration=durations,
        loop=0,
        lossless=True,
        quality=100,
        method=method,
    )


def _write_gif(out: Path, frames: list[Image.Image], durations: list[int]) -> None:
    p_frames = [
        f if f.mode == "P" else f.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
        for f in frames
    ]
    head, *tail = p_frames
    head.save(
        out,
        format="GIF",
        save_all=True,
        append_images=tail,
        duration=durations,
        loop=0,
        disposal=2,
        optimize=True,
    )
    _maybe_gifsicle(out)


def _maybe_gifsicle(path: Path) -> None:
    try:
        subprocess.run(
            ["gifsicle", "-O3", "--lossy=30", "-o", str(path), str(path)],
            check=True,
            capture_output=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
