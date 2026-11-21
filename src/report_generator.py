"""
AI-generated executive status report.

Design: the numbers are computed by src/metrics.py (deterministic, testable). The LLM
only WRITES the narrative from those facts, and `verify_numbers` then checks the text
for any figure that is not in the facts, so a hallucinated number is flagged.

Providers
    offline    no API key needed; deterministic template report (always available, used for tests/demo)
    openai     needs OPENAI_API_KEY and OPENAI_MODEL
    anthropic  needs ANTHROPIC_API_KEY (ANTHROPIC_MODEL optional)
    auto       first provider whose key is set, else offline

Only the Python standard library is used for HTTP, so there is nothing extra to install.
"""
from __future__ import annotations

import json
import os
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPT_FILE = ROOT / "prompts" / "executive_report_prompt.md"


# ----------------------------------------------------------------------------- formatting helpers
def eur(x: float) -> str:
    x = float(x)
    if abs(x) >= 1_000_000:
        return f"EUR {x / 1_000_000:.2f}M".replace(".00M", "M")
    return f"EUR {round(x / 1000):,.0f}k"


def date_str(iso: str) -> str:
    from datetime import date
    d = date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%b %Y')}"


# ----------------------------------------------------------------------------- facts -> prompt
def build_prompt(facts: dict) -> tuple[str, str]:
    system = PROMPT_FILE.read_text(encoding="utf-8")
    user = "FACTS:\n" + json.dumps(facts, indent=1, ensure_ascii=False)
    return system, user


# ----------------------------------------------------------------------------- providers
def _post(url: str, headers: dict, payload: dict) -> dict:
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json", **headers})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read())


def call_openai(system: str, user: str) -> str:
    model = os.environ.get("OPENAI_MODEL")
    if not model:
        raise RuntimeError("Set OPENAI_MODEL (for example in .env) to the model you want to use.")
    out = _post("https://api.openai.com/v1/chat/completions",
                {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
                {"model": model, "temperature": 0.2,
                 "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]})
    return out["choices"][0]["message"]["content"]


def call_anthropic(system: str, user: str) -> str:
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5-5")
    out = _post("https://api.anthropic.com/v1/messages",
                {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"},
                {"model": model, "max_tokens": 3000, "temperature": 0.2, "system": system,
                 "messages": [{"role": "user", "content": user}]})
    return out["content"][0]["text"]


# ----------------------------------------------------------------------------- offline writer
def project_summary(f: dict) -> str:
    """One-paragraph, rule-based explanation of a project's status (also used by the dashboard)."""
    behind = f["spi"] < 1
    s = [f"{f['name']} is {f['actual_pct']:.0f}% complete against {f['planned_pct']:.0f}% planned (SPI {f['spi']:.2f}, CPI {f['cpi']:.2f}). "]
    if f["slip_days"] > 7:
        s.append(f"At the current pace it finishes about {f['slip_days']} days late, on {date_str(f['forecast_end'])} instead of {date_str(f['planned_end'])}. ")
    elif behind and f["slip_days"] > 0:
        s.append(f"The schedule is slightly behind ({f['slip_days']} days of forecast slip). ")
    else:
        s.append("It is on schedule. ")
    if f["forecast_overrun_eur"] > 0:
        s.append(f"The forecast cost is {eur(f['forecast_cost_eur'])} against a budget of {eur(f['budget_eur'])}, an overrun of {eur(f['forecast_overrun_eur'])} ({f['forecast_overrun_pct']:.1f}%). ")
    else:
        s.append(f"The forecast cost of {eur(f['forecast_cost_eur'])} is within the {eur(f['budget_eur'])} budget. ")
    if f["top_items"]:
        t = f["top_items"][0]
        s.append(f"Biggest open item: {t['title']} ({t['type'].lower()}, {t['owner']}). ")
    if f["escalate"]:
        s.append("Escalation triggers: " + "; ".join(f["escalation_reasons"]) + ".")
    return "".join(s).strip()


def recommendations(f: dict) -> list[str]:
    recs = []
    for it in f["top_items"]:
        if it["type"] == "Issue" and (it["score"] or 0) >= 20:
            recs.append(f"{it['owner']}: resolve \"{it['title']}\" ({it['status'].lower()}). Planned response: {it['response']}")
            break
    if f["overallocated_team"]:
        worst = sorted(f["overallocated_team"], key=lambda x: -x["utilisation_pct"])[:2]
        recs.append("Project manager: rebalance workload for " + ", ".join(f"{w['name']} ({w['utilisation_pct']}%)" for w in worst) + ".")
    if f["spi"] < 0.8:
        recs.append(f"{f['manager']}: re-baseline the plan or reduce scope; the forecast end date is {date_str(f['forecast_end'])}.")
    elif f["cpi"] < 0.85:
        recs.append(f"{f['manager']}: re-forecast the budget and ask the sponsor ({f['sponsor']}) to approve or reject the extra {eur(f['forecast_overrun_eur'])}.")
    if len(recs) < 2 and f["top_items"]:
        it = f["top_items"][0]
        recs.append(f"{it['owner']}: {it['response']}")
    return recs[:3]


def offline_report(facts: dict) -> str:
    s, projects = facts["summary"], facts["projects"]
    esc = [p for p in projects if p["escalate"]]
    watch = [p for p in projects if p["rag"] == "Amber" and not p["escalate"]]
    out = [f"# Executive Status Report - {date_str(s['as_of'])}", "",
           "_Generated by the offline (rule-based) writer in `src/report_generator.py`. Run with an LLM provider for narrative prose._", "",
           "## Portfolio at a glance", "",
           f"The portfolio has {s['projects']} projects with a total budget of {eur(s['total_budget_eur'])}. "
           f"{s['rag_counts']['Green']} are Green, {s['rag_counts']['Amber']} Amber and {s['rag_counts']['Red']} Red. "
           f"The portfolio is forecast to cost {eur(s['total_forecast_cost_eur'])}, which is {eur(s['forecast_overrun_eur'])} "
           f"({s['forecast_overrun_pct']:.1f}%) over budget. Portfolio SPI is {s['portfolio_spi']:.2f} and CPI is {s['portfolio_cpi']:.2f}. "
           f"{s['escalations']} projects meet the escalation rules.", "",
           "## Projects needing executive attention", ""]
    for p in esc:
        out += [f"### {p['project_id']} {p['name']} - health {p['health_score']} ({p['rag']})", "", project_summary(p), ""]
        out += ["**Recommendation**", ""] + [f"- {r}" for r in recommendations(p)] + [""]
    out += ["## Watch list", ""] + [f"- **{p['project_id']} {p['name']}** (health {p['health_score']}): SPI {p['spi']:.2f}, CPI {p['cpi']:.2f}." for p in watch] + [""]
    out += ["## Resource conflicts", ""]
    for r in facts["resource_conflicts"]:
        out.append(f"- {r['name']} ({r['role']}): {r['utilisation_pct']}% across {r['projects']} projects.")
    return "\n".join(out) + "\n"


# ----------------------------------------------------------------------------- number check
_ALLOWED_SMALL = set(range(0, 16)) | {100}   # 100 = top of the health-score scale


def _collect_numbers(obj, acc: set):
    if isinstance(obj, bool):
        return
    if isinstance(obj, (int, float)):
        v = abs(float(obj))
        acc.update({v, round(v), round(v, 1), round(v, 2), v / 1000, v / 1_000_000, round(v / 1000), round(v / 1_000_000, 1), round(v / 1_000_000, 2)})
    elif isinstance(obj, dict):
        for x in obj.values():
            _collect_numbers(x, acc)
    elif isinstance(obj, (list, tuple)):
        for x in obj:
            _collect_numbers(x, acc)
    elif isinstance(obj, str):
        for m in re.findall(r"\d+(?:\.\d+)?", obj):
            acc.add(float(m))


def verify_numbers(text: str, facts: dict) -> list[str]:
    """Return numbers in `text` that cannot be traced to `facts` (empty list = all traceable)."""
    allowed: set = set()
    _collect_numbers(facts, allowed)
    clean = re.sub(r"\b(?:P|R|RAID-|CPI|SPI)\d*\b", " ", text)
    clean = re.sub(r"\d{4}-\d{2}-\d{2}", " ", clean)                       # ISO dates
    clean = re.sub(r"\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*(?:\s+\d{4})?", " ", clean)
    clean = re.sub(r"\b20\d{2}\b", " ", clean)
    clean = re.sub(r"^#+ .*$", " ", clean, flags=re.M)                       # headings carry IDs
    clean = re.sub(r"^\s*\d+\.\s", " ", clean, flags=re.M)                   # numbered-list markers
    bad = []
    for m in re.finditer(r"\d[\d,]*(?:\.\d+)?", clean):
        token = m.group(0).replace(",", "")
        if not token or token == ".":
            continue
        v = float(token)
        if v in _ALLOWED_SMALL and float(v).is_integer():
            continue
        if not any(abs(v - a) <= max(0.051, 0.002 * a) for a in allowed):
            bad.append(m.group(0))
    return sorted(set(bad), key=bad.index)


# ----------------------------------------------------------------------------- entry point
def generate_report(facts: dict, provider: str = "auto") -> tuple[str, str]:
    """Return (markdown, provider_used)."""
    if provider == "auto":
        provider = "openai" if os.environ.get("OPENAI_API_KEY") else "anthropic" if os.environ.get("ANTHROPIC_API_KEY") else "offline"
    if provider == "offline":
        return offline_report(facts), "offline"
    system, user = build_prompt(facts)
    text = {"openai": call_openai, "anthropic": call_anthropic}[provider](system, user)
    return text.strip() + "\n", provider
