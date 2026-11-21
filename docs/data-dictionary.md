# Data dictionary

All data is **synthetic**. Source: `data/portfolio_dataset.xlsx` (same tables in `data/csv/`). Reporting date: 31 Oct 2026.

## Projects (`projects.csv`)
| Column | Meaning |
|---|---|
| project_id | P01 to P15 |
| project_name, department, project_manager, sponsor, methodology | Descriptive fields (Agile, Waterfall, Hybrid) |
| start_date, planned_end_date, as_of_date | Baseline schedule and reporting date |
| budget_eur | Approved budget (BAC) |
| actual_cost_eur | Cost to date (AC) |
| actual_pct_complete | Reported progress, 0-100 |
| description | One-line description |

## RAID (`raid.csv`)
| Column | Meaning |
|---|---|
| raid_id, project_id | Keys |
| type | Risk, Assumption, Issue, Dependency |
| title, description, response, owner | Content |
| probability | 1-5 (blank for issues) |
| impact | 1-5; for issues this is the severity (5 critical, 4 high, 3 medium, 2-1 low) |
| score | Risk, assumption and dependency: probability x impact. Issue: severity x 5 |
| status | Open, Mitigating, Escalated, Closed |
| due_date, raised_date | Dates |

## Resources and allocations
`resources.csv`: resource_id, name, role, department, capacity_fte. `allocations.csv`: resource_id, project_id, allocation_fte. Utilisation = sum of a person's allocation / capacity.

## Monthly progress (`monthly_progress.csv`)
Month-end snapshots per project: planned_pct_complete, actual_pct_complete, actual_cost_eur. Used for SPI and CPI trends.

## Calculated (`data/processed/project_metrics.csv`)
bac, pv, ev, ac, spi, cpi, eac (forecast cost), forecast_end_date, slip_days, forecast_overrun_pct, risk_exposure, issue_penalty, five component scores, health_score, rag, escalate, escalation_reasons.

## Formulas
PV = BAC x planned %; EV = BAC x actual %; SPI = EV / PV; CPI = EV / AC; EAC = BAC / CPI (CPI floored at 0.3).
