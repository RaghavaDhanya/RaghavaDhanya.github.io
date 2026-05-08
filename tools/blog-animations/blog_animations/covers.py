"""Static cover image rendering and optimisation.

`render_html_cover` captures a single frame from an HTML page (used for the
PCA post's rendered cover).

`optimize_cover_image` takes an existing image (PNG/JPG) and re-encodes it
to WebP at a target width. For palettable sources (≤256 unique colours) it
quantises back to the source's exact palette after resize, so libwebp's
lossless encoder applies its color-indexing transform — that produces files
significantly smaller than naive RGB lossless. For photos it falls back to
lossy WebP at a tunable quality.

Both write to `assets/images/<slug>/cover.webp` so PaperMod's cover.html
partial picks them up via `resources.ByType "image"` and emits a responsive
srcset of WebP variants.
"""

from __future__ import annotations

import io
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

from .render import _quantise_nn


@dataclass
class StaticRenderConfig:
    html: Path
    out: Path  # .webp
    viewport: tuple[int, int]  # design dimensions of the .stage
    target_width: int = 1500
    device_scale_factor: int = 2
    stage_selector: str = ".stage"
    lossless: bool = True
    quality: int = 90


def render_html_cover(cfg: StaticRenderConfig) -> Path:
    """Render an HTML page's stage element to a single still WebP."""
    cfg.out.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        ctx = b.new_context(
            viewport={"width": cfg.viewport[0], "height": cfg.viewport[1]},
            device_scale_factor=cfg.device_scale_factor,
        )
        page = ctx.new_page()
        page.goto(cfg.html.as_uri())
        page.wait_for_load_state("networkidle")
        png = page.locator(cfg.stage_selector).screenshot(type="png")
        b.close()

    img = Image.open(io.BytesIO(png)).convert("RGB")
    target_w = cfg.target_width
    target_h = round(target_w * cfg.viewport[1] / cfg.viewport[0])
    if img.size != (target_w, target_h):
        img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    img.save(
        cfg.out,
        format="WEBP",
        lossless=cfg.lossless,
        quality=cfg.quality,
        method=4,
    )
    size_kb = cfg.out.stat().st_size / 1024
    print(
        f"wrote {cfg.out.name} ({img.width}x{img.height}, {size_kb:.0f} KB, "
        f"lossless={cfg.lossless})"
    )
    return cfg.out


def optimize_cover_image(
    src: Path,
    out: Path,
    target_width: int = 1500,
    palette: bool | None = None,
    quality: int = 90,
) -> Path:
    """Re-encode a cover image to WebP at target_width.

    `palette=True` (or auto-detected when source has ≤256 unique colours)
    preserves the source palette across the resize via exact NN quantisation,
    so the saved lossless WebP gets libwebp's color-indexing transform.
    `palette=False` saves lossy WebP at `quality` (correct for photos).
    """
    out.parent.mkdir(parents=True, exist_ok=True)
    src_img = Image.open(src)
    rgb_full = src_img.convert("RGB")

    if palette is None:
        colors = rgb_full.getcolors(maxcolors=257)
        palette = colors is not None

    w, h = rgb_full.size
    if w > target_width:
        new_h = round(h * target_width / w)
        resized = rgb_full.resize((target_width, new_h), Image.Resampling.LANCZOS)
    else:
        resized = rgb_full

    if palette:
        colors = rgb_full.getcolors(maxcolors=257)
        if colors is None:
            raise ValueError(f"{src} has >256 unique colours; pass palette=False")
        pal_rgb = np.array([c[1] for c in colors], dtype=np.int16)
        out_img = _quantise_nn(resized, pal_rgb).convert("RGB")
        out_img.save(out, format="WEBP", lossless=True, method=4)
        kind = f"lossless palette ({len(colors)} colours)"
    else:
        resized.save(out, format="WEBP", lossless=False, quality=quality, method=4)
        kind = f"lossy q={quality}"

    size_kb = out.stat().st_size / 1024
    print(
        f"wrote {out.name} ({resized.width}x{resized.height}, {size_kb:.0f} KB, "
        f"{kind})"
    )
    return out
