"""
Portfolio metrics: earned-value (SPI/CPI), forecasts, project health score,
escalation rules, resource utilisation and the facts passed to the report writer.

Everything is a plain pandas function so it can be unit-tested and reused by the
command-line pipeline, the Streamlit app and (as DAX) Power BI.

Health score (0-100), weights chosen to match how steering committees think:
    schedule  30%   SPI 1.0 or better = 100, SPI 0.5 or worse = 0 (linear between)
    cost      30%   CPI 1.0 or better = 100, CPI 0.5 or worse = 0 (linear between)
    risk      15%   open risk exposure (sum of probability x impact); 50+ = 0
    issues    15%   100 minus penalties for open issues (critical 40, high 20, medium 8, low 2)
    resources 10%   100 minus the share of the project's FTE held by over-allocated people
RAG: Green >= 75, Amber 55-74, Red < 55.
"""
from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CSV_DIR = ROOT / "data" / "csv"

WEIGHTS = {"schedule": 0.30, "cost": 0.30, "risk": 0.15, "issues": 0.15, "resources": 0.10}
GREEN_FROM, AMBER_FROM = 75, 55
ISSUE_PENALTY = {5: 40, 4: 20, 3: 8, 2: 2, 1: 2}
RISK_EXPOSURE_CAP = 50.0
ESCALATE_SPI, ESCALATE_CPI, ESCALATE_SLIP_DAYS = 0.80, 0.85, 30


def load_tables(csv_dir: Path = CSV_DIR) -> dict[str, pd.DataFrame]:
    t = {p.stem: pd.read_csv(p) for p in Path(csv_dir).glob("*.csv")}
    for col in ("start_date", "planned_end_date", "as_of_date"):
        t["projects"][col] = pd.to_datetime(t["projects"][col])
    t["raid"]["due_date"] = pd.to_datetime(t["raid"]["due_date"])
    t["raid"]["raised_date"] = pd.to_datetime(t["raid"]["raised_date"])
    t["monthly_progress"]["month_end"] = pd.to_datetime(t["monthly_progress"]["month_end"])
    return t


def linear_score(value: float, bad: float = 0.5, good: float = 1.0) -> float:
    return float(np.clip((value - bad) / (good - bad), 0, 1) * 100)


def rag_for(score: float) -> str:
    return "Green" if score >= GREEN_FROM else "Amber" if score >= AMBER_FROM else "Red"


def utilisation(t: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Per-person utilisation = total allocated FTE / capacity."""
    a = t["allocations"].groupby("resource_id", as_index=False)["allocation_fte"].sum()
    u = t["resources"].merge(a, on="resource_id", how="left").fillna({"allocation_fte": 0.0})
    u["utilisation_pct"] = (u["allocation_fte"] / u["capacity_fte"] * 100).round(0)
    u["status"] = np.where(u["utilisation_pct"] > 110, "Over-allocated",
                           np.where(u["utilisation_pct"] > 100, "Stretched", "OK"))
    n_proj = t["allocations"].groupby("resource_id")["project_id"].nunique().rename("projects")
    return u.merge(n_proj, on="resource_id", how="left").fillna({"projects": 0})


def project_metrics(t: dict[str, pd.DataFrame]) -> pd.DataFrame:
    p = t["projects"].copy()
    raid, util, alloc = t["raid"], utilisation(t), t["allocations"]

    total_days = (p["planned_end_date"] - p["start_date"]).dt.days
    elapsed = (p["as_of_date"] - p["start_date"]).dt.days
    p["planned_pct_complete"] = (elapsed / total_days).clip(0, 1) * 100

    p["bac"] = p["budget_eur"]
    p["pv"] = p["bac"] * p["planned_pct_complete"] / 100
    p["ev"] = p["bac"] * p["actual_pct_complete"] / 100
    p["ac"] = p["actual_cost_eur"]
    p["spi"] = p["ev"] / p["pv"]
    p["cpi"] = p["ev"] / p["ac"]
    p["eac"] = p["bac"] / p["cpi"].clip(lower=0.3)
    p["variance_at_completion"] = p["bac"] - p["eac"]                 # negative = overrun
    p["forecast_overrun_pct"] = (p["eac"] / p["bac"] - 1) * 100
    p["schedule_variance_eur"] = p["ev"] - p["pv"]

    pace = p["spi"].clip(lower=0.4, upper=1.0)
    forecast_days = (total_days / pace).round().astype(int)
    p["forecast_end_date"] = p["start_date"] + pd.to_timedelta(forecast_days, unit="D")
    p["slip_days"] = (p["forecast_end_date"] - p["planned_end_date"]).dt.days

    open_raid = raid[raid["status"] != "Closed"]
    exposure = (open_raid[open_raid["type"].isin(["Risk", "Dependency", "Assumption"])]
                .groupby("project_id")["score"].sum().rename("risk_exposure"))
    issues = open_raid[open_raid["type"] == "Issue"]
    penalty = issues.assign(pen=issues["impact"].map(ISSUE_PENALTY)).groupby("project_id")["pen"].sum().rename("issue_penalty")
    crit = issues[issues["impact"] >= 5].groupby("project_id").size().rename("critical_issues")
    n_issues = issues.groupby("project_id").size().rename("open_issues")
    n_risks = open_raid[open_raid["type"] == "Risk"].groupby("project_id").size().rename("open_risks")
    for s in (exposure, penalty, crit, n_issues, n_risks):
        p = p.merge(s, left_on="project_id", right_index=True, how="left")
    for c in ("risk_exposure", "issue_penalty", "critical_issues", "open_issues", "open_risks"):
        p[c] = p[c].fillna(0)

    over = set(util.loc[util["utilisation_pct"] > 100, "resource_id"])
    al = alloc.assign(over=alloc["resource_id"].isin(over) * alloc["allocation_fte"])
    share = (al.groupby("project_id")["over"].sum() / al.groupby("project_id")["allocation_fte"].sum()).rename("over_share")
    p = p.merge(share, left_on="project_id", right_index=True, how="left").fillna({"over_share": 0})

    p["score_schedule"] = p["spi"].map(linear_score)
    p["score_cost"] = p["cpi"].map(linear_score)
    p["score_risk"] = (100 * (1 - (p["risk_exposure"] / RISK_EXPOSURE_CAP).clip(upper=1)))
    p["score_issues"] = (100 - p["issue_penalty"]).clip(lower=0)
    p["score_resources"] = 100 * (1 - p["over_share"])
    p["health_score"] = sum(p[f"score_{k}"] * w for k, w in WEIGHTS.items()).round(0)
    p["rag"] = p["health_score"].map(rag_for)

    def reasons(r) -> list[str]:
        out = []
        if r["health_score"] < AMBER_FROM:
            out.append(f"health score {r['health_score']:.0f} is in the Red band")
        if r["spi"] < ESCALATE_SPI:
            out.append(f"SPI {r['spi']:.2f} is below {ESCALATE_SPI}")
        if r["cpi"] < ESCALATE_CPI:
            out.append(f"CPI {r['cpi']:.2f} is below {ESCALATE_CPI}")
        if r["critical_issues"] > 0:
            out.append("a critical issue is open")
        if r["slip_days"] > ESCALATE_SLIP_DAYS:
            out.append(f"forecast slip of {r['slip_days']} days exceeds {ESCALATE_SLIP_DAYS}")
        return out

    p["escalation_reasons"] = p.apply(reasons, axis=1)
    p["escalate"] = p["escalation_reasons"].map(bool)
    return p.sort_values("health_score").reset_index(drop=True)


def monthly_trend(t: dict[str, pd.DataFrame]) -> pd.DataFrame:
    m = t["monthly_progress"].merge(t["projects"][["project_id", "budget_eur"]], on="project_id")
    m["ev"] = m["budget_eur"] * m["actual_pct_complete"] / 100
    m["pv"] = m["budget_eur"] * m["planned_pct_complete"] / 100
    m["spi"] = (m["ev"] / m["pv"]).replace([np.inf, -np.inf], np.nan)
    m["cpi"] = (m["ev"] / m["actual_cost_eur"]).replace([np.inf, -np.inf], np.nan)
    return m


def portfolio_summary(p: pd.DataFrame, u: pd.DataFrame) -> dict:
    bac, ev, pv, ac, eac = (p[c].sum() for c in ("bac", "ev", "pv", "ac", "eac"))
    return {
        "as_of": p["as_of_date"].iloc[0].date().isoformat(),
        "projects": int(len(p)),
        "total_budget_eur": float(bac),
        "total_actual_cost_eur": float(ac),
        "total_forecast_cost_eur": float(eac),
        "forecast_overrun_eur": float(eac - bac),
        "forecast_overrun_pct": float((eac / bac - 1) * 100),
        "portfolio_spi": float(ev / pv),
        "portfolio_cpi": float(ev / ac),
        "avg_health_score": float(np.average(p["health_score"], weights=p["bac"])),
        "rag_counts": {k: int((p["rag"] == k).sum()) for k in ("Green", "Amber", "Red")},
        "escalations": int(p["escalate"].sum()),
        "overallocated_people": int((u["utilisation_pct"] > 110).sum()),
        "stretched_people": int(((u["utilisation_pct"] > 100) & (u["utilisation_pct"] <= 110)).sum()),
    }


def project_facts(p: pd.DataFrame, t: dict[str, pd.DataFrame], u: pd.DataFrame) -> list[dict]:
    """Plain-dict facts per project. The report writer may use ONLY these numbers."""
    raid = t["raid"]
    names = t["resources"].set_index("resource_id")["name"]
    alloc = t["allocations"]
    facts = []
    for _, r in p.iterrows():
        pr = raid[(raid["project_id"] == r["project_id"]) & (raid["status"] != "Closed")]
        top = pr.sort_values("score", ascending=False).head(3)
        team = alloc[alloc["project_id"] == r["project_id"]].merge(u[["resource_id", "utilisation_pct"]], on="resource_id")
        stretched = team[team["utilisation_pct"] > 100]
        facts.append({
            "project_id": r["project_id"], "name": r["project_name"], "department": r["department"],
            "manager": r["project_manager"], "sponsor": r["sponsor"], "methodology": r["methodology"],
            "planned_end": r["planned_end_date"].date().isoformat(),
            "forecast_end": r["forecast_end_date"].date().isoformat(),
            "slip_days": int(r["slip_days"]),
            "budget_eur": int(r["bac"]), "actual_cost_eur": int(r["ac"]), "forecast_cost_eur": int(round(r["eac"], -3)),
            "forecast_overrun_eur": int(round(r["eac"] - r["bac"], -3)),
            "forecast_overrun_pct": round(float(r["forecast_overrun_pct"]), 1),
            "planned_pct": round(float(r["planned_pct_complete"]), 1), "actual_pct": float(r["actual_pct_complete"]),
            "spi": round(float(r["spi"]), 2), "cpi": round(float(r["cpi"]), 2),
            "health_score": int(r["health_score"]), "rag": r["rag"],
            "escalate": bool(r["escalate"]), "escalation_reasons": list(r["escalation_reasons"]),
            "open_risks": int(r["open_risks"]), "open_issues": int(r["open_issues"]),
            "top_items": [
                {"id": x["raid_id"], "type": x["type"], "title": x["title"], "score": int(x["score"]) if pd.notna(x["score"]) else None,
                 "owner": x["owner"], "status": x["status"], "response": x["response"]}
                for _, x in top.iterrows()
            ],
            "overallocated_team": [
                {"name": names[x["resource_id"]], "utilisation_pct": int(x["utilisation_pct"])}
                for _, x in stretched.iterrows()
            ],
        })
    return facts
