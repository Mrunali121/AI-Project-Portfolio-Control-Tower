(function () {
  "use strict";
  const D = window.PORTFOLIO;
  const $ = (id) => document.getElementById(id);
  const ICON = { Green: "✓", Amber: "!", Red: "▲" };
  const fmtEur = (x) => (Math.abs(x) >= 1e6 ? "€" + (x / 1e6).toFixed(2) + "M" : "€" + Math.round(x / 1000) + "k");
  const dateStr = (iso) => new Date(iso + "T00:00:00").toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const rag = (r) => `<span class="rag"><span class="ic ${r}" aria-hidden="true">${ICON[r]}</span>${r}</span>`;

  let sortKey = "health_score", sortDir = 1, ragFilter = "All", dept = "All";
  let selected = (location.hash || "").slice(1) || null;
  const byId = Object.fromEntries(D.projects.map((p) => [p.project_id, p]));
  if (!byId[selected]) selected = D.projects.slice().sort((a, b) => a.health_score - b.health_score)[0].project_id;

  // ---------- KPIs ----------
  function renderKpis() {
    const s = D.summary;
    $("asof").textContent = dateStr(s.as_of);
    const k = [
      ["hero", "Avg health score", Math.round(s.avg_health_score), "weighted by budget, out of 100"],
      ["rags", "Status", ["Red", "Amber", "Green"].map((c) => `<span class="rag" aria-label="${s.rag_counts[c]} ${c}"><span class="ic ${c}" aria-hidden="true">${ICON[c]}</span>${s.rag_counts[c]}</span>`).join(" "), "Red, Amber, Green projects"],
      ["", "Forecast overrun", fmtEur(s.forecast_overrun_eur), `${s.forecast_overrun_pct.toFixed(1)}% over ${fmtEur(s.total_budget_eur)} budget`],
      ["", "Portfolio SPI / CPI", `${s.portfolio_spi.toFixed(2)} / ${s.portfolio_cpi.toFixed(2)}`, "below 1.00 = behind schedule / over cost"],
      ["", "Need escalation", s.escalations, "meet the escalation rules"],
      ["", "Over-allocated people", s.overallocated_people, `above 110%; ${s.stretched_people} more above 100%`],
    ];
    $("kpis").innerHTML = k.map((x) => `<div class="kpi ${x[0]}"><div class="l">${x[1]}</div><div class="v">${x[2]}</div><div class="s">${x[3]}</div></div>`).join("");
  }

  // ---------- filters + table ----------
  function renderFilters() {
    $("chips").innerHTML = ["All", "Red", "Amber", "Green"].map((c) => `<button class="chip" type="button" data-c="${c}" aria-pressed="${c === ragFilter}">${c}</button>`).join("");
    $("chips").querySelectorAll("button").forEach((b) => b.addEventListener("click", () => { ragFilter = b.dataset.c; renderFilters(); renderTable(); }));
    const depts = ["All", ...[...new Set(D.projects.map((p) => p.department))].sort()];
    $("dept").innerHTML = depts.map((d) => `<option>${d}</option>`).join("");
    $("dept").value = dept;
  }
  $("dept").addEventListener("change", (e) => { dept = e.target.value; renderTable(); });

  function renderTable() {
    const order = { Red: 0, Amber: 1, Green: 2 };
    const rows = D.projects.filter((p) => (ragFilter === "All" || p.rag === ragFilter) && (dept === "All" || p.department === dept))
      .sort((a, b) => {
        const x = sortKey === "rag" ? order[a.rag] : a[sortKey], y = sortKey === "rag" ? order[b.rag] : b[sortKey];
        return (x > y ? 1 : x < y ? -1 : 0) * sortDir;
      });
    document.querySelectorAll("#tbl th").forEach((th) => {
      if (th.dataset.k === sortKey) th.setAttribute("aria-sort", sortDir === 1 ? "ascending" : "descending"); else th.removeAttribute("aria-sort");
    });
    $("tbl").querySelector("tbody").innerHTML = rows.map((p) => `
      <tr tabindex="0" data-id="${p.project_id}" class="${p.project_id === selected ? "sel" : ""}" aria-label="${esc(p.name)}, ${p.rag}, health ${p.health_score}">
        <td>${p.project_id}</td><td>${esc(p.name)}</td><td>${esc(p.department)}</td><td>${rag(p.rag)}</td>
        <td>${p.health_score}<span class="hbar" aria-hidden="true"><i style="width:${p.health_score}%"></i></span></td>
        <td class="${p.spi < 0.8 ? "neg" : ""}">${p.spi.toFixed(2)}</td><td class="${p.cpi < 0.85 ? "neg" : ""}">${p.cpi.toFixed(2)}</td>
        <td class="${p.slip_days > 30 ? "neg" : ""}">${p.slip_days}</td>
        <td class="${p.forecast_overrun_pct > 10 ? "neg" : ""}">${p.forecast_overrun_pct > 0 ? "+" : ""}${p.forecast_overrun_pct.toFixed(1)}%</td></tr>`).join("")
      || `<tr><td colspan="9">No projects match the filters.</td></tr>`;
    $("tbl").querySelectorAll("tbody tr[data-id]").forEach((tr) => {
      const pick = () => { selected = tr.dataset.id; history.replaceState(null, "", "#" + selected); renderTable(); renderDetail(); };
      tr.addEventListener("click", pick);
      tr.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pick(); } });
    });
  }
  document.querySelectorAll("#tbl th").forEach((th) => th.addEventListener("click", () => {
    sortDir = sortKey === th.dataset.k ? -sortDir : 1; sortKey = th.dataset.k; renderTable();
  }));

  // ---------- detail ----------
  function trendSvg(tr) {
    const W = 460, H = 190, L = 34, R = 56, T = 12, B = 26;
    const vals = tr.flatMap((t) => [t.spi, t.cpi]).filter((v) => v != null);
    const lo = Math.min(0.5, Math.floor(Math.min(...vals) * 10) / 10), hi = Math.max(1.2, Math.ceil(Math.max(...vals) * 10) / 10);
    const x = (i) => L + (i / Math.max(tr.length - 1, 1)) * (W - L - R), y = (v) => T + (1 - (v - lo) / (hi - lo)) * (H - T - B);
    const line = (k) => tr.map((t, i) => (t[k] == null ? null : `${x(i).toFixed(1)},${y(t[k]).toFixed(1)}`)).filter(Boolean).join(" ");
    const last = tr[tr.length - 1];
    const grid = [lo, 0.8, 1.0, hi].filter((v, i, a) => a.indexOf(v) === i).map((v) => `<line x1="${L}" x2="${W - R}" y1="${y(v)}" y2="${y(v)}" stroke="var(--line)" ${v === 1 ? 'stroke-dasharray="3 3" stroke-opacity="1"' : ""}/><text x="${L - 4}" y="${y(v) + 4}" text-anchor="end">${v.toFixed(1)}</text>`).join("");
    const xl = tr.map((t, i) => (i % Math.ceil(tr.length / 6) === 0 || i === tr.length - 1) ? `<text x="${x(i)}" y="${H - 8}" text-anchor="middle">${t.m.slice(5)}/${t.m.slice(2, 4)}</text>` : "").join("");
    const dots = tr.map((t, i) => `<g data-tip="${t.m}: SPI ${t.spi ?? "n/a"}, CPI ${t.cpi ?? "n/a"}"><rect x="${x(i) - 10}" y="${T}" width="20" height="${H - T - B}" fill="transparent"/>` +
      (t.spi != null ? `<circle cx="${x(i)}" cy="${y(t.spi)}" r="3.5" fill="var(--accent)" stroke="var(--surface)" stroke-width="2"/>` : "") +
      (t.cpi != null ? `<circle cx="${x(i)}" cy="${y(t.cpi)}" r="3.5" fill="var(--series2)" stroke="var(--surface)" stroke-width="2"/>` : "") + `</g>`).join("");
    return `<svg viewBox="0 0 ${W} ${H}" width="100%" role="img" aria-label="SPI and CPI by month. Latest SPI ${last.spi}, CPI ${last.cpi}.">
      ${grid}${xl}
      <polyline fill="none" stroke="var(--accent)" stroke-width="2" points="${line("spi")}"/>
      <polyline fill="none" stroke="var(--series2)" stroke-width="2" stroke-dasharray="6 3" points="${line("cpi")}"/>
      ${dots}
      <text x="${x(tr.length - 1) + 8}" y="${y(last.spi) + (last.spi >= last.cpi ? -2 : 12)}">SPI ${last.spi}</text>
      <text x="${x(tr.length - 1) + 8}" y="${y(last.cpi) + (last.cpi > last.spi ? -2 : 12)}">CPI ${last.cpi}</text></svg>`;
  }

  function renderDetail() {
    const p = byId[selected];
    const items = D.raid.filter((r) => r.project_id === p.project_id && r.status !== "Closed").sort((a, b) => (b.score || 0) - (a.score || 0)).slice(0, 5);
    const names = { schedule: "Schedule (30%)", cost: "Cost (30%)", risk: "Risk (15%)", issues: "Issues (15%)", resources: "Resources (10%)" };
    $("detail").innerHTML = `
      <div class="d-head"><h2 id="d-h">${p.project_id} · ${esc(p.name)}</h2><span>${rag(p.rag)} · health ${p.health_score}/100</span></div>
      <p class="hint">${esc(p.department)} · PM ${esc(p.manager)} · sponsor ${esc(p.sponsor)} · ${esc(p.methodology)}</p>
      ${p.escalate ? `<div class="reasons" aria-label="Escalation reasons">${p.escalation_reasons.map((r) => `<span class="reason">${esc(r)}</span>`).join("")}</div>` : ""}
      <div class="d-grid"><div>
        <p class="d-sum">${esc(p.summary)}</p>
        <h3>Recommended actions</h3><ul class="recs">${p.recommendations.map((r) => `<li>${esc(r)}</li>`).join("") || "<li>No action needed; continue monitoring.</li>"}</ul>
        <h3>Top open RAID items</h3><ul class="raid-list">${items.map((r) => `<li><span class="tag">${r.type}</span><strong>${esc(r.title)}</strong> · score ${r.score ?? "-"} · ${esc(r.owner)} · ${r.status}</li>`).join("") || "<li>None open.</li>"}</ul>
      </div><div>
        <h3>SPI and CPI by month</h3>
        <div class="legend"><span><i class="sw" style="border-color:var(--accent)"></i>SPI (schedule)</span><span><i class="sw cpi" style="border-color:var(--series2)"></i>CPI (cost)</span></div>
        ${trendSvg(p.trend)}
        <h3>Health score breakdown</h3>
        ${Object.keys(names).map((k) => `<div class="score-row"><span>${names[k]}</span><div class="track" role="img" aria-label="${names[k]} score ${p.scores[k]} of 100"><i style="width:${p.scores[k]}%"></i></div><b>${p.scores[k]}</b></div>`).join("")}
        <p class="hint">Budget ${fmtEur(p.budget_eur)} · spent ${fmtEur(p.actual_cost_eur)} · forecast ${fmtEur(p.forecast_cost_eur)}</p>
      </div></div>`;
  }

  // ---------- bar charts ----------
  function divergingRows(el, items, fmt, signedUp) {
    const max = Math.max(...items.map((i) => Math.abs(i.v)), 1), neg = Math.min(...items.map((i) => i.v)) < 0;
    const zero = neg ? 30 : 0;
    el.style.setProperty("--zero", zero + "%");
    el.innerHTML = items.map((i) => {
      const w = (Math.abs(i.v) / max) * (neg ? 70 : 100) * (neg && i.v < 0 ? 30 / 70 : 1);
      const bar = i.v >= 0 ? `left:${zero}%;width:${(Math.abs(i.v) / max) * (100 - zero)}%` : `right:${100 - zero}%;width:${(Math.abs(i.v) / max) * zero}%`;
      return `<li class="brow" data-tip="${esc(i.tip)}"><span>${esc(i.label)}</span><div class="btrack" style="--zero:${zero}%"><div class="b ${i.v > 0 ? "up" : "down"}" style="${bar}"></div></div><span class="bval">${fmt(i.v)}</span></li>`;
    }).join("");
  }

  function renderCharts() {
    const ps = D.projects;
    divergingRows($("bud"), ps.slice().sort((a, b) => b.forecast_overrun_pct - a.forecast_overrun_pct).map((p) => ({
      label: `${p.project_id} ${p.name}`, v: p.forecast_overrun_pct, tip: `${p.name}: budget ${fmtEur(p.budget_eur)}, forecast ${fmtEur(p.forecast_cost_eur)} (${p.forecast_overrun_eur >= 0 ? "+" : ""}${fmtEur(p.forecast_overrun_eur)})`,
    })), (v) => (v > 0 ? "+" : "") + v.toFixed(1) + "%");
    divergingRows($("sch"), ps.slice().sort((a, b) => b.slip_days - a.slip_days).map((p) => ({
      label: `${p.project_id} ${p.name}`, v: p.slip_days, tip: `${p.name}: planned ${dateStr(p.planned_end)}, forecast ${dateStr(p.forecast_end)}`,
    })), (v) => (v > 0 ? "+" : "") + v + " d");

    const maxU = 160;
    $("res").innerHTML = D.resources.map((r) => `<li class="brow" data-tip="${esc(r.name)} (${esc(r.role)}): ${r.allocated} FTE allocated of ${r.capacity} across ${r.projects} projects. ${r.status}">
      <span>${esc(r.name)}</span><div class="btrack" style="--zero:0%"><div class="b ${r.utilisation_pct > 110 ? "up" : r.utilisation_pct > 100 ? "warn" : "ok"}" style="left:0;width:${Math.min(100, r.utilisation_pct / maxU * 100)}%"></div>
      <i class="mark" style="left:${100 / maxU * 100}%"></i><i class="mark" style="left:${110 / maxU * 100}%"></i></div><span class="bval">${r.utilisation_pct}%</span></li>`).join("");

    const cnt = {}, names = {};
    D.raid.filter((r) => r.type === "Risk" && r.status !== "Closed").forEach((r) => { const k = r.impact + "-" + r.probability; cnt[k] = (cnt[k] || 0) + 1; (names[k] = names[k] || []).push(`${r.project_id} ${r.title}`); });
    const maxC = Math.max(...Object.values(cnt));
    let h = "";
    for (let imp = 5; imp >= 1; imp--) {
      h += `<div class="hl">${imp}</div>`;
      for (let pr = 1; pr <= 5; pr++) {
        const c = cnt[imp + "-" + pr] || 0, a = c ? 0.25 + 0.65 * (c / maxC) : 0;
        h += `<div class="hc" ${c ? `data-tip="${esc(names[imp + "-" + pr].join("; "))}"` : ""} style="${c ? `background:color-mix(in srgb,var(--accent) ${Math.round(a * 100)}%,var(--surface))` : ""}">${c || ""}</div>`;
      }
    }
    h += `<div></div>` + [1, 2, 3, 4, 5].map((n) => `<div class="hl">${n}</div>`).join("");
    $("heat").innerHTML = `<div class="heat">${h}</div><p class="hint">Rows: impact (5 = highest). Columns: probability (5 = near certain).</p>`;
  }

  function renderTop() {
    $("topraid").innerHTML = D.raid.filter((r) => r.status !== "Closed" && r.score != null).sort((a, b) => b.score - a.score).slice(0, 8)
      .map((r) => `<li><span class="tag">${r.type}</span><strong>${esc(r.title)}</strong> · ${r.project_id} · score ${r.score} · ${esc(r.owner)} · ${r.status}</li>`).join("");
  }

  function renderEsc() {
    $("esc").innerHTML = D.projects.filter((p) => p.escalate).sort((a, b) => a.health_score - b.health_score).map((p) =>
      `<div class="esc-item ${p.rag}"><strong>${p.project_id} ${esc(p.name)}</strong> · ${rag(p.rag)} · health ${p.health_score}<p>${esc(p.summary)}</p>
       <p><strong>Recommendation:</strong> ${esc(p.recommendations[0] || "")}</p></div>`).join("");
  }

  // ---------- tooltip + theme ----------
  const tip = $("tip");
  document.addEventListener("mousemove", (e) => {
    const t = e.target.closest && e.target.closest("[data-tip]");
    if (!t) { tip.hidden = true; return; }
    tip.textContent = t.dataset.tip; tip.hidden = false;
    tip.style.left = Math.min(e.clientX + 14, innerWidth - tip.offsetWidth - 8) + "px"; tip.style.top = e.clientY + 16 + "px";
  });
  $("theme").addEventListener("click", () => {
    const r = document.documentElement;
    const dark = r.dataset.theme ? r.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
    r.dataset.theme = dark ? "light" : "dark";
  });

  renderKpis(); renderFilters(); renderTable(); renderDetail(); renderCharts(); renderTop(); renderEsc();
})();
