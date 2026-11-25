# Curation, Normalization, and Classification Policy

This document is the **canonical curation rulebook** for the CheapInfra resource library. Every collection agent, enrichment pass, and reviewer MUST follow it strictly before keeping, dropping, normalizing, or classifying any link. Where an external automation prompt or summary conflicts with this file, **this policy wins**.

---

## 1. Keep vs. Drop Decision Flow

Run every candidate link through these checks in order:

### A. Wrapper vs. Underlying Resource Check (Promos, Deals, Notices)
Never index a promo, discount, coupon, student deal, or vendor incident/privacy/outage notice URL directly (e.g. `/black-friday`, `/ai-student`, `/promo`, `/privacy-notice`, `/incident`).

Before dropping a promotional or announcement post, inspect the **underlying product, tool, or provider**:
1. **Underlying resource is already published** (or queued on the current branch) → **Drop** as a duplicate / time-bound notice.
2. **Underlying resource is new and genuinely useful to developers** → Resolve it to its **clean evergreen homepage** (or `/pricing` for an inference provider when pricing is the core developer reference), write an **evergreen brief** (describe what the product does, not the temporary discount), and **keep** that normalized URL. Mention any temporary offer only as context in the daily notes if relevant.
3. **Underlying offering is a consumer/student promo or non-developer deal** (e.g. a student subscription discount like `one.google.com/ai-student`) → **Drop** completely.

### B. Always Drop
- **Hype, memes, GIFs, videos, or unclassifiable bare links** with no retrievable context.
- **Exact duplicates** or near-duplicates of already-published resources.
- **Models and model weights** (2026-11-14 rule): Hugging Face model repos, GGUF/FP8/MLX/quantized builds, fine-tunes, open-weights announcements, and single-model launch or docs pages (e.g. a vendor's `"Qwen4-Max-Preview"` page). *Still keep:* inference providers (including a provider's pricing page for a model), developer tools, apps, benchmarks/leaderboards, datasets, and articles *about* models.
- **Time-bound vendor notices & news**: security breach posts, privacy notices, outage postmortems, quota-reset announcements, funding/stock news.
- **Login-walled or geo-gated pages** where you cannot verify the resource without signing in (unless a public product homepage or documentation URL exists — if so, normalize to the public URL and verify it returns HTTP 200).
- **Conversational / non-reusable shares**: personal gists, one-off reply threads, or throwaway demos not intended as a reusable tool, library, provider, or developer reference.
- **Subpages of already-published resources**: docs subpages, changelogs, or feature announcements of a site/provider already in the catalog (e.g. `openrouter.ai/docs/...`), unless the subpage is a genuinely distinct, standalone tool or repository.

### C. Tweet & Announcement Extraction (2026-10-04 Rule)
- **Never drop an announcement tweet just for being an announcement.** Extract every outbound link inside the tweet (and Discord embed) and evaluate each link individually against Sections 1A–1B; attribute kept resources to the tweet's Discord sharer.
- **Tweet without an outbound link:** If a tweet names a concrete tool or repository without linking it directly, web-search resolution is allowed **only** if the resolved URL is live-verified (HTTP 200) and the resolution is explicitly documented in `notes/daily-*.md`.
- Never use `x.com`, `twitter.com`, `fxtwitter.com`, `vxtwitter.com`, or `t.co` status URLs as a resource's `URL:` when an outbound tool/site/repo link exists (or when none exists, drop as link-less announcement).

---

## 2. Channel ≠ Section or Classification

Classify every kept resource strictly by **what the resource actually is**, never by which Discord channel (`#share-tech` vs `#providers`) it was posted in.

| Resource nature | Section in `notes/` | Site category (`Category:`) | Catalog `resource_type` |
|---|---|---|---|
| **Actual inference / API provider** (developers sign up, get an API key, or buy/run model inference — e.g. Unaligned, DeepInfra, OpenRouter) | `## Providers` | `providers` | `provider` |
| **Non-provider resource shared in `#providers`** (benchmarks, arenas, leaderboards, articles/analyses, pricing trackers, CLI/IDE plugins, SDKs, GitHub repos) | `## Week: <label>` (or `## Fold into week:`) | Normal site categories (`ai-tool`, `dev-tool`, `web-app`, `github`, `article` — **never** `providers`) | Its true type (`tool`, `article-guide`, `repository`, `directory-gallery`, `service-platform`, etc.) |
| **Inference / API provider shared in `#share-tech`** | `## Providers` | `providers` | `provider` |

- Raw Discord channel provenance stays intact in `raw/daily-*.md` regardless of which section the curated entry lands in.
- **`providers` consistency rule:** `## Providers`, `Category: providers`, and `resource_type: provider` are reserved **exclusively** for actual inference/API providers. Benchmarks and provider-comparison websites (e.g. BlackBox Arena, Artificial Analysis) are **not** `providers`.

---

## 3. URL Normalization & Granularity

Apply these rules before deduplicating and before writing `- URL:`:

1. **Strip tracking and session noise:**
   - Remove `utm_*`, `?s=20`, `?s=46`, `?a=...`, `?ref=...`, view/sort params, and Google account-index segments (`/u/0/`, `/u/1/`).
   - Always use clean `https://` URLs.
2. **Root site vs. deep link:**
   - If the **domain/product is new to the catalog** and the shared URL is a narrow subpage of a broader platform, benchmark, or tool site (for example, `blackboxarena.ai/compare/deepseek-v4-1-flash-providers/`), normalize to the **root site** (`https://blackboxarena.ai/`) and describe the specific board or feature in the brief/details.
   - Keep a **deep link** only when the resource *is* that specific target:
     - A standalone article, essay, or blog post.
     - A specific repository (`https://github.com/<org>/<repo>`).
     - An inference provider's `/pricing` page when it is the primary developer reference and clearer than the marketing homepage.

---

## 4. Classification Decision Matrix

### A. Site Categories (`- Category:` in `notes/`)
Pick **one or two** categories per resource from the active set (`ai-tool`, `dev-tool`, `github`, `web-app`, `article`, `providers`):

| Category | When to use | Typical pairing |
|---|---|---|
| `providers` | Inference/API providers **only** | Usually standalone (`providers`) |
| `github` | Open/public source code repository on GitHub/GitLab | Pair with `ai-tool` or `dev-tool` |
| `ai-tool` | AI apps, coding-agent skills, evals/benchmarks, MCP servers, AI utilities | Pair with `github` or `web-app` |
| `dev-tool` | General developer tools, CLIs, SDKs, libraries, infra/testing utilities | Pair with `github` or `web-app` |
| `web-app` | Interactive browser tools, playgrounds, dashboards, benchmarks/arenas | Pair with `ai-tool` or `dev-tool` |
| `article` | Blog posts, essays, guides, technical comparisons/write-ups | Usually standalone (`article`) |

### B. Catalog Facets (`catalog/taxonomy/*.json`)
- **`resource_type` (exactly 1):**
  - `provider`: Inference/API provider only.
  - `repository`: Source-code repo (typically paired with site category `github`).
  - `tool`: Standalone utility, CLI, agent skill, or interactive benchmark/arena web app.
  - `service-platform`: Hosted SaaS/PaaS product requiring signup/hosting.
  - `library-framework`: Reusable code library, SDK, UI kit, or framework.
  - `article-guide`: Article, blog post, tutorial, or static analysis write-up.
  - `directory-gallery`: Curated directory, gallery, awesome-list, or multi-skill collection.
  - `documentation`: Reference docs site.
  - `template-starter`: Project template or starter kit.
  - `dataset`: Benchmark or evaluation dataset (never model weights).
  - `other`: Only when none of the above fit.
- **`topics` (1–3 preferred, max 5):** Use only active slugs in `catalog/taxonomy/topics.json`; avoid tag stuffing.
- **`use_cases` (1–2 preferred, max 6):** Use only active slugs in `catalog/taxonomy/use-cases.json`.
- **`interfaces` (0–5) & `technologies` (0–8):** Only include values explicitly evidenced on the page or in the source post.
- **`open_source`:** Set `true` only when the brief explicitly confirms open source (e.g. `"open-source"` / `"open source"`); otherwise `null`. Never guess `license` (leave `null` unless verified).

### C. Extending Categories or Taxonomy When Justified
Do **not** force a resource into a mismatched box if a genuinely distinct, recurring concept does not fit the existing labels:
1. **Prefer extending `catalog/taxonomy/*.json` first** for new `resource_type`, `topics`, `use_cases`, `interfaces`, or `technologies` slugs (and keep `schemas/resource.schema.json` in sync).
2. **Adding a new site category** (`Category:`) is also permitted when clearly justified for a recurring class of resources (not for a one-off item):
   - Add its label and chip/color styling in `scripts/build.py`.
   - Update `KNOWN_CATEGORIES` in `tests/test_invariants.py`, the enum in `schemas/resource.schema.json`, `AGENTS.md`, and this policy doc.
   - Call out the new category and its rationale prominently in the PR body for review.

---

## 5. Brief, Warning, Details, and PR Review Hygiene

- **Brief (`- Brief:`):** ~2 sentences describing what the resource does and why a developer would use it. Do not repeat promo hype or copy-paste marketing slogans without framing.
- **Warning (`- Warning:`):** Put caveats, unverified vendor claims, experimental status, telemetry defaults, or pricing caveats in a dedicated `- Warning:` bullet (never inline inside `- Brief:`). `scripts/build.py` parses `- Warning:` directly into `warning` / `caveat`.
- **Details (`notes/details-*.md`):** ≤2,000 characters, researched from the live page. Any vendor-reported benchmark numbers, user-preference percentages, or pricing figures **must** be explicitly attributed as vendor-reported/unverified. Any region-specific pricing **must** state the currency/region.
- **PR Review Table:** Every daily PR body **must** include a concise Markdown table covering every added resource, plus a 1-line summary of drops:

```markdown
| Title | Found in → Placed in | Categories | resource_type | URL normalization & why kept |
|---|---|---|---|---|
| Example | `#providers` → `19–26 Nov 2026` | `ai-tool, web-app` | `tool` | Normalized `/compare/...` to root; benchmarking site |
```
