# Risk and Issue Register - the Control Tower project

This register tracks risks and issues of **building** the Control Tower. The 45-entry register of the 15 *sample portfolio* projects is in [`portfolio-raid-register.md`](portfolio-raid-register.md) and the Excel file `data/portfolio_dataset.xlsx`.

Scale: probability and impact 1-5; score = probability x impact (15 or more is high).

## Risks
| ID | Risk | Prob | Impact | Score | Response | Owner | Status |
|---|---|---|---|---|---|---|---|
| CT-R01 | Input data quality is poor (late or inconsistent project updates) | 4 | 4 | 16 | Validate inputs, require owner sign-off, show data date on every page | PMO analyst | Mitigating |
| CT-R02 | AI report contains a wrong or invented number | 3 | 5 | 15 | Calculate in code, give the LLM facts only, verify every figure automatically, human review | Data engineer | Mitigating |
| CT-R03 | Project managers disagree with the health-score weights | 4 | 3 | 12 | Publish formula, agree weights with the PMO head, review after one quarter | PM | Open |
| CT-R04 | Scope creep into live integrations (Jira, SAP) | 3 | 4 | 12 | Change control; defer to release 2 | PM | Open |
| CT-R05 | Power BI licences or Desktop not available to all reviewers | 2 | 3 | 6 | Provide the web dashboard and screenshots as equal alternatives | BI developer | Open |
| CT-R06 | Sensitive data sent to an external LLM provider | 2 | 5 | 10 | Send only aggregated facts, no personal data beyond role-holder names; DPO review; offline mode available | Data engineer | Mitigating |
| CT-R07 | Dashboard seen as a surveillance tool, lowering adoption | 3 | 4 | 12 | Position as support for project managers; show their effort saved | Sponsor | Open |
| CT-R08 | Synthetic data mistaken for real results | 2 | 4 | 8 | Label "synthetic" on every page and in the README | PM | Mitigating |
| CT-R09 | Key person (data engineer) unavailable | 2 | 4 | 8 | Document code, tests and run instructions | PM | Open |
| CT-R10 | Cost forecast (BAC / CPI) misleads on early-stage projects | 3 | 3 | 9 | Show SPI and CPI trend; note the method; floor CPI | PMO analyst | Mitigating |

## Issues (found during the build)
| ID | Issue | Severity | Resolution | Status |
|---|---|---|---|---|
| CT-I01 | Assumptions and dependencies had no score, so they were ignored in the health score; found when reviewing the data. Effect: P05 moved from Green to Amber and average health from 69 to 67 after the fix. | Medium | Score all non-issue items as probability x impact; add test coverage | Closed |
| CT-I02 | Number verifier accepted an invented figure because its tolerance was too wide | High | Tighten tolerance to 0.2%; test with an invented number | Closed |
| CT-I03 | Verifier flagged "out of 100" as an untraceable number | Low | Allow the health-score scale constant | Closed |
| CT-I04 | KPI row overflowed horizontally on a 390 px phone | Low | Allow the status icons to wrap | Closed |
| CT-I05 | Power BI file cannot be produced without Power BI Desktop | Medium | Deliver a build kit (queries, model, DAX, theme, page layouts) plus an equivalent web dashboard | Open |
| CT-I06 | Streamlit could not be installed in the build environment, so the app was syntax-checked but not run end to end | Medium | The app only calls tested functions; run `streamlit run app/streamlit_app.py` locally and report any defect | Open |
