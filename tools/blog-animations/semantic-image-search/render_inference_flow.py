"""Render inference_flow.html → inference-flow.webp."""

from __future__ import annotations

from pathlib import Path

from blog_animations import RenderConfig, render

HERE = Path(__file__).parent
ROOT = HERE.parent.parent.parent

if __name__ == "__main__":
    render(
        RenderConfig(
            html=HERE / "inference_flow.html",
            out=ROOT / "static/images/semantic-image-search/inference-flow.webp",
            phase_durations_ms=[1900, 2900, 1200],
            fps=30,
        )
    )
