"""Render ann_clustering.html → ann-clustering.webp."""

from __future__ import annotations

from pathlib import Path

from blog_animations import RenderConfig, render

HERE = Path(__file__).parent
ROOT = HERE.parent.parent.parent

if __name__ == "__main__":
    render(
        RenderConfig(
            html=HERE / "ann_clustering.html",
            out=ROOT / "static/images/semantic-image-search/ann-clustering.webp",
            phase_durations_ms=[1500, 1900, 1100, 1900, 1500, 2000, 1300],
            fps=30,
        )
    )
