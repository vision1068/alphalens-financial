"use strict";
// BetaLens dashboard. Plain JS, no build step. All text from data files is inserted with textContent.

const CFG = window.BETALENS;
const SIGNALS = ["STRONG_BUY", "BUY", "HOLD", "SELL", "STRONG_SELL", "INSUFFICIENT_DATA"];
const SIGNAL_LABEL = {
  STRONG_BUY: "Strong Buy", BUY: "Buy", HOLD: "Hold", SELL: "Sell", STRONG_SELL: "Strong Sell",
  INSUFFICIENT_DATA: "Not enough data",
};
const FACTOR_LABEL = {
  revenue_growth: "Revenue growth", earnings_growth: "Earnings growth", profitability: "Profitability",
  cash_flow_quality: "Cash flow quality", cash_conversion_cycle: "Cash conversion cycle", debt: "Debt",
  liquidity: "Liquidity", valuation: "Valuation", dividend: "Dividend", price_trend: "Price trend",
};
const MANUAL_FIELDS = ["equity", "total_debt", "ebit", "interest_expense", "operating_cash_flow", "capex",
  "current_assets", "current_liabilities", "receivables", "inventory", "payables", "cost_of_sales",
  "dividend_per_share"];
const HOLD_KEY = "betalens.holdings.v1";

const $ = (id) => document.getElementById(id);
const state = { scores: [], bySymbol: {}, payouts: [], sort: { key: "score", dir: -1 }, signal: "" };

function el(tag, props = {}, children = []) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(props)) {
    if (k === "class") node.className = v;
    else if (k === "text") node.textContent = v;
    else node.setAttribute(k, v);
  }
  for (const c of [].concat(children)) node.append(c);
  return node;
}
const fmt = (n, d = 2) => (n === null || n === undefined || Number.isNaN(n)) ? "–"
  : Number(n).toLocaleString("en-US", { minimumFractionDigits: d, maximumFractionDigits: d });
const chip = (signal) => el("span", { class: `chip ${signal}`, text: SIGNAL_LABEL[signal] || signal });
const fmtDate = (iso) => iso ? new Date(iso + "T00:00:00").toLocaleDateString("en-GB",
  { day: "numeric", month: "short", year: "numeric" }) : "–";

async function getJson(path) {
  const res = await fetch(`${CFG.dataBase}/${path}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`${path}: HTTP ${res.status}`);
  return res.json();
}

function bar(score) {
  const fill = el("i");
  fill.style.width = `${score === null ? 0 : score}%`;   // set through the style object so the CSP allows it
  return el("div", { class: "bar" }, fill);
}

// ---------- Signals ----------
function renderTiles() {
  const counts = Object.fromEntries(SIGNALS.map((s) => [s, 0]));
  state.scores.forEach((k) => { counts[k.signal] = (counts[k.signal] || 0) + 1; });
  $("tiles").replaceChildren(...SIGNALS.map((s) => {
    const tile = el("button", { class: "tile", type: "button", "aria-pressed": String(state.signal === s) },
      [el("b", { text: counts[s] }), chip(s)]);
    tile.addEventListener("click", () => {
      state.signal = state.signal === s ? "" : s;
      $("fSignal").value = state.signal;
      renderTiles(); renderScores();
    });
    return tile;
  }));
}

function renderScores() {
  const q = $("search").value.trim().toLowerCase();
  const sector = $("fSector").value;
  const { key, dir } = state.sort;
  const rows = state.scores
    .filter((k) => (!state.signal || k.signal === state.signal) && (!sector || k.sector === sector)
      && (!q || k.symbol.toLowerCase().includes(q) || (k.name || "").toLowerCase().includes(q)))
    .sort((a, b) => {
      const x = key === "signal" ? SIGNALS.indexOf(a.signal) : a[key];
      const y = key === "signal" ? SIGNALS.indexOf(b.signal) : b[key];
      if (x === null || x === undefined) return 1;
      if (y === null || y === undefined) return -1;
      return (typeof x === "string" ? x.localeCompare(y) : x - y) * dir;
    });
  $("scoreTable").tBodies[0].replaceChildren(...rows.map((k) => {
    const tr = el("tr", { tabindex: "0" }, [
      el("td", {}, el("b", { text: k.symbol })), el("td", { class: "wrap hide-s", text: k.name || "" }),
      el("td", { class: "hide-s", text: k.sector || "" }), el("td", { class: "num", text: fmt(k.price) }),
      el("td", { class: "num", text: fmt(k.score, 1) }), el("td", { class: "num hide-s", text: `${fmt(k.coverage_pct, 0)}%` }),
      el("td", {}, k.red_flags && k.red_flags.length
        ? [chip(k.signal), el("span", { class: "flag", title: k.red_flags.join("; "), text: " ⚠ check" })] : chip(k.signal)),
    ]);
    const open = () => showDetail(k);
    tr.addEventListener("click", open);
    tr.addEventListener("keydown", (e) => { if (e.key === "Enter") open(); });
    return tr;
  }));
  document.querySelectorAll("#scoreTable th[data-sort]").forEach((th) => {
    if (th.dataset.sort === key) th.setAttribute("aria-sort", dir === 1 ? "ascending" : "descending");
    else th.removeAttribute("aria-sort");
  });
}

function showDetail(k) {
  $("dTitle").textContent = `${k.symbol} · ${k.name || ""}`;
  $("dMeta").replaceChildren(chip(k.signal),
    ` Score ${fmt(k.score, 1)} of 100 · data coverage ${fmt(k.coverage_pct, 0)}% · ${k.sector || ""} · Rs ${fmt(k.price)}`);
  const blocks = k.factors.map((f) => el("div", { class: "factor" }, [
    el("div", { class: "head" }, [
      el("b", { text: `${FACTOR_LABEL[f.name] || f.name} (weight ${f.weight})` }),
      el("span", { text: f.score === null ? "no data" : `${fmt(f.score, 0)} / 100` }),
    ]),
    bar(f.score),
    el("ul", {}, f.reasons.map((r) => el("li", { text: r }))),
  ]));
  const note = (state.notes || {})[k.symbol];
  if (note) {
    const list = (title, items) => (items && items.length)
      ? [el("b", { text: title }), el("ul", {}, items.map((i) => el("li", { text: i })))] : [];
    blocks.unshift(el("div", { class: "note" }, [
      el("b", { text: "Analyst note" }), el("p", { text: note.summary }),
      ...list("Strengths", note.strengths), ...list("Risks", note.risks), ...list("Check before acting", note.checks),
      el("p", { class: "muted small", text: "Written by an AI model from the figures above. It does not change the score." }),
    ]));
  }
  if (k.red_flags && k.red_flags.length) {
    blocks.unshift(el("p", { class: "error", text: `Red flags: ${k.red_flags.join("; ")}` }));
  }
  $("dFactors").replaceChildren(...blocks);
  $("detail").showModal();
}

// ---------- Portfolio (stored in this browser only) ----------
function loadHoldings() {
  try { return JSON.parse(localStorage.getItem(HOLD_KEY)) || []; } catch { return []; }
}
function saveHoldings(list) {
  try { localStorage.setItem(HOLD_KEY, JSON.stringify(list)); } catch { /* private mode: keep in memory only */ }
  state.holdings = list;
}
function validHolding(h) {
  return h && typeof h.symbol === "string" && /^[A-Z0-9]{1,12}$/.test(h.symbol)
    && Number.isFinite(h.qty) && h.qty > 0 && Number.isFinite(h.cost) && h.cost >= 0;
}
function renderHoldings() {
  const list = state.holdings;
  $("holdEmpty").hidden = list.length > 0;
  $("holdTable").tBodies[0].replaceChildren(...list.map((h, i) => {
    const k = state.bySymbol[h.symbol];
    const pl = k && k.price !== null ? (k.price - h.cost) * h.qty : null;
    const remove = el("button", { type: "button", class: "ghost", "aria-label": `Remove ${h.symbol}`, text: "Remove" });
    remove.addEventListener("click", () => { saveHoldings(list.filter((_, j) => j !== i)); renderHoldings(); });
    return el("tr", {}, [
      el("td", {}, el("b", { text: h.symbol })), el("td", { class: "num", text: fmt(h.qty, 0) }),
      el("td", { class: "num", text: fmt(h.cost) }), el("td", { class: "num", text: k ? fmt(k.price) : "–" }),
      el("td", { class: `num ${pl === null ? "" : pl >= 0 ? "gain" : "loss"}`,
        text: pl === null ? "–" : `${pl >= 0 ? "+" : ""}${fmt(pl, 0)}` }),
      el("td", { class: "num", text: k ? fmt(k.score, 1) : "–" }),
      el("td", {}, k ? chip(k.signal) : el("span", { class: "muted", text: "Not in KSE-100 data" })),
      el("td", {}, remove),
    ]);
  }));
}

// ---------- Dividends ----------
function payoutLabel(p) {
  const kind = { cash: "Cash dividend", bonus: "Bonus shares", right: "Right shares" }[p.kind] || p.kind;
  return `${kind}, ${p.stage}, ${fmt(p.percent, p.percent % 1 ? 1 : 0)}%`;
}
function renderDividends() {
  const since = new Date(Date.now() - 90 * 864e5).toISOString().slice(0, 10);
  const agent = state.agent || { upcoming: [], companies: {}, summary: {} };
  const pct = (x) => (x === null || x === undefined) ? "–" : `${fmt(100 * x, 0)}%`;
  const s = agent.summary;
  $("divSummary").textContent = s && s.events
    ? `Across ${s.events} past dividends, the price typically fell by ${pct(s.median_drop_ratio)} of the dividend on the `
      + `ex-dividend day and was back to its earlier level within 20 trading days ${pct(s.quick_recovery_share)} of the time.`
    : "";
  $("upEmpty").hidden = agent.upcoming.length > 0;
  $("upTable").tBodies[0].replaceChildren(...agent.upcoming.flatMap((u) => {
    const good = u.verdict === "WORTH_A_LOOK";
    return [el("tr", {}, [
      el("td", {}, el("b", { text: u.symbol })), el("td", { class: "num", text: fmt(u.amount_per_share) }),
      el("td", { class: "num", text: u.yield_pct === null ? "–" : `${fmt(u.yield_pct, 1)}%` }),
      el("td", { text: fmtDate(u.last_buy_date) }), el("td", { text: fmtDate(u.ex_date) }),
      el("td", { class: "num", text: u.expected_drop_rs === null ? "–" : `${fmt(u.expected_drop_rs)} (${u.expected_drop_basis})` }),
      el("td", { class: "num", text: u.median_recovery_days === null ? "–" : `${fmt(u.median_recovery_days, 0)} days` }),
      el("td", {}, u.signal ? chip(u.signal) : "–"),
      el("td", {}, el("span", { class: `chip ${good ? "BUY" : "HOLD"}`, text: good ? "Worth a look" : "Skip" })),
    ]), el("tr", { class: "why" }, el("td", { colspan: "9", class: "wrap muted small", text: u.reasons.join(" · ") }))];
  }));
  const hist = Object.entries(agent.companies).filter(([, h]) => h.events >= 2)
    .sort((a, b) => (b[1].quick_recovery_share ?? -1) - (a[1].quick_recovery_share ?? -1)
      || (a[1].median_recovery_days ?? 999) - (b[1].median_recovery_days ?? 999));
  $("histTable").tBodies[0].replaceChildren(...hist.map(([symbol, h]) => el("tr", {}, [
    el("td", {}, el("b", { text: symbol })), el("td", { class: "num", text: h.events }),
    el("td", { class: "num", text: pct(h.median_drop_ratio) }),
    el("td", { class: "num", text: h.median_recovery_days === null ? "–" : fmt(h.median_recovery_days, 0) }),
    el("td", { class: "num", text: pct(h.quick_recovery_share) }),
    el("td", { class: `num ${h.avg_capture_10d_pct === null ? "" : h.avg_capture_10d_pct >= 0 ? "gain" : "loss"}`,
      text: h.avg_capture_10d_pct === null ? "–" : `${h.avg_capture_10d_pct >= 0 ? "+" : ""}${fmt(h.avg_capture_10d_pct, 1)}%` }),
  ])));
  const recent = state.payouts.filter((p) => p.announced && p.announced >= since)
    .sort((a, b) => b.announced.localeCompare(a.announced));
  $("recentTable").tBodies[0].replaceChildren(...recent.map((p) => el("tr", {}, [
    el("td", { text: fmtDate(p.announced) }), el("td", {}, el("b", { text: p.symbol })),
    el("td", { text: payoutLabel(p) }), el("td", { class: "num", text: fmt(p.amount_per_share) }),
    el("td", { text: `${fmtDate(p.book_closure_from)} to ${fmtDate(p.book_closure_to)}` }),
  ])));
}

// ---------- Back-test ----------
function statTable(title, firstCol, rows) {
  const head = [firstCol, "Observations", "Avg return %", "Avg vs KSE-100 %", "Beat index %"];
  const table = el("table", {}, [
    el("thead", {}, el("tr", {}, head.map((h, i) => el("th", { class: i ? "num" : "", text: h })))),
    el("tbody", {}, rows.map(([name, v]) => el("tr", {}, [
      el("td", {}, SIGNAL_LABEL[name] ? chip(name) : el("span", { text: name })),
      el("td", { class: "num", text: fmt(v.n, 0) }), el("td", { class: "num", text: fmt(v.avg_return_pct, 1) }),
      el("td", { class: "num", text: `${v.avg_excess_pct >= 0 ? "+" : ""}${fmt(v.avg_excess_pct, 1)}` }),
      el("td", { class: "num", text: fmt(v.beat_index_pct, 0) }),
    ]))),
  ]);
  return [el("h2", { text: title }), el("div", { class: "tablewrap" }, table)];
}
function renderBacktest(r) {
  if (!r || !r.observations) { $("btIntro").textContent = "No back-test results yet."; return; }
  $("btIntro").textContent = `${fmt(r.observations, 0)} company-month observations from ${fmtDate(r.first_month)} to `
    + `${fmtDate(r.last_month)}; ${fmt(r.with_signal, 0)} had enough data for a signal. Indicative only: today's `
    + "KSE-100 members, a short window, and settings tuned on this same period.";
  const parts = [];
  for (const [label, h] of Object.entries(r.horizons)) {
    const months = label === "3m" ? "3 months" : "6 months";
    parts.push(...statTable(`${months} after the signal`, "Signal",
      Object.entries(h.by_signal).filter(([name]) => name !== "INSUFFICIENT_DATA")));
  }
  $("btBody").replaceChildren(...parts);
}

// ---------- Manual statement entry ----------
function renderManualForm() {
  const field = (name, label, attrs) => el("label", {}, [label, el("input", { id: `m_${name}`, ...attrs })]);
  $("manualForm").replaceChildren(
    field("symbol", "Symbol", { list: "symbolList", required: "", placeholder: "e.g. PSO" }),
    field("year", "Fiscal year", { type: "number", min: "2015", max: "2100", placeholder: "e.g. 2026" }),
    ...MANUAL_FIELDS.map((f) => field(f, f === "dividend_per_share" ? "Dividend per share (Rs)"
      : `${f.replace(/_/g, " ")} (Rs 000)`, { type: "number", step: "any" })));
  $("openFile").href = CFG.manualFileUrl;
  const build = () => {
    const symbol = $("m_symbol").value.trim().toUpperCase();
    const year = $("m_year").value.trim();
    $("rowOut").textContent = /^[A-Z0-9]{1,12}$/.test(symbol) && /^\d{4}$/.test(year)
      ? [symbol, year, ...MANUAL_FIELDS.map((f) => $(`m_${f}`).value.trim())].join(",")
      : "Enter a symbol and a four-digit fiscal year to build the row.";
  };
  $("manualForm").addEventListener("input", build);
  build();
  $("copyRow").addEventListener("click", async () => {
    try { await navigator.clipboard.writeText($("rowOut").textContent); $("copyRow").textContent = "Copied"; }
    catch { $("copyRow").textContent = "Select the row and copy it"; }
    setTimeout(() => { $("copyRow").textContent = "Copy row"; }, 2000);
  });
}

// ---------- Wiring ----------
function wire() {
  document.querySelectorAll("#tabs button").forEach((b) => b.addEventListener("click", () => {
    document.querySelectorAll("#tabs button").forEach((x) => x.setAttribute("aria-selected", String(x === b)));
    document.querySelectorAll("main > section").forEach((s) => { s.hidden = s.id !== b.dataset.tab; });
  }));
  $("search").addEventListener("input", renderScores);
  $("fSector").addEventListener("change", renderScores);
  $("fSignal").addEventListener("change", () => { state.signal = $("fSignal").value; renderTiles(); renderScores(); });
  document.querySelectorAll("#scoreTable th[data-sort]").forEach((th) => th.addEventListener("click", () => {
    const key = th.dataset.sort;
    state.sort = { key, dir: state.sort.key === key ? -state.sort.dir : (key === "score" || key === "price" ? -1 : 1) };
    renderScores();
  }));
  $("dClose").addEventListener("click", () => $("detail").close());
  $("holdForm").addEventListener("submit", (e) => {
    e.preventDefault();
    const h = { symbol: $("hSymbol").value.trim().toUpperCase(), qty: Number($("hQty").value), cost: Number($("hCost").value) };
    if (!validHolding(h)) return;
    saveHoldings([...state.holdings, h]);
    e.target.reset();
    renderHoldings();
  });
  $("exportBtn").addEventListener("click", () => {
    const url = URL.createObjectURL(new Blob([JSON.stringify(state.holdings, null, 1)], { type: "application/json" }));
    const a = el("a", { href: url, download: "betalens-holdings.json" });
    a.click();
    URL.revokeObjectURL(url);
  });
  $("importFile").addEventListener("change", async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    try {
      const list = JSON.parse(await file.text());
      if (!Array.isArray(list) || !list.every(validHolding)) throw new Error("not a holdings file");
      saveHoldings(list.map(({ symbol, qty, cost }) => ({ symbol, qty, cost })));
      renderHoldings();
    } catch (err) { showError(`Could not import holdings: ${err.message}`); }
    e.target.value = "";
  });
}
function showError(msg) { $("error").textContent = msg; $("error").hidden = false; }

async function main() {
  wire();
  state.holdings = loadHoldings().filter(validHolding);
  renderManualForm();
  try {
    const [scores, dividends] = await Promise.all([getJson("latest/scores.json"), getJson("latest/dividends.json")]);
    state.scores = scores.scores;
    state.bySymbol = Object.fromEntries(scores.scores.map((k) => [k.symbol, k]));
    state.payouts = dividends.payouts;
    const failed = Object.keys(scores.meta.errors || {}).length;
    $("updated").textContent = `Updated ${new Date(scores.meta.generated_at).toLocaleString("en-GB",
      { dateStyle: "medium", timeStyle: "short" })} · ${scores.meta.companies} companies · `
      + `${scores.meta.period_years}-year look-back${failed ? ` · ${failed} failed to load` : ""}`;
    $("fSignal").append(...SIGNALS.map((s) => el("option", { value: s, text: SIGNAL_LABEL[s] })));
    const sectors = [...new Set(scores.scores.map((k) => k.sector).filter(Boolean))].sort();
    $("fSector").append(...sectors.map((s) => el("option", { value: s, text: s })));
    $("symbolList").append(...scores.scores.map((k) => el("option", { value: k.symbol })));
    try { state.agent = await getJson("latest/dividend_agent.json"); } catch { state.agent = null; }
    try { state.notes = await getJson("latest/analyst_notes.json"); } catch { state.notes = {}; }
    renderTiles(); renderScores(); renderHoldings(); renderDividends();
  } catch (err) {
    $("updated").textContent = "Data could not be loaded.";
    showError(`Could not load the latest scores (${err.message}). Check that the daily job ran.`);
  }
  try { renderBacktest(await getJson("backtest/report.json")); }
  catch { $("btIntro").textContent = "Back-test results could not be loaded."; }
}
main();
