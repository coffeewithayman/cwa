# ayman.network — network graph site

A single-page Astro site: a center node surrounded by satellite link nodes,
rendered as an interactive graph on desktop and a stacked list on mobile.

## Running locally

```sh
npm install
npm run dev      # http://localhost:4321
```

```sh
npm run build     # outputs to ./dist
npm run preview   # preview the production build
```

> **Note:** the dev server's file-watcher can be unreliable in some sandboxed
> environments (e.g. WSL2). If you edit a file and the browser doesn't
> update, stop the dev server (Ctrl-C) and run `npm run dev` again.

## Everything you'll want to edit lives in one file

**[`src/data/site.config.ts`](src/data/site.config.ts)**

This is the only file you need to touch for day-to-day changes: colors, the
center node, the satellite nodes, and the header/about/elsewhere/footer text.

### Adding or removing a node

Add or remove an entry in the `nodes` array. The circular layout
recalculates automatically — you never need to set x/y positions.

```ts
{
  id: "my-new-thing",              // unique, used internally
  mainText: "My New\nThing",       // "\n" forces a line break
  secondaryText: "LABEL",          // small caption, e.g. "PODCAST"
  tooltip: "Shown on hover",
  href: "https://example.com",
  size: 120,                       // optional, px diameter — omit to use theme default
  ringColor: "#4a9eff",            // optional — omit to use theme default
},
```

### Nesting sub-bubbles under a node

Give a node a `children` array (of `SubNodeConfig` entries — same shape,
minus `size`/nesting) and it becomes an **expandable** bubble instead of a
direct link: on desktop it renders as a button that fans its children out
into smaller sub-bubbles (with connector lines) when clicked; on mobile it
renders as a `<details>/<summary>` accordion. See the `misc-projects` entry
in `site.config.ts` for a working example.

```ts
{
  id: "misc-projects",
  mainText: "Misc\nProjects",
  secondaryText: "GITHUB",
  tooltip: "Click to expand",
  href: "#",                       // unused — clicking expands instead of navigating
  ringColor: "#8a8a8a",
  children: [
    { id: "child-1", mainText: "Thing One", secondaryText: "GITHUB", tooltip: "...", href: "https://..." },
    // ...
  ],
},
```

Sub-bubbles can't have their own `children` — nesting only goes one level
deep.

### Changing colors

Edit the `theme` object. Every color used on the site comes from here:

| Field                 | What it controls                              |
| ---------------------- | --------------------------------------------- |
| `backgroundColor`      | Page background                                |
| `innerGlowColor`       | The glow behind the center node ("inside space")|
| `defaultRingColor`     | Outer ring color for nodes without their own `ringColor` |
| `defaultNodeSize`      | Node diameter (px) for nodes without their own `size` |
| `textColor`            | Primary text color                             |
| `secondaryTextColor`   | Muted/caption text color                       |
| `lineColor`            | The dotted connector lines                     |
| `centerRingColor`      | Center node's ring                             |
| `centerNodeSize`       | Center node diameter (px)                      |
| `ctaBackgroundColor` / `ctaTextColor` | The center node's CTA button       |

### Editing the center node

Edit the `centerNode` object: `name`, `title`, optional `extraText`, and an
optional `cta` (`{ label, href }`) — the only link allowed on the center
node, matching the "Book a call" button in the design.

### Editing the "About" box and "Elsewhere" links

Both live in `chrome`:

- `chrome.aboutTextMarkdown` — free-form **Markdown** (paragraphs,
  `**bold**`, `_italic_`, `[links](https://...)`), rendered via
  [`marked`](https://www.npmjs.com/package/marked).
- `chrome.elsewhereLinks` — an array of `{ label, href, icon }` entries, e.g.:

  ```ts
  { label: "GitHub", href: "https://github.com/you", icon: "github" },
  ```

  `icon` picks the glyph rendered next to the label — see the `icons` map in
  [`ElsewhereList.astro`](src/components/ElsewhereList.astro) for the
  supported keys (`x`, `linkedin`, `youtube`, `instagram`, `github`, `rss`).
  Every link automatically gets the small "↗" arrow — you don't need to add
  it yourself.

### Header/footer text

Also in `chrome`: `headerLabel` (top-left), `aboutTitle`/`elsewhereTitle`
(panel headings), and `footerText`/`footerRight` (bottom bar). The node
count in the top-right updates automatically based on how many entries are
in `nodes`.

## Project structure

- [`src/data/site.config.ts`](src/data/site.config.ts) — edit this for content/color/node changes
- [`src/layouts/Layout.astro`](src/layouts/Layout.astro) — HTML shell, injects theme as CSS variables
- `src/components/`
  - [`NetworkGraph.astro`](src/components/NetworkGraph.astro) — desktop graph: circular layout, SVG lines, hover effects
  - [`CenterNode.astro`](src/components/CenterNode.astro)
  - [`MobileLinkList.astro`](src/components/MobileLinkList.astro) — stacked-list fallback under 700px width
  - [`AboutBox.astro`](src/components/AboutBox.astro) — renders aboutTextMarkdown
  - [`ElsewhereList.astro`](src/components/ElsewhereList.astro) — renders elsewhereLinks with icons
- [`src/pages/index.astro`](src/pages/index.astro) — assembles the page

You generally shouldn't need to touch anything outside of
[`src/data/site.config.ts`](src/data/site.config.ts) unless you're changing layout/behavior itself
(e.g. graph size, animation, breakpoints) — those live in
[`NetworkGraph.astro`](src/components/NetworkGraph.astro) and [`pages/index.astro`](src/pages/index.astro).

## Behavior notes

- Satellite nodes are arranged evenly in a circle; the first node starts
  straight up (12 o'clock) and the rest follow clockwise.
- Clicking a satellite node opens its `href` in a new tab (internal links like `/talks/` open in the same tab). Hovering scales
  the node up, glows its ring, brightens its connector line, and shows the
  tooltip.
- A node with `children` doesn't link out — clicking it toggles a fan-out
  of smaller sub-bubbles (with their own connector lines back to the
  parent). Only one expanded group at a time; clicking elsewhere or
  pressing Escape closes it. On mobile this is a native accordion instead.
- Below 700px width, the graph is replaced by `MobileLinkList.astro` — a
  stacked list with the same nodes/links, since a force graph doesn't work
  well on small screens.

## Talks & Videos (`/talks`)

A searchable archive of every talk, panel, interview and podcast appearance,
with transcripts. The website only reads generated files
(`src/data/talks.json`, `src/content/transcripts/*.json`); everything is
driven from plain Markdown in [`intake/`](intake/) and processed locally on
the GPU by [`ingest/`](ingest/) (Python, managed with `uv`).

### What goes in

**Videos only**: talks, panels, interviews, webinars, filmed podcast
appearances and the @coffeewithayman channel. Audio-only podcasts are out
(links are skipped automatically; audio files dropped into the inbox are moved
to `media/inbox/_failed/`). Getting Into Infosec is deliberately not included. Enterprise Security Weekly
episodes are listed separately in [`intake/esw.md`](intake/esw.md) — they'll
link to Ayman's segment of each episode (workflow not built yet).
Recordings where the voiceprint finds no trace of Ayman are skipped.

### Adding talks

- **A link:** paste it under `## Inbox` in [`intake/talks.md`](intake/talks.md) and save.
- **A video:** drop it into `media/inbox/` (`.mp4 .mov .mkv .webm .m4v .avi`).
  Optional: a same-named `.md` next to it with `# Title`, `- format:`, `- event:`, `- date:`,
  `- topics:` lines and a `### Notes` section.
- **A batch of links:** drop a `.txt` file of URLs into `media/inbox/`.

With the watcher running these are picked up within seconds. Without it, run
`npm run ingest`. Each entry in `talks.md` gets a status line
(⏳ queued → ⬇️ → 🎧 → 👂 → ✅, or 👤 needs speaker review / ⏸ waiting for GPU / ⚠️ error).

### What gets indexed

`format` on each entry decides it: `talk`/`webinar` and one-on-one
`interview`/`podcast-guest` keep the whole recording; `panel`/`cohost` keep only
Ayman's parts, each with the question before it as context. If `format` is
blank the pipeline guesses from the number of voices — fix it if wrong and the
talk is re-published.

Speaker identification compares each voice to Ayman's voiceprint (built from
clips listed in [`intake/voiceprint.md`](intake/voiceprint.md), `npm run enroll`)
and checks the transcript names him. When unsure, the talk lands in
[`intake/speakers.md`](intake/speakers.md) with a 10-second sample per voice:
tick the right one and save. Confirmed voices are added to the voiceprint.

### Summaries

Clicking a title on `/talks` expands a 2–3 sentence summary. Summaries come
from a local model through [Ollama](https://ollama.com) — no API keys
anywhere: `qwen3:14b` by default, `qwen3:4b` with the low-VRAM profile
(override with `CWA_SUMMARY_MODEL`). If Ollama isn't already running the
pipeline starts it for the run and pulls the model on first use. The summary
is written into the entry's `summary:` line in `talks.md`; edit it freely —
it's only generated while that line is empty (clear it to regenerate).

### Vocabulary and notes

[`intake/vocab.md`](intake/vocab.md) holds terms (spelling/casing, also fed to
Whisper) and a heard→correct table. After editing, `npm run ingest -- --reclean`
re-applies it without re-transcribing. Add bullets under any entry's
`### Notes`; `npm run notes` lists open ones and `/process-notes` in Claude Code
works through them, striking each through when done.

### Commands

| Command | What it does |
|---|---|
| `npm run ingest` | One pass: inbox, reviews, then every talk whose inputs changed (`-- --only <slug>`, `-- --force`, `-- --reclean`) |
| `npm run watch` | Keep running and react to `media/inbox/` and `intake/*.md` |
| `npm run watch:install` | Install the watcher as a systemd user service (starts at boot) |
| `npm run enroll` | Build the voiceprint from `intake/voiceprint.md` |
| `npm run notes` | List open notes |
| `npm run test:ingest` | Pipeline unit tests |

Setup: `cd ingest && uv sync`, then `hf auth login` with an account that has
accepted the terms of `pyannote/speaker-diarization-community-1`. The pipeline
needs ~9 GB free VRAM and waits (⏸) when another process is using the GPU.
On a 6 GB card (e.g. RTX 3050, including under WSL2) put `CWA_PROFILE=low-vram`
in `ingest/.env`: int8 weights, batch 1 and models unloaded between stages cut
the peak to ~3.6 GB for roughly 2x the time. Under WSL, `npm run watch:install`
needs systemd enabled (`[boot] systemd=true` in `/etc/wsl.conf`, then `wsl --shutdown`).

---

*This README is kept up to date after any significant change to the site —
if something here looks stale, treat the code as the source of truth and
flag it.*
