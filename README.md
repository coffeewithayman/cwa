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
- Clicking a satellite node opens its `href` in a new tab. Hovering scales
  the node up, glows its ring, brightens its connector line, and shows the
  tooltip.
- A node with `children` doesn't link out — clicking it toggles a fan-out
  of smaller sub-bubbles (with their own connector lines back to the
  parent). Only one expanded group at a time; clicking elsewhere or
  pressing Escape closes it. On mobile this is a native accordion instead.
- Below 700px width, the graph is replaced by `MobileLinkList.astro` — a
  stacked list with the same nodes/links, since a force graph doesn't work
  well on small screens.

---

*This README is kept up to date after any significant change to the site —
if something here looks stale, treat the code as the source of truth and
flag it.*
