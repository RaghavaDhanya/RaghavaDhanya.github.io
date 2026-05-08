"""Render pair_revert_animation.html → pair-revert-{1,2,3}.webp.

Variant is selected via URL fragment; the HTML reads location.hash to choose
which path geometry to draw.
"""

from __future__ import annotations

from pathlib import Path

from blog_animations import RenderConfig, render

HERE = Path(__file__).parent
ROOT = HERE.parent.parent.parent
HTML = HERE / "pair_revert_animation.html"
OUT_DIR = ROOT / "static/images/high-velocity-trading-ml-systems"
PHASES = [300, 900, 1500, 700, 1700, 1700]

if __name__ == "__main__":
    for variant in ("1", "2", "3"):
        render(
            RenderConfig(
                html=HTML,
                out=OUT_DIR / f"pair-revert-{variant}.webp",
                phase_durations_ms=PHASES,
                url_fragment=variant,
            )
        )
