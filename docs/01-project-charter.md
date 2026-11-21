# Project Charter - AI Project Portfolio Control Tower

| | |
|---|---|
| **Version / status** | 1.0 / Approved (template scenario) |
| **Company (fictional)** | Meridian Works GmbH |
| **Sponsor** | Chief Information Officer |
| **Project manager** | PMO Lead (you) |
| **Business owner** | Head of Portfolio Management Office (PMO) |
| **Methodology** | Hybrid: stage gates for governance, two-week sprints for delivery |

## 1. Purpose and background
Meridian Works runs 15 IT projects across Finance, Operations, IT, Sales, HR, Legal, Marketing, Procurement and Customer Service, with a combined budget of EUR 9.55M. Status reporting is manual: each project manager sends a slide or spreadsheet in a different format, and consolidating them takes days. By the time management sees a delay, a budget overrun or a resource conflict, options are limited.

This project builds a **Control Tower**: one consolidated, near-real-time view of portfolio health, with an AI-written executive status report that explains *why* a project needs attention and recommends actions.

## 2. Objectives (SMART)
| # | Objective | Measure | Target |
|---|---|---|---|
| O1 | One consolidated portfolio view | Projects shown in the dashboard | All 15 active projects |
| O2 | Early warning | Escalation rules flag projects before sponsor reviews | Every project with SPI < 0.80, CPI < 0.85, slip > 30 days or a critical issue is flagged automatically |
| O3 | Cut reporting effort | PM time spent preparing monthly status | From about 1.5 days to about 0.75 days per project per month (assumption, validated in pilot) |
| O4 | Trustworthy AI reports | Figures in AI report that cannot be traced to calculated data | 0 |
| O5 | Resource visibility | People above 110% allocation are visible to the PMO | 100% of people covered |

## 3. Scope
**In scope:** data model and dataset (Excel/CSV), Python processing and metrics, health score, escalation rules, RAID analysis, resource utilisation, Power BI executive dashboard, Streamlit exploration app, LLM-generated executive status report with number verification, documentation.

**Out of scope:** live integration with Jira/MS Project/SAP (data is loaded from files), time-tracking, financial accounting changes, automated emails, predictive forecasting beyond earned-value extrapolation.

## 4. Deliverables
Project charter, business case, requirements specification, project plan, synthetic portfolio dataset, Power BI dashboard (file and screenshots), Python integration code, AI-generated project status report, risk and issue register, lessons learned.

## 5. Milestones (week numbers from project start)
| Milestone | Week |
|---|---|
| M1 Charter and business case approved | 1 |
| M2 Requirements baselined | 2 |
| M3 Dataset and metrics validated | 4 |
| M4 Dashboard v1 reviewed by PMO | 6 |
| M5 AI report accepted by sponsor | 7 |
| M6 Release and handover | 8 |

## 6. Budget and resources
One-off cost EUR 58,900 (see business case) for roughly 87 person-days: PMO analyst, BI developer, data/Python engineer, project manager. Annual run cost about EUR 5,780.

## 7. Stakeholders
| Stakeholder | Interest | Influence |
|---|---|---|
| CIO (sponsor) | Single view of IT delivery, fewer surprises | High |
| PMO Head (business owner) | Consistent reporting, less manual work | High |
| Project managers | Less reporting effort, fair health scoring | Medium |
| Finance Controlling | Reliable cost forecasts | Medium |
| Resource managers | Visibility of over-allocation | Medium |
| Data protection officer | No personal data misuse in AI prompts | Medium |

## 8. Assumptions and constraints
- Project managers can provide a monthly data extract (percent complete, actual cost, RAID entries).
- Health-score weights are agreed with the PMO and reviewed after one quarter.
- Only aggregated project data, never personal data beyond names of role holders, is sent to the LLM provider.
- Constraint: budget cap EUR 60,000; first release within 8 weeks.

## 9. Top risks at initiation
See `risk-issue-register.md`. Main risks: low-quality input data, disagreement over health-score weights, AI text containing wrong numbers, scope creep into live integrations.

## 10. Success criteria / acceptance
A reviewer can open the dashboard, see 15 projects, identify an at-risk project, and read an AI-generated report explaining why it needs attention and what to do (see requirements AC-1 to AC-4).

## 11. Approval
| Role | Name | Date |
|---|---|---|
| Sponsor | ______ | ______ |
| Business owner | ______ | ______ |
| Project manager | ______ | ______ |
