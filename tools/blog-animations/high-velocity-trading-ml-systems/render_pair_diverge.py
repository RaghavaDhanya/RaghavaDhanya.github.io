"""Render pair_diverge_animation.html → pair-diverge.webp."""

from __future__ import annotations

from pathlib import Path

from blog_animations import RenderConfig, render

HERE = Path(__file__).parent
ROOT = HERE.parent.parent.parent

if __name__ == "__main__":
    render(
        RenderConfig(
            html=HERE / "pair_diverge_animation.html",
            out=ROOT / "static/images/high-velocity-trading-ml-systems/pair-diverge.webp",
            phase_durations_ms=[300, 1500, 1500, 700, 1700],
        )
    )
