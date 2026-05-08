"""Render scaling_matrix_animation.html → scaling_matrix.webp."""

from __future__ import annotations

from pathlib import Path

from blog_animations import RenderConfig, render

HERE = Path(__file__).parent
ROOT = HERE.parent.parent.parent

if __name__ == "__main__":
    render(
        RenderConfig(
            html=HERE / "scaling_matrix_animation.html",
            out=ROOT
            / "static/images/intuitive-understanding-of-pca/scaling_matrix.webp",
            phase_durations_ms=[
                600, 1000, 300, 1000, 400, 1000, 300, 1000, 400, 1000, 300, 1000, 600,
            ],
        )
    )
