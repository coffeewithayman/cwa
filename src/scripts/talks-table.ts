// Filtering + sorting for /talks. Rows are server-rendered; this only hides,
// shows, reorders and renumbers them. State lives in the URL so views are shareable.

type SortKey = "date" | "title" | "format" | "event" | "duration";

const table = document.querySelector<HTMLTableElement>("[data-table]");

if (table) {
  const tbody = table.tBodies[0];
  const rows = Array.from(tbody.rows);
  const chips = Array.from(document.querySelectorAll<HTMLButtonElement>("[data-kind]"));
  const status = document.querySelector<HTMLElement>("[data-status]");
  const sortToggle = document.querySelector<HTMLButtonElement>("[data-sort-toggle]");
  const search = document.querySelector<HTMLInputElement>('input[name="q"]');
  const selects = (["category", "topic", "event"] as const)
    .map((name) => document.querySelector<HTMLSelectElement>(`select[name="${name}"]`))
    .filter((el): el is HTMLSelectElement => !!el);

  let kind = "";
  let sortKey: SortKey = "date";
  let sortDir: 1 | -1 = -1;

  function readUrl() {
    const p = new URLSearchParams(location.search);
    kind = p.get("kind") ?? "";
    if (search) search.value = p.get("q") ?? "";
    for (const el of selects) el.value = p.get(el.name) ?? "";
    const sort = p.get("sort");
    if (sort) {
      const [key, dir] = sort.split(":");
      sortKey = key as SortKey;
      sortDir = dir === "asc" ? 1 : -1;
    }
  }

  function writeUrl() {
    const p = new URLSearchParams();
    if (kind) p.set("kind", kind);
    const q = search?.value.trim();
    if (q) p.set("q", q);
    for (const el of selects) if (el.value) p.set(el.name, el.value);
    if (sortKey !== "date" || sortDir !== -1) p.set("sort", `${sortKey}:${sortDir === 1 ? "asc" : "desc"}`);
    const qs = p.toString();
    history.replaceState(null, "", qs ? `?${qs}` : location.pathname);
  }

  function matches(row: HTMLTableRowElement): boolean {
    const d = row.dataset;
    if (kind && d.format !== kind) return false;
    for (const el of selects) {
      if (!el.value) continue;
      if (el.name === "topic" ? !(d.topics ?? "").split("|").includes(el.value) : d[el.name] !== el.value) return false;
    }
    const terms = (search?.value ?? "").trim().toLowerCase().split(/\s+/).filter(Boolean);
    return terms.every((t) => (d.search ?? "").includes(t));
  }

  function apply() {
    const sorted = [...rows].sort((a, b) => {
      const av = a.dataset[sortKey] ?? "";
      const bv = b.dataset[sortKey] ?? "";
      const cmp = sortKey === "duration" ? Number(av) - Number(bv) : av.localeCompare(bv);
      return cmp * sortDir || (b.dataset.date ?? "").localeCompare(a.dataset.date ?? "");
    });
    tbody.append(...sorted);

    let n = 0;
    for (const row of sorted) {
      const ok = matches(row);
      row.hidden = !ok;
      if (ok) row.querySelector<HTMLElement>("[data-n]")!.textContent = String(++n).padStart(3, "0");
    }

    for (const chip of chips) chip.setAttribute("aria-pressed", String((chip.dataset.kind ?? "") === kind));
    for (const th of table!.tHead!.querySelectorAll<HTMLElement>("th[data-sort]")) {
      th.setAttribute("aria-sort", th.dataset.sort === sortKey ? (sortDir === 1 ? "ascending" : "descending") : "none");
    }
    if (sortToggle) {
      sortToggle.textContent =
        sortKey === "date" ? `sort: ${sortDir === -1 ? "newest" : "oldest"} first` : `sort: ${sortKey} ${sortDir === 1 ? "↑" : "↓"}`;
    }
    if (status) status.textContent = n === rows.length ? "" : `showing ${n} of ${rows.length}`;
    writeUrl();
  }

  for (const chip of chips) {
    chip.addEventListener("click", () => {
      kind = chip.dataset.kind ?? "";
      apply();
    });
  }
  search?.addEventListener("input", apply);
  for (const el of selects) el.addEventListener("change", apply);
  sortToggle?.addEventListener("click", () => {
    sortDir = sortKey === "date" ? ((-sortDir) as 1 | -1) : -1;
    sortKey = "date";
    apply();
  });
  for (const th of table.tHead!.querySelectorAll<HTMLElement>("th[data-sort]")) {
    th.querySelector("button")!.addEventListener("click", () => {
      const key = th.dataset.sort as SortKey;
      sortDir = key === sortKey ? ((-sortDir) as 1 | -1) : key === "date" || key === "duration" ? -1 : 1;
      sortKey = key;
      apply();
    });
  }

  readUrl();
  apply();
}
