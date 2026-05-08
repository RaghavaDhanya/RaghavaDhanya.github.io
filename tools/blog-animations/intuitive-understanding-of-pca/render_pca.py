"""Render pca_animation.html → height_weight_pca.webp."""

from __future__ import annotations

from pathlib import Path

from blog_animations import RenderConfig, render

HERE = Path(__file__).parent
ROOT = HERE.parent.parent.parent

if __name__ == "__main__":
    render(
        RenderConfig(
            html=HERE / "pca_animation.html",
            out=ROOT
            / "static/images/intuitive-understanding-of-pca/height_weight_pca.webp",
            phase_durations_ms=[1200, 1400, 1200, 1000, 1800, 2400, 1200],
        )
    )
