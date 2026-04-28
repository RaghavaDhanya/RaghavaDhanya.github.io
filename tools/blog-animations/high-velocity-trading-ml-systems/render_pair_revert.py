"""Render pair_revert_animation.html to three GIFs (variants 1, 2, 3).

Variant is selected via URL fragment; the HTML page reads location.hash to
choose which path geometry to draw.

Usage:
    uv run python render_pair_revert.py
"""

from __future__ import annotations

import io
from pathlib import Path

import imageio.v3 as iio
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
HTML_FILE = HERE / "pair_revert_animation.html"
OUT_DIR = (
    HERE.parent.parent.parent
    / "static"
    / "images"
    / "high-velocity-trading-ml-systems"
)

PHASE_DURATIONS_MS = [300, 900, 1500, 700, 1700, 1700]
TOTAL_MS = sum(PHASE_DURATIONS_MS)
FPS = 24
N_FRAMES = round(TOTAL_MS / 1000 * FPS)
VIEW_W, VIEW_H = 720, 540

VARIANTS = ["1", "2", "3"]


def render_variant(pw, variant: str) -> list[np.ndarray]:
    browser = pw.chromium.launch()
    context = browser.new_context(
        viewport={"width": VIEW_W, "height": VIEW_H},
        device_scale_factor=2,
    )
    page = context.new_page()
    page.goto(HTML_FILE.as_uri() + f"#{variant}")
    page.wait_for_function("typeof window.renderAt === 'function'")
    page.add_style_tag(content=".controls { display: none !important; }")

    frames: list[np.ndarray] = []
    for i in range(N_FRAMES):
        t_ms = (i / FPS) * 1000
        page.evaluate(
            """(t) => { window.__virtualTimeMs = t; window.renderAt(t); }""",
            t_ms,
        )
        png_bytes = page.locator(".stage").screenshot(type="png")
        img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
        if img.size != (VIEW_W, VIEW_H):
            img = img.resize((VIEW_W, VIEW_H), Image.LANCZOS)
        frames.append(np.array(img))

    browser.close()
    return frames


def write_gif(frames: list[np.ndarray], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    duration_ms = round(1000 / FPS)
    iio.imwrite(out_path, frames, loop=0, duration=duration_ms, plugin="pillow")
    print(f"wrote {out_path} ({len(frames)} frames at {FPS}fps, ~{TOTAL_MS}ms loop)")


if __name__ == "__main__":
    with sync_playwright() as pw:
        for v in VARIANTS:
            frames = render_variant(pw, v)
            write_gif(frames, OUT_DIR / f"pair-revert-{v}.gif")
