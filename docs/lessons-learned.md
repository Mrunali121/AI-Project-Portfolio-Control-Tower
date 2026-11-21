# Lessons Learned

A retrospective on building the Control Tower. Add your own observations from running it; the ones below come from the actual build.

## What went well
1. **Calculations in code, writing by the LLM.** Computing SPI, CPI, health and forecasts in tested Python and giving the model only facts removed most of the hallucination risk. A separate checker then validates the text.
2. **Hand-designing the sample portfolio.** Random data produced a flat, boring portfolio. Defining 15 projects with a deliberate story (a few troubled, some on watch, most healthy, shared specialists across the troubled ones) made the dashboard worth reading and showed how resource conflicts cause delays.
3. **One pipeline, many views.** The same metrics feed the web dashboard, Streamlit app, Power BI and the report, so the numbers cannot disagree.
4. **An offline mode.** The report writer works without an API key, so the project always runs for a reviewer.

## What went wrong, and what we changed
| # | What happened | Impact | Change made |
|---|---|---|---|
| 1 | Assumptions and dependencies were not scored, so they were silently left out of the risk component of the health score | One project looked healthier than it was (P05 Green instead of Amber); average health overstated by about 3 points | Scored every non-issue item; reviewed outputs row by row; added a test |
| 2 | The first number checker used a loose tolerance and let an invented figure pass (an invented 777k matched a real 778k) | The safeguard was weaker than it looked | Tightened the tolerance and added a test with a clearly invented number. Lesson: test the checker with a deliberately wrong input |
| 3 | The checker flagged "out of 100" as unverifiable | False alarm that would train people to ignore warnings | Allowed the scale constant; kept the check strict for everything else |
| 4 | The KPI cards overflowed on a phone | Horizontal scrolling on mobile | Let the status icons wrap; re-tested at 390 px |
| 5 | A Power BI file cannot be created outside Power BI Desktop, and Streamlit could not be installed in the build environment | Two deliverables could not be proven end to end here | Delivered a Power BI build kit and an equivalent web dashboard; kept Streamlit code thin so its logic is covered by unit tests; documented both as open issues |

## Project-management lessons
- **Agree the rules before the pictures.** The health-score weights and escalation thresholds are policy choices. Publishing the formula early (and showing the breakdown per project) prevents arguments about fairness.
- **A portfolio view exposes shared-resource problems that single-project reports hide.** One database administrator at 140% touches four projects; no individual project report would show it.
- **Earned value is a smoke alarm, not a diagnosis.** SPI and CPI say *that* a project is in trouble; the RAID items say *why*. The dashboard needs both.
- **Say what the data is.** Marking the data as synthetic everywhere avoids over-claiming, which matters more than a polished chart.
- **Defer integrations.** Live Jira or SAP connections were tempting but would have doubled the schedule; change control kept the first release small.

## What I would do differently
- Start the number-verification test earlier, before writing the report generator.
- Involve a real project manager to calibrate the health weights on historical projects.
- Keep a data-quality page in the dashboard (data age, missing updates per project).
- Test the Streamlit app in a clean environment as part of the definition of done.

## Next steps (release 2)
1. Connect to a real source (Jira or MS Project export) instead of CSV files.
2. Back-test escalation rules on completed projects to tune thresholds.
3. Add scheduled monthly report generation and email to the steering committee.
4. Add a "what-if" view: move a person between projects and see the effect on health.
