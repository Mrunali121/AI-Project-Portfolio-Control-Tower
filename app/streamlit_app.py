"""
Interactive Streamlit app for the Portfolio Control Tower.

    pip install -r requirements.txt
    streamlit run app/streamlit_app.py

Tabs: Portfolio | Project drill-down | Risks and issues | Resources | AI report.
The AI report tab uses the offline writer unless an API key is set (see .env.example).
"""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import metrics as M                       # noqa: E402
import report_generator as G              # noqa: E402
from run_pipeline import build_everything, load_dotenv   # noqa: E402

load_dotenv()
st.set_page_config(page_title="AI Project Portfolio Control Tower", layout="wide")


@st.cache_data
def load():
    b = build_everything()
    return b["metrics"], b["util"], b["tables"]["raid"], b["trend"], b["summary"], b["facts"]


p, util, raid, trend, summary, facts = load()
EMOJI = {"Green": "🟢", "Amber": "🟠", "Red": "🔴"}

st.title("AI Project Portfolio Control Tower")
st.caption(f"Synthetic data for a fictional company · status as of {summary['as_of']}")

depts = st.sidebar.multiselect("Department", sorted(p["department"].unique()), default=sorted(p["department"].unique()))
rags = st.sidebar.multiselect("Status", ["Red", "Amber", "Green"], default=["Red", "Amber", "Green"])
view = p[p["department"].isin(depts) & p["rag"].isin(rags)]

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Portfolio", "Project drill-down", "Risks and issues", "Resources", "AI report"])

with tab1:
    c = st.columns(5)
    c[0].metric("Avg health score", f"{summary['avg_health_score']:.0f}")
    c[1].metric("Red / Amber / Green", f"{summary['rag_counts']['Red']} / {summary['rag_counts']['Amber']} / {summary['rag_counts']['Green']}")
    c[2].metric("Forecast overrun", f"€{summary['forecast_overrun_eur']/1e6:.2f}M", f"{summary['forecast_overrun_pct']:.1f}%", delta_color="inverse")
    c[3].metric("Portfolio SPI / CPI", f"{summary['portfolio_spi']:.2f} / {summary['portfolio_cpi']:.2f}")
    c[4].metric("Need escalation", summary["escalations"])
    table = view.assign(Status=view["rag"].map(EMOJI) + " " + view["rag"])[
        ["project_id", "project_name", "department", "Status", "health_score", "spi", "cpi", "slip_days", "forecast_overrun_pct", "escalate"]
    ].rename(columns={"project_id": "ID", "project_name": "Project", "department": "Department", "health_score": "Health",
                      "spi": "SPI", "cpi": "CPI", "slip_days": "Slip (days)", "forecast_overrun_pct": "Overrun %", "escalate": "Escalate"})
    st.dataframe(table.round(2), hide_index=True, use_container_width=True)
    l, r = st.columns(2)
    l.subheader("Budget variance (forecast vs budget, €k)")
    l.bar_chart((view.set_index("project_id")["variance_at_completion"] / 1000).round(0))
    r.subheader("Schedule variance (forecast slip, days)")
    r.bar_chart(view.set_index("project_id")["slip_days"])

with tab2:
    choice = st.selectbox("Project", p["project_id"] + " " + p["project_name"])
    pid = choice.split()[0]
    f = next(x for x in facts["projects"] if x["project_id"] == pid)
    st.subheader(f"{EMOJI[f['rag']]} {f['name']} - health {f['health_score']}")
    st.write(G.project_summary(f))
    st.markdown("**Recommended actions**")
    for r_ in G.recommendations(f):
        st.markdown(f"- {r_}")
    tr = trend[trend["project_id"] == pid].set_index("month_end")[["spi", "cpi"]]
    st.line_chart(tr)
    st.markdown("**Health score breakdown**")
    row = p[p["project_id"] == pid].iloc[0]
    st.bar_chart(pd.Series({k: row[f"score_{k}"] for k in M.WEIGHTS}))

with tab3:
    open_ = raid[raid["status"] != "Closed"].merge(p[["project_id", "project_name"]], on="project_id")
    kind = st.multiselect("Type", sorted(open_["type"].unique()), default=["Risk", "Issue"])
    st.dataframe(open_[open_["type"].isin(kind)].sort_values("score", ascending=False)[
        ["raid_id", "project_name", "type", "title", "score", "owner", "status", "due_date"]], hide_index=True, use_container_width=True)
    heat = open_[open_["type"] == "Risk"].groupby(["impact", "probability"]).size().unstack(fill_value=0).reindex(index=range(5, 0, -1), columns=range(1, 6), fill_value=0)
    st.markdown("**Risk heat map** (rows: impact 5 to 1, columns: probability 1 to 5, values: number of open risks)")
    st.dataframe(heat)

with tab4:
    st.bar_chart(util.set_index("name")["utilisation_pct"])
    st.caption("Above 100% means the person is allocated more than their capacity; above 110% is flagged as over-allocated.")
    st.dataframe(util[["name", "role", "capacity_fte", "allocation_fte", "utilisation_pct", "status", "projects"]].sort_values("utilisation_pct", ascending=False), hide_index=True)

with tab5:
    provider = st.selectbox("Report writer", ["offline", "openai", "anthropic"])
    if st.button("Generate executive report"):
        try:
            with st.spinner("Writing report..."):
                md, used = G.generate_report(facts, provider)
            bad = G.verify_numbers(md, facts)
            st.markdown(md)
            (st.success if not bad else st.warning)("All figures traceable to the data." if not bad else f"Figures not found in the data: {bad}")
            st.download_button("Download report (.md)", md, file_name="executive-status-report.md")
        except Exception as e:               # missing key, network error, ...
            st.error(f"Could not generate the report: {e}")
