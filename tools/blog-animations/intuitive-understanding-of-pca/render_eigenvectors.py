"""Render eigenvectors_animation.html → eigenvectors.webp."""

from __future__ import annotations

from pathlib import Path

from blog_animations import RenderConfig, render

HERE = Path(__file__).parent
ROOT = HERE.parent.parent.parent

if __name__ == "__main__":
    render(
        RenderConfig(
            html=HERE / "eigenvectors_animation.html",
            out=ROOT / "static/images/intuitive-understanding-of-pca/eigenvectors.webp",
            phase_durations_ms=[1200, 2600, 2400],
        )
    )
