"""Render pca_animation.html to a GIF using Playwright + imageio.

Drives the animation's clock from Python so frames are deterministic and
timing-perfect (no jitter from real-time rAF).

Usage:
    uv run render.py

Output:
    ../../../static/images/intuitive-understanding-of-pca/height_weight_pca.gif
"""

from __future__ import annotations

import io
from pathlib import Path

import imageio.v3 as iio
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
HTML_FILE = HERE / "pca_animation.html"
OUT_GIF = (
    HERE.parent.parent.parent
    / "static"
    / "images"
    / "intuitive-understanding-of-pca"
    / "height_weight_pca.gif"
)

# Must match the phase durations declared in pca_animation.html
PHASE_DURATIONS_MS = [1200, 1400, 1200, 1000, 1800, 2400, 1200]
TOTAL_MS = sum(PHASE_DURATIONS_MS)
FPS = 24
N_FRAMES = round(TOTAL_MS / 1000 * FPS)
VIEW_W, VIEW_H = 720, 540


def capture_frames() -> list[np.ndarray]:
    frames: list[np.ndarray] = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context(
            viewport={"width": VIEW_W, "height": VIEW_H},
            device_scale_factor=2,  # render at 2x for crispness, downscale later
        )
        page = context.new_page()
        page.goto(HTML_FILE.as_uri())
        page.wait_for_function("typeof window.renderAt === 'function'")

        # Hide the controls overlay so it doesn't appear in screenshots.
        page.add_style_tag(content=".controls { display: none !important; }")

        for i in range(N_FRAMES):
            t_ms = (i / FPS) * 1000
            # Setting __virtualTimeMs tells the rAF loop to freeze at this time,
            # so subsequent rAF callbacks don't overwrite our render. Calling
            # renderAt directly applies the state synchronously before screenshot.
            page.evaluate(
                """(t) => {
                    window.__virtualTimeMs = t;
                    window.renderAt(t);
                }""",
                t_ms,
            )
            png_bytes = page.locator(".stage").screenshot(type="png")
            img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
            if img.size != (VIEW_W, VIEW_H):
                img = img.resize((VIEW_W, VIEW_H), Image.LANCZOS)
            frames.append(np.array(img))

        browser.close()
    return frames


def write_gif(frames: list[np.ndarray]) -> None:
    OUT_GIF.parent.mkdir(parents=True, exist_ok=True)
    duration_ms = round(1000 / FPS)
    iio.imwrite(
        OUT_GIF,
        frames,
        loop=0,
        duration=duration_ms,
        plugin="pillow",
    )
    print(f"wrote {OUT_GIF} ({len(frames)} frames at {FPS}fps, ~{TOTAL_MS}ms loop)")


if __name__ == "__main__":
    frames = capture_frames()
    write_gif(frames)
