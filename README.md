# AI Logs

Source for [ai.ragv.in](https://ai.ragv.in). Hugo site with the PaperMod theme, deployed to GitHub Pages.

This README is a personal reference for how the repo is wired up and how to update the parts that drift over time (Hugo, PaperMod, the deploy workflow).

## Repo layout

```
content/posts/        # blog posts (front matter + markdown)
static/               # served as-is (CNAME, favicons, /images, Logo_2_0.svg)
layouts/partials/     # local overrides on top of PaperMod
  author.html
  extend_head.html
archetypes/default.md # template used by `hugo new`
config.yml            # site config (baseURL, params, menu, social icons)
themes/PaperMod/      # git submodule -> github.com/adityatelange/hugo-PaperMod
tools/blog-animations/# Python (uv) project for rendering per-post animations
.github/workflows/
  gh-pages.yml        # build + deploy pipeline
public/               # generated, gitignored
```

The custom domain is set by `static/CNAME` (`ai.ragv.in`). `baseURL` in `config.yml` must match.

## Branches

- `master` is the deploy branch. Every push triggers `.github/workflows/gh-pages.yml`.
- `dev` is the working branch. Merge dev to master via PR to ship.
- `drafts/*` are long-lived WIP branches for posts that aren't ready.

## Local development

Clone with submodules:

```sh
git clone --recurse-submodules <repo>
# if already cloned:
git submodule update --init --recursive
```

Run the dev server:
In config.yml, comment out `env: production` to disable production-only features like Google Analytics.
```sh
hugo server -D    # -D includes drafts
```

The Hugo version used in CI is pinned in `.github/workflows/gh-pages.yml` (`hugo-version`). Match it locally to avoid surprises.

## Writing a post

```sh
hugo new posts/my-post-title.md
```

This uses `archetypes/default.md`, which sets `draft: true`. Hugo skips drafts in production builds, so flip it to `false` (or remove the line) before merging to master. A previously merged post stayed invisible because of this.

Math is enabled via Goldmark passthrough (`config.yml` -> `markup.goldmark.extensions.passthrough`). Use `\(...\)` or `$...$` inline, `\[...\]` or `$$...$$` for blocks.

For images, drop them under `static/images/<post-slug>/` and reference them as `/images/<post-slug>/...`.

## Deploy pipeline

`.github/workflows/gh-pages.yml`:

1. `actions/checkout` with `submodules: true` (needed for the theme).
2. `peaceiris/actions-hugo` installs the pinned Hugo version.
3. `actions/configure-pages` resolves the Pages base URL (only on master).
4. `hugo --minify --baseURL ...` builds into `public/`.
5. On master, `actions/upload-pages-artifact` uploads `public/` and `actions/deploy-pages` publishes it.

PRs run the build but skip upload and deploy.

To trigger a deploy manually, use the workflow_dispatch button on the Actions page or:

```sh
gh workflow run "github pages" --ref master
```

To check recent runs:

```sh
gh run list --branch master --limit 5
gh run view <run-id> --log
```

## Updating PaperMod

The theme is a submodule pinned to a specific commit. To bump it:

```sh
cd themes/PaperMod
git fetch --tags
git checkout <tag-or-commit>      # e.g. v8.0
cd ../..
git add themes/PaperMod
git commit -m "feat: bump PaperMod to <tag>"
```

After bumping, run `hugo server` locally and check:
- the home page, a post, the categories/tags pages, the RSS feed (`/index.xml`)
- the local overrides in `layouts/partials/` (`author.html`, `extend_head.html`) still render
- any deprecated params in `config.yml` still work (PaperMod renames things between major versions)

The current pin is `v8.0` (commit `f207ce6d`).

## Updating the deploy workflow

Action versions are pinned by commit SHA in `.github/workflows/gh-pages.yml`. Bump them periodically:

- `actions/checkout`
- `peaceiris/actions-hugo` (and `hugo-version` inside it)
- `actions/configure-pages`
- `actions/upload-pages-artifact`
- `actions/deploy-pages`

Dependabot or a manual check works. After editing, push to a branch and open a PR so the build job runs against the new versions before they hit master.

To bump Hugo, change `hugo-version` in the workflow and update the local install to match.

## Updating Go modules

There aren't any Go module dependencies in the Hugo build. Theme components and shortcodes come from the PaperMod submodule.

## Animation tooling

`tools/blog-animations/` is a [uv](https://docs.astral.sh/uv/) project that renders HTML/SVG animation pages to GIFs (Playwright + imageio + Pillow). One subdirectory per post:

```
tools/blog-animations/
  pyproject.toml
  uv.lock
  intuitive-understanding-of-pca/
    *_animation.html
    render_*.py
```

To render:

```sh
cd tools/blog-animations
uv sync
uv run playwright install chromium
uv run python intuitive-understanding-of-pca/render_pca.py
```

Output GIFs go under `static/images/<post-slug>/` so posts can reference them.

## Common gotchas

- A post merged to master but missing from the live site usually has `draft: true`. Hugo silently skips drafts.
- `baseURL` in `config.yml` must match `static/CNAME`. Mismatches break absolute links and the RSS feed.
- Submodule not checked out -> `hugo` fails with a theme-not-found error. Run `git submodule update --init --recursive`.
