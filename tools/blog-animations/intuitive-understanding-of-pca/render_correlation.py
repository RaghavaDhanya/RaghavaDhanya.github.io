"""Render correlation_animation.html → correlation_morph.webp."""

from __future__ import annotations

from pathlib import Path

from blog_animations import RenderConfig, render

HERE = Path(__file__).parent
ROOT = HERE.parent.parent.parent

if __name__ == "__main__":
    render(
        RenderConfig(
            html=HERE / "correlation_animation.html",
            out=ROOT
            / "static/images/intuitive-understanding-of-pca/correlation_morph.webp",
            phase_durations_ms=[800, 2000, 2000, 2000, 1200],
        )
    )
