# Business Case - AI Project Portfolio Control Tower

> All figures are **illustrative assumptions** for a fictional company. Replace them with your organisation's data before using this for a real decision. The arithmetic is reproducible from the tables below.

## 1. Problem
- 15 projects, EUR 9.55M budget, no consolidated view.
- Status is compiled by hand; delays and overruns surface late.
- In the sample portfolio (as of 31 Oct 2026) the forecast is EUR 10.55M, which is **EUR 1.0M (10.5%) over budget**, with six projects meeting escalation rules and six people above 110% allocation. These problems existed before anyone saw them together.

## 2. Options
| Option | Description | Verdict |
|---|---|---|
| A. Do nothing | Keep manual reporting | Overruns keep surfacing late; reporting effort stays |
| B. Buy a PPM suite | Commercial portfolio tool | Higher licence cost and long implementation; more than needed for 15 projects |
| **C. Build a lightweight Control Tower** | Excel + Python + Power BI + LLM report | **Recommended**: low cost, fast, reuses existing Microsoft licences, extensible |

## 3. Costs
**One-off**
| Item | Calculation | EUR |
|---|---|---|
| PMO analyst | 30 days x 600 | 18,000 |
| BI developer | 25 days x 700 | 17,500 |
| Data / Python engineer | 20 days x 750 | 15,000 |
| Project manager | 12 days x 700 | 8,400 |
| **Total one-off** | | **58,900** |

**Annual run**
| Item | Calculation | EUR |
|---|---|---|
| Power BI Pro licences | 10 users x 14 x 12 | 1,680 |
| LLM API usage | 50 per month x 12 | 600 |
| Support | 5 days x 700 | 3,500 |
| **Total per year** | | **5,780** |

## 4. Benefits (per year)
| Benefit | Assumption | Base case EUR | Conservative EUR |
|---|---|---|---|
| Reporting effort saved | 15 projects x 0.75 day saved x 12 months = 135 days at EUR 600 (conservative: half) | 81,000 | 40,500 |
| Earlier intervention reduces overruns | Base: 10% of the EUR 998,580 forecast overrun avoided; conservative: 5% | 99,858 | 49,929 |
| **Total** | | **180,858** | **90,429** |

Not quantified: better steering decisions, fewer surprises for sponsors, transparency about shared resources.

## 5. Financial summary (3 years, undiscounted)
| | Base | Conservative |
|---|---|---|
| Total cost (58,900 + 3 x 5,780) | 76,240 | 76,240 |
| Total benefit | 542,574 | 271,287 |
| Net benefit | 466,334 | 195,047 |
| ROI | 612% | 256% |
| Payback | 4.0 months | 8.3 months |

Sensitivity: the case stays positive unless benefits fall below roughly 14% of the base estimate, so the decision is not fragile to the assumptions. The largest uncertainty is the overrun-avoided percentage, which should be tracked after go-live.

## 6. Risks to the benefits
Poor data quality (mitigation: data-validation rules and owner sign-off), low adoption by project managers (mitigation: reduce their reporting burden, not add to it), AI text containing errors (mitigation: calculations outside the model, automatic number check, human review).

## 7. Recommendation
Approve Option C with a budget of EUR 58,900 and a first release in 8 weeks, and review benefits after one quarter of use.
