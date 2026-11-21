"""Write docs/portfolio-raid-register.md from data/csv/raid.csv (one table per project, open items first)."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
raid = pd.read_csv(ROOT / "data" / "csv" / "raid.csv")
proj = pd.read_csv(ROOT / "data" / "csv" / "projects.csv").set_index("project_id")["project_name"]
order = {"Escalated": 0, "Open": 1, "Mitigating": 2, "Closed": 3}
out = ["# Portfolio RAID register (synthetic)", "",
       "Generated from `data/csv/raid.csv` by `src/export_raid_markdown.py`. Edit the Excel/CSV, then re-run the script.",
       "Score: risk, assumption, dependency = probability x impact; issue = severity x 5. 15 or more is high.", ""]
open_ = raid[raid["status"] != "Closed"]
out += [f"**{len(raid)} entries, {len(open_)} open** - "
        + ", ".join(f"{n} {t.lower()}s" for t, n in open_["type"].value_counts().items()) + ".", ""]
for pid, g in raid.groupby("project_id"):
    out += [f"## {pid} {proj[pid]}", "", "| ID | Type | Title | Prob | Impact | Score | Owner | Status | Response | Due |", "|---|---|---|---|---|---|---|---|---|---|"]
    g = g.assign(o=g["status"].map(order)).sort_values(["o", "score"], ascending=[True, False])
    for _, r in g.iterrows():
        prob = "" if pd.isna(r["probability"]) else int(r["probability"])
        out.append(f"| {r['raid_id']} | {r['type']} | {r['title']} | {prob} | {int(r['impact'])} | {int(r['score'])} | {r['owner']} | {r['status']} | {r['response']} | {r['due_date']} |")
    out.append("")
(ROOT / "docs" / "portfolio-raid-register.md").write_text("\n".join(out), encoding="utf-8")
print("Wrote docs/portfolio-raid-register.md")
