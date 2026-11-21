# Requirements Specification

Priority uses MoSCoW: **M**ust, **S**hould, **C**ould. "Where" shows where the requirement is implemented.

## 1. Functional requirements
| ID | Requirement | Priority | Where / how verified |
|---|---|---|---|
| FR-01 | Show all projects in one table with status (RAG), health score, SPI, CPI, schedule slip and cost overrun | M | `index.html`; Power BI page 1; test `test_fifteen_projects` |
| FR-02 | Calculate SPI = EV / PV and CPI = EV / AC for every project | M | `src/metrics.py`; test `test_earned_value_identities` |
| FR-03 | Forecast cost at completion (BAC / CPI) and forecast finish date | M | `metrics.py` |
| FR-04 | Calculate a 0-100 project health score from schedule, cost, risk, issues and resources, with documented weights | M | `metrics.py`; `test_health_*` |
| FR-05 | Classify Green / Amber / Red by fixed thresholds (75 / 55) | M | `metrics.rag_for` |
| FR-06 | Apply escalation rules: Red health, SPI < 0.80, CPI < 0.85, slip > 30 days, open critical issue; show the reasons | M | `metrics.project_metrics` |
| FR-07 | Budget variance view per project and for the portfolio | M | dashboard "Budget variance"; DAX `Forecast Overrun %` |
| FR-08 | Schedule variance view per project (forecast slip in days) | M | dashboard "Schedule variance" |
| FR-09 | RAID register with probability, impact, score, owner, status, response, due date | M | `data/portfolio_dataset.xlsx` (RAID sheet) |
| FR-10 | Risk heat map and list of highest-scoring open items | S | dashboard; Power BI page 4 |
| FR-11 | Resource utilisation per person; flag > 100% and > 110% | M | `metrics.utilisation`; dashboard |
| FR-12 | Project drill-down: summary, recommended actions, SPI/CPI trend, health breakdown, top RAID items | M | dashboard detail panel; Power BI drill-through |
| FR-13 | Generate an executive status report with an LLM from calculated facts only | M | `report_generator.py` |
| FR-14 | Automatically check every figure in the report against the facts; flag any that cannot be traced | M | `verify_numbers`; test `test_verifier_catches_invented_number` |
| FR-15 | Work without an API key (offline rule-based writer) so the demo always runs | S | `offline_report`; test `test_offline_report_numbers_are_traceable` |
| FR-16 | Generate management recommendations per escalated project, with an owner | M | `recommendations()`; report |
| FR-17 | Filter by status and department; sort by any column | S | dashboard; Streamlit sidebar |
| FR-18 | Interactive Streamlit app with report generation and download | C | `app/streamlit_app.py` |
| FR-19 | Reproducible pipeline: one command regenerates all outputs | S | `src/run_pipeline.py` |
| FR-20 | Export processed tables for Power BI | M | `data/processed/*.csv` |

## 2. Non-functional requirements
| ID | Requirement | Verified by |
|---|---|---|
| NFR-01 | Dashboard loads and works without a server (open `index.html`) and on GitHub Pages | Browser test |
| NFR-02 | Responsive: usable at phone width, no horizontal page scroll | Browser test at 390 px |
| NFR-03 | Accessible: status shown by icon and text, not colour alone; keyboard-selectable rows; visible focus; light and dark theme | Manual / browser test |
| NFR-04 | Deterministic: same inputs give same metrics; random data uses a fixed seed | `generate_data.py` seed 2026 |
| NFR-05 | Testable: core logic covered by automated tests, `python -m unittest discover -s tests` | 13 tests |
| NFR-06 | Privacy: LLM receives only aggregated project facts; no secrets in the repo (`.env` is git-ignored) | Code review |
| NFR-07 | Transparency: data is labelled synthetic everywhere it is shown | UI, README |

## 3. Data requirements
Projects (15), RAID register (45 entries), Resources (24), Allocations (62), Monthly progress (109 rows). Fields are described in `data-dictionary.md`.

## 4. Business rules
- Planned % complete is linear between start and planned end.
- Forecast finish = start + planned duration / min(SPI, 1.0), with SPI floored at 0.4.
- Closed RAID items are excluded from scoring.
- Health weights: schedule 30, cost 30, risk 15, issues 15, resources 10.

## 5. Acceptance criteria
| ID | Criterion |
|---|---|
| AC-1 | The dashboard shows 15 projects with RAG status and health score |
| AC-2 | A reviewer can identify the most at-risk project (P01 ERP Finance Migration) within 30 seconds |
| AC-3 | The AI executive report explains for each escalated project what is wrong, why it needs attention and what to do |
| AC-4 | Every figure in the report can be traced to `outputs/portfolio_facts.json` (verifier returns an empty list) |
| AC-5 | All automated tests pass |

## 6. Traceability
Each deliverable in the charter maps to requirements: dashboard (FR-01, 07, 08, 10-12, 17), AI report (FR-13, 14, 16), health score (FR-04-06), resource utilisation (FR-11), dataset (FR-09, 20), code (FR-02, 03, 19).
