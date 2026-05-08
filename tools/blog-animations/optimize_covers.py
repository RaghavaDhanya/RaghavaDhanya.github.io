"""Re-encode the non-rendered post covers to WebP under assets/.

PCA cover is rendered separately via intuitive-understanding-of-pca/render_cover.py.
"""

from __future__ import annotations

from pathlib import Path

from blog_animations import optimize_cover_image

ROOT = Path(__file__).parent.parent.parent
STATIC = ROOT / "static" / "images"
ASSETS = ROOT / "assets" / "images"

# P-mode PNG illustrations: preserve palette, save lossless WebP. libwebp
# applies its color-indexing transform automatically.
optimize_cover_image(
    src=STATIC / "golang-for-machine-learning-serving/go_mab_wide.png",
    out=ASSETS / "golang-for-machine-learning-serving/cover.webp",
    target_width=1500,
    palette=True,
)
optimize_cover_image(
    src=STATIC / "python-with-a-dash-of-cpp-optimizing/cpp_python1.png",
    out=ASSETS / "python-with-a-dash-of-cpp-optimizing/cover.webp",
    target_width=1500,
    palette=True,
)

# Photo: lossy WebP q90.
optimize_cover_image(
    src=STATIC / "sane-configs-with-pydantic-settings/cover.jpg",
    out=ASSETS / "sane-configs-with-pydantic-settings/cover.webp",
    target_width=1500,
    palette=False,
    quality=90,
)
