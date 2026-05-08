"""Render pair_example_animation.html → pair-example.webp."""

from __future__ import annotations

from pathlib import Path

from blog_animations import RenderConfig, render

HERE = Path(__file__).parent
ROOT = HERE.parent.parent.parent

if __name__ == "__main__":
    render(
        RenderConfig(
            html=HERE / "pair_example_animation.html",
            out=ROOT / "static/images/high-velocity-trading-ml-systems/pair-example.webp",
            phase_durations_ms=[2800, 1400, 2200, 600],
        )
    )
