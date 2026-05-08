"""Render covariance_transform_animation.html → covariance_transform.webp."""

from __future__ import annotations

from pathlib import Path

from blog_animations import RenderConfig, render

HERE = Path(__file__).parent
ROOT = HERE.parent.parent.parent

if __name__ == "__main__":
    render(
        RenderConfig(
            html=HERE / "covariance_transform_animation.html",
            out=ROOT
            / "static/images/intuitive-understanding-of-pca/covariance_transform.webp",
            phase_durations_ms=[1000, 2500, 1000, 1500, 1500],
        )
    )
