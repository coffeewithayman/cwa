// Filtering + sorting for /talks. Rows are server-rendered; this only hides,
// shows and reorders them. Filter state lives in the URL so views are shareable.

type SortKey = "date" | "title" | "format" | "event" | "category" | "duration";

const form = document.querySelector<HTMLFormElement>("[data-filters]");
const table = document.querySelector<HTMLTableElement>("[data-table]");

if (form && table) {
  const tbody = table.tBodies[0];
  const rows = Array.from(tbody.rows);
  const chips = Array.from(document.querySelectorAll<HTMLButtonElement>("[data-topic]"));
  const status = document.querySelector<HTMLElement>("[data-status]");
  const selects = ["category", "format", "event", "year", "platform"] as const;
  const field = (name: string) => form.elements.namedItem(name) as HTMLInputElement | HTMLSelectElement | null;

  let sortKey: SortKey = "date";
  let sortDir: 1 | -1 = -1;

  function readUrl() {
    const params = new URLSearchParams(location.search);
    const q = field("q");
    if (q) q.value = params.get("q") ?? "";
    for (const name of selects) {
      const el = field(name);
      if (el) el.value = params.get(name) ?? "";
    }
    const wanted = new Set(params.getAll("topic"));
    for (const chip of chips) chip.setAttribute("aria-pressed", String(wanted.has(chip.dataset.topic!)));
    const sort = params.get("sort");
    if (sort) {
      const [key, dir] = sort.split(":");
      sortKey = key as SortKey;
      sortDir = dir === "asc" ? 1 : -1;
    }
  }

  function writeUrl() {
    const params = new URLSearchParams();
    const q = field("q")?.value.trim();
    if (q) params.set("q", q);
    for (const name of selects) {
      const v = field(name)?.value;
      if (v) params.set(name, v);
    }
    for (const chip of chips) if (chip.getAttribute("aria-pressed") === "true") params.append("topic", chip.dataset.topic!);
    if (sortKey !== "date" || sortDir !== -1) params.set("sort", `${sortKey}:${sortDir === 1 ? "asc" : "desc"}`);
    const qs = params.toString();
    history.replaceState(null, "", qs ? `?${qs}` : location.pathname);
  }

  function apply() {
    const q = (field("q")?.value ?? "").trim().toLowerCase().split(/\s+/).filter(Boolean);
    const want = Object.fromEntries(selects.map((n) => [n, field(n)?.value ?? ""]));
    const topics = chips.filter((c) => c.getAttribute("aria-pressed") === "true").map((c) => c.dataset.topic!);

    let shown = 0;
    for (const row of rows) {
      const d = row.dataset;
      const rowTopics = (d.topics ?? "").split("|");
      const ok =
        selects.every((n) => !want[n] || d[n] === want[n]) &&
        topics.every((t) => rowTopics.includes(t)) &&
        q.every((term) => (d.search ?? "").includes(term));
      row.hidden = !ok;
      if (ok) shown++;
    }

    const sorted = [...rows].sort((a, b) => {
      const av = a.dataset[sortKey] ?? "";
      const bv = b.dataset[sortKey] ?? "";
      const cmp = sortKey === "duration" ? Number(av) - Number(bv) : av.localeCompare(bv);
      return cmp * sortDir || (b.dataset.date ?? "").localeCompare(a.dataset.date ?? "");
    });
    tbody.append(...sorted);

    for (const th of table!.tHead!.querySelectorAll<HTMLElement>("th[data-sort]")) {
      th.setAttribute("aria-sort", th.dataset.sort === sortKey ? (sortDir === 1 ? "ascending" : "descending") : "none");
    }
    if (status) status.textContent = shown === rows.length ? "" : `Showing ${shown} of ${rows.length}`;
    writeUrl();
  }

  form.addEventListener("input", apply);
  for (const chip of chips) {
    chip.addEventListener("click", () => {
      chip.setAttribute("aria-pressed", String(chip.getAttribute("aria-pressed") !== "true"));
      apply();
    });
  }
  for (const th of table.tHead!.querySelectorAll<HTMLElement>("th[data-sort]")) {
    th.querySelector("button")!.addEventListener("click", () => {
      const key = th.dataset.sort as SortKey;
      sortDir = key === sortKey ? ((-sortDir) as 1 | -1) : key === "date" || key === "duration" ? -1 : 1;
      sortKey = key;
      apply();
    });
  }
  document.querySelector("[data-reset]")?.addEventListener("click", () => {
    form.reset();
    for (const chip of chips) chip.setAttribute("aria-pressed", "false");
    sortKey = "date";
    sortDir = -1;
    apply();
  });

  readUrl();
  apply();
}
