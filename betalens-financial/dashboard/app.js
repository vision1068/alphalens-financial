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
  price_to_book: "Price to book", asset_quality: "Asset quality", capital_adequacy: "Capital adequacy",
};
const MANUAL_FIELDS = ["equity", "total_debt", "ebit", "interest_expense", "operating_cash_flow", "capex",
  "current_assets", "current_liabilities", "receivables", "inventory", "payables", "cost_of_sales",
  "dividend_per_share", "npl_ratio_pct", "capital_adequacy_pct"];
const MANUAL_LABEL = { dividend_per_share: "Dividend per share (Rs)", npl_ratio_pct: "Banks: non-performing loans (% of advances)",
  capital_adequacy_pct: "Banks: capital adequacy ratio (%)" };

const MARKETS = {
  psx: {
    name: "PSX", currency: "Rs", benchmark: "KSE-100", companies: "Shariah-compliant companies",
    files: { scores: "latest/scores.json", agent: "latest/dividend_agent.json", live: "latest/live.json",
      notes: "latest/analyst_notes.json", payouts: "latest/dividends.json", backtest: "backtest/report.json" },
    required: true,
    divKey: (u) => `${u.symbol}|${u.book_closure_from}`,
    weekEmpty: "No Shariah-compliant company has a last buying day in the next 7 days.",
    divNote: "Shariah-compliant companies only. New announcements appear within 30 minutes during PSX hours; the expected "
      + "drop, recovery record and verdict are added by the daily analysis at 09:30 Pakistan time. ≈ means the amount "
      + "assumes the usual Rs 10 face value. Amounts are before tax; tax is deducted at source. Dates assume no public "
      + "holiday in between, so check the company's notice.",
  },
  us: {
    name: "US (S&P 500)", currency: "$", benchmark: "S&P 500 (SPY)", companies: "S&P 500 companies",
    files: { scores: "latest/us_scores.json", agent: "latest/us_dividend_agent.json", live: "latest/us_live.json",
      backtest: "backtest_us/report.json" },
    required: false,
    divKey: (u) => `${u.symbol}|${u.ex_date}`,
    weekEmpty: "No S&P 500 company has a last buying day in the next 7 days.",
    divNote: "S&P 500 companies. Prices and dividends going ex in the next week refresh every 30 minutes during US "
      + "trading hours; the verdict is added by the daily analysis at 09:30 Pakistan time. In the US you must buy by "
      + "the close of the trading day before the ex-dividend day. Amounts are before US withholding tax. Dates assume "
      + "no market holiday in between.",
  },
};

const $ = (id) => document.getElementById(id);
const state = Object.fromEntries(Object.keys(MARKETS).map((m) => [m, {
  scores: [], bySymbol: {}, payouts: [], live: null, agent: null, notes: {}, sort: { key: "score", dir: -1 },
  signal: "", meta: null, loaded: false,
}]));

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
const timeFmt = (iso) => new Date(iso).toLocaleString("en-GB", { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" });

async function getJson(path) {
  // The query string stops GitHub's 5-minute cache from serving an older copy.
  const res = await fetch(`${CFG.dataBase}/${path}?t=${Date.now()}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`${path}: HTTP ${res.status}`);
  return res.json();
}

function bar(score) {
  const fill = el("i");
  fill.style.width = `${score === null ? 0 : score}%`;   // set through the style object so the CSP allows it
  return el("div", { class: "bar" }, fill);
}

// ---------- Section skeletons (one set per market) ----------
function buildSignalsSection(m) {
  const id = (x) => `${m}-${x}`;
  const head = [["symbol", "Symbol", ""], ["name", "Company", "hide-s"], ["sector", "Sector", "hide-s"],
    ["price_now", `Price (${MARKETS[m].currency})`, "num"], ["change_pct", "Today", "num"], ["score", "Score", "num"],
    ["coverage_pct", "Data", "num hide-s"], ["signal", "Signal", ""]];
  $(id("signals")).replaceChildren(
    el("p", { id: id("status"), class: "muted", text: "Loading…" }),
    el("div", { id: id("tiles"), class: "tiles" }),
    el("div", { class: "controls" }, [
      el("input", { id: id("search"), type: "search", placeholder: "Search symbol or company", "aria-label": "Search symbol or company" }),
      el("select", { id: id("fSignal"), "aria-label": "Filter by signal" }, el("option", { value: "", text: "All signals" })),
      el("select", { id: id("fSector"), "aria-label": "Filter by sector" }, el("option", { value: "", text: "All sectors" })),
    ]),
    el("div", { class: "tablewrap" }, el("table", { id: id("scoreTable"), class: "scoreTable" }, [
      el("thead", {}, el("tr", {}, head.map(([key, text, cls]) => el("th", { "data-sort": key, class: cls, text })))),
      el("tbody"),
    ])),
    el("p", { class: "muted small", text: "Score is out of 100. “Data” is the share of the scorecard's weight that had "
      + "figures; signals need at least 60%. Click a company for each factor's mark and reasons." }),
  );
  $(id("search")).addEventListener("input", () => renderScores(m));
  $(id("fSector")).addEventListener("change", () => renderScores(m));
  $(id("fSignal")).addEventListener("change", () => { state[m].signal = $(id("fSignal")).value; renderTiles(m); renderScores(m); });
  $(id("scoreTable")).querySelectorAll("th[data-sort]").forEach((th) => th.addEventListener("click", () => {
    const key = th.dataset.sort;
    const s = state[m].sort;
    state[m].sort = { key, dir: s.key === key ? -s.dir : (["score", "price_now", "change_pct", "coverage_pct"].includes(key) ? -1 : 1) };
    renderScores(m);
  }));
}

function buildDividendsSection(m) {
  const id = (x) => `${m}-${x}`;
  const cur = MARKETS[m].currency;
  const head = () => el("thead", {}, el("tr", {}, [["Symbol", ""], [`Per share (${cur})`, "num"], ["Yield", "num"],
    ["Last day to buy", ""], ["Ex-dividend day", ""], [`Expected drop (${cur})`, "num"], ["Usual recovery", "num"],
    ["Signal", ""], ["Verdict", ""]].map(([text, cls]) => el("th", { class: cls, text }))));
  const parts = [
    el("h2", { id: id("weekTitle"), text: "Last day to buy in the next 7 days" }),
    el("p", { id: id("divSummary"), class: "muted" }),
    el("div", { class: "tablewrap" }, el("table", { id: id("weekTable") }, [head(), el("tbody")])),
    el("p", { id: id("weekEmpty"), class: "muted", hidden: "", text: MARKETS[m].weekEmpty }),
    el("h2", { text: "Later dividends" }),
    el("div", { class: "tablewrap" }, el("table", { id: id("laterTable") }, [head(), el("tbody")])),
    el("p", { id: id("laterEmpty"), class: "muted", hidden: "", text: "No later cash dividends announced yet." }),
    el("p", { class: "muted small", text: `${MARKETS[m].divNote} “Worth a look” needs a Buy signal and a record of quick `
      + "price recovery after past dividends." }),
    el("h2", { text: "How prices behaved after past dividends" }),
    el("div", { class: "tablewrap" }, el("table", { id: id("histTable") }, [
      el("thead", {}, el("tr", {}, [["Symbol", ""], ["Past dividends", "num"], ["Drop as % of dividend", "num"],
        ["Median days to recover", "num"], ["Recovered in 20 days", "num"], ["10-day result incl. dividend", "num"]]
        .map(([text, cls]) => el("th", { class: cls, text })))),
      el("tbody"),
    ])),
  ];
  if (m === "psx") {
    parts.push(el("h2", { text: "Announced in the last 90 days" }),
      el("div", { class: "tablewrap" }, el("table", { id: id("recentTable") }, [
        el("thead", {}, el("tr", {}, [["Announced", ""], ["Symbol", ""], ["Payout", ""], ["Per share (Rs)", "num"],
          ["Books close", ""]].map(([text, cls]) => el("th", { class: cls, text })))),
        el("tbody"),
      ])));
  }
  $(id("dividends")).replaceChildren(...parts);
}

// ---------- Signals ----------
function renderTiles(m) {
  const st = state[m];
  const counts = Object.fromEntries(SIGNALS.map((s) => [s, 0]));
  st.scores.forEach((k) => { counts[k.signal] = (counts[k.signal] || 0) + 1; });
  $(`${m}-tiles`).replaceChildren(...SIGNALS.map((s) => {
    const tile = el("button", { class: "tile", type: "button", "aria-pressed": String(st.signal === s) },
      [el("b", { text: counts[s] }), chip(s)]);
    tile.addEventListener("click", () => {
      st.signal = st.signal === s ? "" : s;
      $(`${m}-fSignal`).value = st.signal;
      renderTiles(m); renderScores(m);
    });
    return tile;
  }));
}

function renderScores(m) {
  const st = state[m];
  const q = $(`${m}-search`).value.trim().toLowerCase();
  const sector = $(`${m}-fSector`).value;
  const { key, dir } = st.sort;
  const rows = st.scores
    .filter((k) => (!st.signal || k.signal === st.signal) && (!sector || k.sector === sector)
      && (!q || k.symbol.toLowerCase().includes(q) || (k.name || "").toLowerCase().includes(q)))
    .sort((a, b) => {
      const x = key === "signal" ? SIGNALS.indexOf(a.signal) : a[key];
      const y = key === "signal" ? SIGNALS.indexOf(b.signal) : b[key];
      if (x === null || x === undefined) return 1;
      if (y === null || y === undefined) return -1;
      return (typeof x === "string" ? x.localeCompare(y) : x - y) * dir;
    });
  const table = $(`${m}-scoreTable`);
  table.tBodies[0].replaceChildren(...rows.map((k) => {
    const tr = el("tr", { tabindex: "0" }, [
      el("td", {}, el("b", { text: k.symbol })), el("td", { class: "wrap hide-s", text: k.name || "" }),
      el("td", { class: "hide-s", text: k.sector || "" }), el("td", { class: "num", text: fmt(k.price_now) }),
      el("td", { class: `num ${k.change_pct > 0 ? "gain" : k.change_pct < 0 ? "loss" : ""}`,
        text: k.change_pct === null || k.change_pct === undefined ? "–" : `${k.change_pct > 0 ? "+" : ""}${fmt(k.change_pct, 2)}%` }),
      el("td", { class: "num", text: fmt(k.score, 1) }), el("td", { class: "num hide-s", text: `${fmt(k.coverage_pct, 0)}%` }),
      el("td", {}, k.red_flags && k.red_flags.length
        ? [chip(k.signal), el("span", { class: "flag", title: k.red_flags.join("; "), text: " ⚠ check" })] : chip(k.signal)),
    ]);
    const open = () => showDetail(m, k);
    tr.addEventListener("click", open);
    tr.addEventListener("keydown", (e) => { if (e.key === "Enter") open(); });
    return tr;
  }));
  table.querySelectorAll("th[data-sort]").forEach((th) => {
    if (th.dataset.sort === key) th.setAttribute("aria-sort", dir === 1 ? "ascending" : "descending");
    else th.removeAttribute("aria-sort");
  });
}

function showDetail(m, k) {
  $("dTitle").textContent = `${k.symbol} · ${k.name || ""}`;
  $("dMeta").replaceChildren(chip(k.signal),
    ` Score ${fmt(k.score, 1)} of 100 · data coverage ${fmt(k.coverage_pct, 0)}% · ${k.sector || ""} · `
    + `${MARKETS[m].currency} ${fmt(k.price_now)}`
    + (k.in_base_index === false ? " · outside KSE-100, included for its upcoming dividend" : ""));
  const blocks = k.factors.map((f) => el("div", { class: "factor" }, [
    el("div", { class: "head" }, [
      el("b", { text: `${FACTOR_LABEL[f.name] || f.name} (weight ${f.weight})` }),
      el("span", { text: f.score === null ? "no data" : `${fmt(f.score, 0)} / 100` }),
    ]),
    bar(f.score),
    el("ul", {}, f.reasons.map((r) => el("li", { text: r }))),
  ]));
  const note = (state[m].notes || {})[k.symbol];
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

// ---------- Dividends ----------
function payoutLabel(p) {
  const kind = { cash: "Cash dividend", bonus: "Bonus shares", right: "Right shares" }[p.kind] || p.kind;
  return `${kind}, ${p.stage}, ${fmt(p.percent, p.percent % 1 ? 1 : 0)}%`;
}

function dividendRows(m) {
  // Fresh dividends come from the 30-minute live feed; the daily dividend agent adds its assessment.
  const st = state[m];
  const agent = st.agent || { upcoming: [] };
  const key = MARKETS[m].divKey;
  const assessed = Object.fromEntries(agent.upcoming.map((u) => [key(u), u]));
  const live = (st.live && st.live.upcoming) || [];
  const rows = live.map((u) => {
    const a = assessed[key(u)];
    const k = st.bySymbol[u.symbol] || {};
    return a ? { ...a, ...u, verdict: a.verdict, reasons: a.reasons }
      : { ...u, signal: k.signal, score: k.score, expected_drop_rs: null, median_recovery_days: null, verdict: "PENDING",
          reasons: ["Not assessed yet: the daily analysis at 09:30 Pakistan time adds the verdict"] };
  });
  const liveKeys = new Set(live.map(key));
  agent.upcoming.filter((u) => !liveKeys.has(key(u))).forEach((u) => rows.push(u));
  return rows.sort((a, b) => String(a.last_buy_date).localeCompare(String(b.last_buy_date)) || a.symbol.localeCompare(b.symbol));
}

function dividendTableRows(list) {
  const verdictChip = (v) => {
    const map = { WORTH_A_LOOK: ["BUY", "Worth a look"], SKIP: ["HOLD", "Skip"], PENDING: ["INSUFFICIENT_DATA", "Pending analysis"] };
    const [cls, text] = map[v] || ["HOLD", v];
    return el("span", { class: `chip ${cls}`, text });
  };
  return list.flatMap((u) => {
    const approx = u.face_value_assumed ? "≈" : "";
    const perShare = el("td", { class: "num", text: u.amount_per_share === null ? "–" : `${approx}${fmt(u.amount_per_share)}` });
    if (approx) perShare.title = "Assumes the usual Rs 10 face value; check the company's notice";
    return [el("tr", {}, [
      el("td", {}, el("b", { text: u.symbol })), perShare,
      el("td", { class: "num", text: u.yield_pct === null || u.yield_pct === undefined ? "–" : `${approx}${fmt(u.yield_pct, 1)}%` }),
      el("td", { text: fmtDate(u.last_buy_date) }), el("td", { text: fmtDate(u.ex_date) }),
      el("td", { class: "num", text: u.expected_drop_rs === null || u.expected_drop_rs === undefined ? "–"
        : `${fmt(u.expected_drop_rs)} (${u.expected_drop_basis})` }),
      el("td", { class: "num", text: u.median_recovery_days === null || u.median_recovery_days === undefined ? "–"
        : `${fmt(u.median_recovery_days, 0)} days` }),
      el("td", {}, u.signal ? chip(u.signal) : "–"), el("td", {}, verdictChip(u.verdict)),
    ]), el("tr", { class: "why" }, el("td", { colspan: "9", class: "wrap muted small", text: (u.reasons || []).join(" · ") }))];
  });
}

function renderDividends(m) {
  const st = state[m];
  const id = (x) => `${m}-${x}`;
  const agent = st.agent || { upcoming: [], companies: {}, summary: {} };
  const pct = (x) => (x === null || x === undefined) ? "–" : `${fmt(100 * x, 0)}%`;
  const s = agent.summary;
  $(id("divSummary")).textContent = s && s.events
    ? `Across ${s.events} past dividends, the price typically fell by ${pct(s.median_drop_ratio)} of the dividend on the `
      + `ex-dividend day and was back to its earlier level within 20 trading days ${pct(s.quick_recovery_share)} of the time.`
    : "";
  const localIso = (d) => new Date(d.getTime() - d.getTimezoneOffset() * 6e4).toISOString().slice(0, 10);
  const today = new Date();
  const first = localIso(today);
  const last = localIso(new Date(today.getFullYear(), today.getMonth(), today.getDate() + 6));
  $(id("weekTitle")).textContent = `Last day to buy in the next 7 days (${fmtDate(first)} to ${fmtDate(last)})`;
  const rows = dividendRows(m).filter((u) => String(u.last_buy_date) >= first);
  const week = rows.filter((u) => String(u.last_buy_date) <= last);
  const later = rows.filter((u) => String(u.last_buy_date) > last);
  $(id("weekEmpty")).hidden = week.length > 0;
  $(id("laterEmpty")).hidden = later.length > 0;
  $(id("weekTable")).tBodies[0].replaceChildren(...dividendTableRows(week));
  $(id("laterTable")).tBodies[0].replaceChildren(...dividendTableRows(later));
  const hist = Object.entries(agent.companies || {}).filter(([, h]) => h.events >= 2)
    .sort((a, b) => (b[1].quick_recovery_share ?? -1) - (a[1].quick_recovery_share ?? -1)
      || (a[1].median_recovery_days ?? 999) - (b[1].median_recovery_days ?? 999));
  $(id("histTable")).tBodies[0].replaceChildren(...hist.map(([symbol, h]) => el("tr", {}, [
    el("td", {}, el("b", { text: symbol })), el("td", { class: "num", text: h.events }),
    el("td", { class: "num", text: h.median_drop_ratio === null ? "–" : h.median_drop_ratio > 1.5 ? "over 150% (noisy)"
      : h.median_drop_ratio < 0 ? "rose instead" : pct(h.median_drop_ratio) }),
    el("td", { class: "num", text: h.median_recovery_days === null ? "–" : fmt(h.median_recovery_days, 0) }),
    el("td", { class: "num", text: pct(h.quick_recovery_share) }),
    el("td", { class: `num ${h.avg_capture_10d_pct === null ? "" : h.avg_capture_10d_pct >= 0 ? "gain" : "loss"}`,
      text: h.avg_capture_10d_pct === null ? "–" : `${h.avg_capture_10d_pct >= 0 ? "+" : ""}${fmt(h.avg_capture_10d_pct, 1)}%` }),
  ])));
  if (m === "psx") {
    const since = new Date(Date.now() - 90 * 864e5).toISOString().slice(0, 10);
    const recent = st.payouts.filter((p) => p.announced && p.announced >= since)
      .sort((a, b) => b.announced.localeCompare(a.announced));
    $(id("recentTable")).tBodies[0].replaceChildren(...recent.map((p) => el("tr", {}, [
      el("td", { text: fmtDate(p.announced) }), el("td", {}, el("b", { text: p.symbol })),
      el("td", { text: payoutLabel(p) }), el("td", { class: "num", text: fmt(p.amount_per_share) }),
      el("td", { text: `${fmtDate(p.book_closure_from)} to ${fmtDate(p.book_closure_to)}` }),
    ])));
  }
}

// ---------- Back-test ----------
function statTable(title, benchmark, rows) {
  const head = ["Signal", "Observations", "Avg return %", `Avg vs ${benchmark} %`, "Beat index %"];
  const table = el("table", {}, [
    el("thead", {}, el("tr", {}, head.map((h, i) => el("th", { class: i ? "num" : "", text: h })))),
    el("tbody", {}, rows.map(([name, v]) => el("tr", {}, [
      el("td", {}, chip(name)),
      el("td", { class: "num", text: fmt(v.n, 0) }), el("td", { class: "num", text: fmt(v.avg_return_pct, 1) }),
      el("td", { class: "num", text: `${v.avg_excess_pct >= 0 ? "+" : ""}${fmt(v.avg_excess_pct, 1)}` }),
      el("td", { class: "num", text: fmt(v.beat_index_pct, 0) }),
    ]))),
  ]);
  return [el("h3", { text: title }), el("div", { class: "tablewrap" }, table)];
}

function renderBacktest(m, r) {
  const box = $(m === "psx" ? "btPsx" : "btUs");
  const mk = MARKETS[m];
  if (!r || !r.observations) {
    box.replaceChildren(el("h2", { text: mk.name }), el("p", { class: "muted", text: "No back-test results yet." }));
    return;
  }
  const parts = [el("h2", { text: mk.name }), el("p", { class: "muted", text:
    `${fmt(r.observations, 0)} company-month observations from ${fmtDate(r.first_month)} to ${fmtDate(r.last_month)}; `
    + `${fmt(r.with_signal, 0)} had enough data for a signal. Indicative only: today's index members, and settings tuned on this same period.` })];
  for (const [label, h] of Object.entries(r.horizons)) {
    const months = label === "3m" ? "3 months" : "6 months";
    parts.push(...statTable(`${months} after the signal`, mk.benchmark,
      Object.entries(h.by_signal).filter(([name]) => name !== "INSUFFICIENT_DATA")));
  }
  box.replaceChildren(...parts);
}

// ---------- Manual statement entry (PSX) ----------
function renderManualForm() {
  const field = (name, label, attrs) => el("label", {}, [label, el("input", { id: `m_${name}`, ...attrs })]);
  $("manualForm").replaceChildren(
    field("symbol", "Symbol", { list: "symbolList", required: "", placeholder: "e.g. PSO" }),
    field("year", "Fiscal year", { type: "number", min: "2015", max: "2100", placeholder: "e.g. 2026" }),
    ...MANUAL_FIELDS.map((f) => field(f, MANUAL_LABEL[f] || `${f.replace(/_/g, " ")} (Rs 000)`,
      { type: "number", step: "any" })));
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

// ---------- Loading ----------
function showError(msg) { $("error").textContent = msg; $("error").hidden = false; }

function fillSelect(id, values, labels) {
  const sel = $(id);
  const keep = sel.value;
  sel.replaceChildren(sel.options[0], ...values.map((v) => el("option", { value: v, text: labels ? labels[v] : v })));
  sel.value = values.includes(keep) ? keep : "";
}

async function loadMarket(m) {
  const f = MARKETS[m].files;
  const opt = (path) => (path ? getJson(path).catch(() => null) : Promise.resolve(null));
  const scores = await getJson(f.scores);
  const [live, agent, notes, payouts, backtest] = await Promise.all([opt(f.live), opt(f.agent), opt(f.notes),
    opt(f.payouts), opt(f.backtest)]);
  const st = state[m];
  const prices = (live && live.prices) || {};
  st.scores = scores.scores.map((k) => {
    const p = prices[k.symbol];
    return { ...k, price_now: p && p.price !== null ? p.price : k.price,
      change_pct: p && p.change_pct !== undefined ? p.change_pct : (k.change_pct ?? null) };
  });
  st.bySymbol = Object.fromEntries(st.scores.map((k) => [k.symbol, k]));
  st.live = live;
  st.agent = agent;
  st.notes = notes || {};
  st.payouts = (payouts && payouts.payouts) || [];
  st.meta = scores.meta;
  st.loaded = true;
  const failed = Object.keys(scores.meta.errors || {}).length;
  $(`${m}-status`).textContent = `${scores.meta.companies} ${MARKETS[m].companies} · analysis ${timeFmt(scores.meta.generated_at)}`
    + (live ? ` · prices ${timeFmt(live.as_of)}${live.market_status ? ` (${live.market_status.toLowerCase()})` : ""}` : "") + ` · ${scores.meta.period_years}-year look-back`
    + (failed ? ` · ${failed} with data problems` : "");
  fillSelect(`${m}-fSignal`, SIGNALS, SIGNAL_LABEL);
  fillSelect(`${m}-fSector`, [...new Set(st.scores.map((k) => k.sector).filter(Boolean))].sort());
  if (m === "psx") $("symbolList").replaceChildren(...st.scores.map((k) => el("option", { value: k.symbol })));
  renderTiles(m); renderScores(m); renderDividends(m);
  renderBacktest(m, backtest);
}

let refreshing = false;
async function refresh() {
  if (refreshing) return;
  refreshing = true;
  const btn = $("refreshBtn");
  btn.className = "refresh busy";
  btn.textContent = "Refreshing…";
  btn.disabled = true;
  const results = await Promise.allSettled(Object.keys(MARKETS).map((m) => loadMarket(m)));
  const failed = Object.keys(MARKETS).filter((m, i) => results[i].status === "rejected");
  const time = new Date().toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" });
  if (!failed.length) {
    btn.className = "refresh ok";
    btn.textContent = `✓ Data refreshed ${time}`;
    $("error").hidden = true;
  } else {
    btn.className = "refresh fail";
    btn.textContent = `${failed.map((m) => MARKETS[m].name).join(" and ")} failed to refresh, tap to retry`;
    failed.forEach((m) => {
      if (!state[m].loaded) $(`${m}-status`).textContent = "This data could not be loaded yet.";
    });
  }
  const parts = Object.keys(MARKETS).filter((m) => state[m].meta)
    .map((m) => `${MARKETS[m].name}: ${timeFmt(state[m].meta.generated_at)}`);
  $("updated").textContent = parts.length ? `Daily analysis · ${parts.join(" · ")}` : "Data could not be loaded.";
  btn.disabled = false;
  refreshing = false;
}

function wire() {
  document.querySelectorAll("#tabs button").forEach((b) => b.addEventListener("click", () => {
    document.querySelectorAll("#tabs button").forEach((x) => x.setAttribute("aria-selected", String(x === b)));
    document.querySelectorAll("main > section").forEach((s) => { s.hidden = s.id !== b.dataset.tab; });
  }));
  $("dClose").addEventListener("click", () => $("detail").close());
  $("refreshBtn").addEventListener("click", refresh);
}

function main() {
  Object.keys(MARKETS).forEach((m) => { buildSignalsSection(m); buildDividendsSection(m); });
  wire();
  renderManualForm();
  refresh();
  setInterval(refresh, 10 * 60 * 1000);   // pick up the 30-minute price updates while the page stays open
}
main();
