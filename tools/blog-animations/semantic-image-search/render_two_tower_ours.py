"""Render two_tower_ours.html → two-tower-ours.webp."""

from __future__ import annotations

from pathlib import Path

from blog_animations import RenderConfig, render

HERE = Path(__file__).parent
ROOT = HERE.parent.parent.parent

if __name__ == "__main__":
    render(
        RenderConfig(
            html=HERE / "two_tower_ours.html",
            out=ROOT / "static/images/semantic-image-search/two-tower-ours.webp",
            phase_durations_ms=[2100, 1500, 1700, 1200],
            fps=30,
        )
    )
