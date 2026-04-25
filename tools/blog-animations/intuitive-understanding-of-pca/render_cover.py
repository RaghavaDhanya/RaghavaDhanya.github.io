"""Render cover.html to a static PNG cover image for the PCA post.

Usage:
    uv run render_cover.py

Output:
    ../../../static/images/intuitive-understanding-of-pca/cover.png
"""

from __future__ import annotations

import io
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
HTML_FILE = HERE / "cover.html"
OUT_PNG = (
    HERE.parent.parent.parent
    / "static"
    / "images"
    / "intuitive-understanding-of-pca"
    / "cover.png"
)

VIEW_W, VIEW_H = 1200, 630


def render() -> None:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context(
            viewport={"width": VIEW_W, "height": VIEW_H},
            device_scale_factor=2,
        )
        page = context.new_page()
        page.goto(HTML_FILE.as_uri())
        page.wait_for_load_state("networkidle")
        png_bytes = page.locator(".stage").screenshot(type="png")
        browser.close()

    img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    if img.size != (VIEW_W, VIEW_H):
        img = img.resize((VIEW_W, VIEW_H), Image.LANCZOS)
    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT_PNG, format="PNG", optimize=True)
    print(f"wrote {OUT_PNG}")


if __name__ == "__main__":
    render()
