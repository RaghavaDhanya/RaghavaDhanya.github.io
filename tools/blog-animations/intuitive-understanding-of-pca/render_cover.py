"""Render cover.html → assets/images/intuitive-understanding-of-pca/cover.webp."""

from __future__ import annotations

from pathlib import Path

from blog_animations import StaticRenderConfig, render_html_cover

HERE = Path(__file__).parent
ROOT = HERE.parent.parent.parent

if __name__ == "__main__":
    render_html_cover(
        StaticRenderConfig(
            html=HERE / "cover.html",
            out=ROOT / "assets/images/intuitive-understanding-of-pca/cover.webp",
            viewport=(1200, 630),
            target_width=1500,
        )
    )
