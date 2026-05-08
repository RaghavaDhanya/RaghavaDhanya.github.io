"""Render projection_animation.html → projection.webp."""

from __future__ import annotations

from pathlib import Path

from blog_animations import RenderConfig, render

HERE = Path(__file__).parent
ROOT = HERE.parent.parent.parent

if __name__ == "__main__":
    render(
        RenderConfig(
            html=HERE / "projection_animation.html",
            out=ROOT / "static/images/intuitive-understanding-of-pca/projection.webp",
            phase_durations_ms=[1000, 1000, 2200, 1000, 1600, 1600],
        )
    )
