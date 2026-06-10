# Animation palette (soft dusty pastels)

Canonical accent palette for blog post animations. The user curates these colors;
role assignment per animation is the author's choice. Style: soft, muted mid-pastels
at similar light value and gentle saturation, cool-leaning with warm accents, calm on white.

## Style: soft, fill-only (no outlines)

Shapes use **solid fills with no strokes** — outlines read as harsh. Edges are carried by
the fill alone, so fills are nudged a touch deeper than a pale tint. Conventions:

- **Towers** get a hint of corner rounding (`roundedPoly(verts, 9)`), never sharp.
- **Panels** (shared latent space, ANN index) are soft filled rounded rects, no border.
- **Frozen / structural blocks** are a soft neutral grey fill (`#eceef2`).
- **"Rings"** (match highlight, cluster centers) are done as fills, not strokes: a soft
  filled halo, or a fill-only "donut" (colored disc + white core).
- The only strokes left are unavoidable **connector lines / arrows / axes**, kept soft
  (`--conn #d7dbe2`) and thin, and the single result-ring accent.

Soft fill triples actually used (fill / pill-or-region tint / dot):

| accent     | fill      | tint      | dot       |
|------------|-----------|-----------|-----------|
| periwinkle | `#b9c8e8` | `#e9eef9` | `#6e8cc4` |
| coral      | `#f0c4b6` | `#fbe9e2` | `#db9f8d` |
| mint       | `#c4e7e0` | `#e7f3ed` | `#6fbfae` |
| cyan       | `#bfe6ea` | `#dff4f5` | `#6fcdd6` |
| neutral    | `#eceef2` | —         | `#b6b6be` |


Each accent has three relatives in the same dusty register:
- **fill** — the shape fill (lighter)
- **line** — outline / dot / connector (deeper, the readable one)
- **tint** — very light wash for pills/cells

| Accent      | mid       | fill      | line      | tint      |
|-------------|-----------|-----------|-----------|-----------|
| periwinkle  | `#8faad5` | `#c3cfe8` | `#6e8cc4` | `#eaf0f9` |
| coral       | `#f1c9bd` | `#f1c9bd` | `#db9f8d` | `#fbeae4` |
| mint green  | `#8fd3c8` | `#c4e7e0` | `#5fb6a8` | `#e6f5f1` |
| cyan        | `#8ce7ef` | `#c2f0f4` | `#4fbfcb` | `#e3f9fb` |
| rose        | `#eeb4ca` | `#f6d4e0` | `#d98aa6` | `#fbe9f0` |
| yellow      | `#ecd99a` | `#f5eed0` | `#d9c47e` | `#faf5e2` |

The mint "shared latent space" and the yellow "index" are deliberately different colors:
the latent space is a concept, the index is the concrete thing we actually query.

Neutrals (shared):

| role        | hex       |
|-------------|-----------|
| bg          | `#ffffff` |
| ink         | `#4b4b55` |
| secondary   | `#8a8a93` |
| mid grey    | `#b6b6be` |
| hairline    | `#dcdce2` |
| faint       | `#eef0f3` |
| panel fill  | `#fbfdfc` |

## Role assignments so far

- **two-tower-generic** — query/text = periwinkle, candidate/image = coral, shared latent space = mint.
- **two-tower-ours** — text tower = periwinkle, image tower = coral, shared latent space = mint; frozen encoders = neutral grey (dashed), trained = colored.
- **inference-flow** — CLIP encoders = cyan, image/ingestion path = coral, text/query path = periwinkle, ANN index = mint, results = coral. Progressive reveal: ingestion lane first, query lane on query, results arrow last; single continuous dot draws each curve behind it.
- **ann-clustering** — clusters = cyan / coral / mint, query = ink, winner = nearest (coral here) highlighted, others dimmed, result ring = ink. Caption narrates compare → pick → search.
