# Portfolio RAID register (synthetic)

Generated from `data/csv/raid.csv` by `src/export_raid_markdown.py`. Edit the Excel/CSV, then re-run the script.
Score: risk, assumption, dependency = probability x impact; issue = severity x 5. 15 or more is high.

**45 entries, 42 open** - 21 risks, 9 issues, 7 dependencys, 5 assumptions.

## P01 ERP Finance Migration

| ID | Type | Title | Prob | Impact | Score | Owner | Status | Response | Due |
|---|---|---|---|---|---|---|---|---|---|
| RAID-001 | Issue | Ledger data migration fails reconciliation |  | 5 | 25 | Lena Hartmann | Escalated | Dedicated data-cleansing squad; reconciliation rules agreed with Finance; steering committee decision on a third trial load. | 2026-11-14 |
| RAID-002 | Risk | Year-end close overlaps with cut-over window | 4 | 5 | 20 | Lena Hartmann | Open | Negotiate cut-over after the close or split go-live into two phases. | 2026-11-20 |
| RAID-004 | Dependency | Bank interface certification | 3 | 4 | 12 | Eva Maier | Open | Submit certification request now; track weekly with the bank. | 2026-11-10 |
| RAID-005 | Assumption | Chart of accounts frozen by 31 March | 3 | 3 | 9 | Mira Kovacs | Open | Assumption no longer holds; add change-control gate for account changes. | 2026-11-05 |
| RAID-003 | Risk | ERP consultant contract ends in December | 4 | 4 | 16 | Lena Hartmann | Mitigating | Extension quotation requested; knowledge-transfer sessions scheduled. | 2026-11-30 |

## P02 Customer Portal Relaunch

| ID | Type | Title | Prob | Impact | Score | Owner | Status | Response | Due |
|---|---|---|---|---|---|---|---|---|---|
| RAID-006 | Risk | Peak-season load testing starts late | 2 | 3 | 6 | Anna Köhler | Open | Bring forward performance test environment booking. | 2026-11-30 |
| RAID-007 | Assumption | SSO provider API stays stable | 2 | 3 | 6 | Felix Brandt | Open | Confirm roadmap with the provider each quarter. | 2026-12-15 |

## P03 HR Self-Service App

| ID | Type | Title | Prob | Impact | Score | Owner | Status | Response | Due |
|---|---|---|---|---|---|---|---|---|---|
| RAID-008 | Risk | Works council approval for time tracking | 3 | 3 | 9 | Anna Köhler | Mitigating | Early workshop held; approval meeting set for 18 Nov. | 2026-11-18 |
| RAID-009 | Issue | App-store review delay |  | 2 | 10 | Nora Schulz | Closed | Submit earlier in the sprint; buffer added to plan. | 2026-10-05 |

## P04 Warehouse Management System Upgrade

| ID | Type | Title | Prob | Impact | Score | Owner | Status | Response | Due |
|---|---|---|---|---|---|---|---|---|---|
| RAID-010 | Issue | Scanner firmware incompatible with WMS v9 |  | 4 | 20 | Emre Yilmaz | Open | Vendor escalation; interim workaround with older scanner profile. | 2026-11-12 |
| RAID-011 | Risk | DBA over-allocation delays schema migration | 4 | 4 | 16 | Emre Yilmaz | Open | Request contractor DBA for 3 months; re-prioritise portfolio DBA time. | 2026-11-15 |
| RAID-012 | Risk | Cut-over during Q1 stock-take | 3 | 5 | 15 | Emre Yilmaz | Open | Move go-live to mid-February or run a parallel pilot site first. | 2026-12-01 |
| RAID-013 | Dependency | Hardware delivery from vendor | 3 | 3 | 9 | Marco Rossi | Open | Weekly delivery check-in; second supplier as fallback. | 2026-11-28 |

## P05 Data Platform Modernisation

| ID | Type | Title | Prob | Impact | Score | Owner | Status | Response | Due |
|---|---|---|---|---|---|---|---|---|---|
| RAID-016 | Dependency | Cloud landing zone from P12 | 3 | 4 | 12 | Sofia Lindqvist | Open | Joint milestone plan with P12. | 2026-11-25 |
| RAID-014 | Risk | Source-system owners delay data extracts | 3 | 4 | 12 | Thomas Berger | Mitigating | Sponsor letter sent; extract workshop booked. | 2026-11-12 |
| RAID-015 | Risk | Cloud run-cost above forecast | 3 | 3 | 9 | Ivan Petrov | Mitigating | Introduce cost alerts and partitioning review. | 2026-11-30 |

## P06 Cyber Security Hardening

| ID | Type | Title | Prob | Impact | Score | Owner | Status | Response | Due |
|---|---|---|---|---|---|---|---|---|---|
| RAID-017 | Risk | Pen-test findings exceed remediation capacity | 2 | 4 | 8 | Thomas Berger | Open | Risk-rank findings; agree acceptance criteria for low severity. | 2026-11-20 |
| RAID-018 | Assumption | Security tooling licences approved | 1 | 3 | 3 | Aylin Demir | Closed | Approval confirmed on 2026-08-22. | 2026-08-22 |

## P07 CRM Rollout for Sales

| ID | Type | Title | Prob | Impact | Score | Owner | Status | Response | Due |
|---|---|---|---|---|---|---|---|---|---|
| RAID-019 | Issue | Low sales-team adoption |  | 4 | 20 | Julia Neumann | Escalated | Sales directors to mandate attendance; add regional super-users. | 2026-11-12 |
| RAID-020 | Risk | Q4 quota season limits UAT availability | 4 | 4 | 16 | Julia Neumann | Open | Shorten UAT scope to critical flows; evening sessions. | 2026-11-10 |
| RAID-021 | Risk | ERP integration delayed by P01 | 3 | 4 | 12 | Marco Rossi | Open | Define interim file-based interface. | 2026-11-30 |
| RAID-022 | Dependency | Customer master data from P01 | 4 | 3 | 12 | Julia Neumann | Open | Agree delivery date with P01 programme manager. | 2026-11-20 |

## P08 GDPR Compliance Programme

| ID | Type | Title | Prob | Impact | Score | Owner | Status | Response | Due |
|---|---|---|---|---|---|---|---|---|---|
| RAID-024 | Issue | Missing data-processing agreements |  | 3 | 15 | Sara Haddad | Open | Procurement to apply payment hold on unsigned suppliers. | 2026-11-15 |
| RAID-025 | Assumption | Audit scope stays unchanged | 2 | 3 | 6 | Sara Haddad | Open | Confirm scope in writing with the regulator. | 2026-11-20 |
| RAID-023 | Risk | Regulator review date is fixed | 2 | 5 | 10 | Nadine Roth | Mitigating | Evidence pack 80% complete; mock review planned for 30 Nov. | 2026-12-14 |

## P09 Marketing Automation Platform

| ID | Type | Title | Prob | Impact | Score | Owner | Status | Response | Due |
|---|---|---|---|---|---|---|---|---|---|
| RAID-027 | Dependency | Clean contact data from P07 | 3 | 3 | 9 | Mia Becker | Open | Interim data-cleansing script as a fallback. | 2026-12-10 |
| RAID-026 | Risk | Agency contract renewal | 2 | 2 | 4 | Julia Neumann | Open | Start renewal discussion in November. | 2026-12-01 |

## P10 Predictive Maintenance Pilot

| ID | Type | Title | Prob | Impact | Score | Owner | Status | Response | Due |
|---|---|---|---|---|---|---|---|---|---|
| RAID-028 | Issue | Sensor delivery slipped six weeks |  | 4 | 20 | Emre Yilmaz | Escalated | Sponsor escalation to the vendor; pilot plant 2 re-sequenced. | 2026-11-14 |
| RAID-030 | Assumption | Maintenance team available for pilot | 3 | 3 | 9 | Emre Yilmaz | Open | Agree roster with plant managers. | 2026-11-15 |
| RAID-029 | Risk | Pilot data quality too low for modelling | 3 | 4 | 12 | Clara Fischer | Mitigating | Add buffering at the edge; synthetic augmentation test. | 2026-11-25 |

## P11 Intranet Replacement

| ID | Type | Title | Prob | Impact | Score | Owner | Status | Response | Due |
|---|---|---|---|---|---|---|---|---|---|
| RAID-032 | Risk | Low early adoption | 2 | 2 | 4 | Paul Richter | Open | Redirect old URLs; communication plan. | 2026-11-20 |
| RAID-031 | Issue | Search relevance tuning |  | 2 | 10 | Anna Köhler | Mitigating | Synonym list and boosting rules in progress. | 2026-11-12 |

## P12 Cloud Migration Wave 2

| ID | Type | Title | Prob | Impact | Score | Owner | Status | Response | Due |
|---|---|---|---|---|---|---|---|---|---|
| RAID-033 | Issue | Network latency above SLA |  | 4 | 20 | Leon Wagner | Open | Dedicated connection upgrade ordered; delivery in 4 weeks. | 2026-11-28 |
| RAID-034 | Risk | Cut-over collides with month-end | 4 | 5 | 20 | Lena Hartmann | Open | Move cut-over by one week; confirm with Finance. | 2026-11-18 |
| RAID-035 | Risk | Cloud architect over-allocated | 4 | 4 | 16 | Lena Hartmann | Open | Backfill with contractor; defer design reviews on P05. | 2026-11-15 |
| RAID-036 | Dependency | Security baseline from P06 | 2 | 4 | 8 | Aylin Demir | Mitigating | Baseline v1 published; v2 due in November. | 2026-11-22 |

## P13 Finance Reporting Automation

| ID | Type | Title | Prob | Impact | Score | Owner | Status | Response | Due |
|---|---|---|---|---|---|---|---|---|---|
| RAID-037 | Risk | ERP source data changes after P01 go-live | 3 | 3 | 9 | Eva Maier | Open | Isolate source mappings in a configuration layer. | 2026-12-15 |
| RAID-038 | Assumption | Finance users can attend design workshops | 2 | 2 | 4 | Nadine Roth | Open | Review after month-end. | 2026-11-30 |

## P14 Customer Support Chatbot

| ID | Type | Title | Prob | Impact | Score | Owner | Status | Response | Due |
|---|---|---|---|---|---|---|---|---|---|
| RAID-039 | Issue | Answer accuracy below target |  | 4 | 20 | Anna Köhler | Escalated | Improve retrieval and prompt design; limit scope to top-20 intents. | 2026-11-20 |
| RAID-040 | Issue | LLM usage costs above forecast |  | 4 | 20 | Karim Aziz | Open | Response caching and model tiering; cost cap per conversation. | 2026-11-18 |
| RAID-041 | Risk | Scope creep: voice channel | 5 | 4 | 20 | Anna Köhler | Open | Route through change control; defer to phase 2. | 2026-11-12 |
| RAID-042 | Risk | Training data privacy review | 4 | 4 | 16 | Sara Haddad | Mitigating | Anonymise transcripts; legal review scheduled. | 2026-11-25 |

## P15 Supplier Portal

| ID | Type | Title | Prob | Impact | Score | Owner | Status | Response | Due |
|---|---|---|---|---|---|---|---|---|---|
| RAID-044 | Dependency | Vendor master data from P01 | 3 | 3 | 9 | Julia Neumann | Open | Interim extract from legacy system. | 2026-11-25 |
| RAID-043 | Risk | Supplier onboarding adoption | 2 | 3 | 6 | Julia Neumann | Open | Onboarding webinars; paper fallback for 6 months. | 2026-12-01 |
| RAID-045 | Issue | Invoice PDF layout bug |  | 1 | 5 | Oskar Lang | Closed | Fixed in release 0.9.4. | 2026-10-12 |
