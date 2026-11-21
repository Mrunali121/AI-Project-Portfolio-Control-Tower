# Executive Status Report - October 2026

**Portfolio:** Meridian Works GmbH IT portfolio (fictional) · **Status as of:** 31 Oct 2026 · **Audience:** IT Steering Committee

> **How this report was produced.** Written by an LLM (Claude) from `outputs/portfolio_facts.json`, following the rules in
> `prompts/executive_report_prompt.md`. All figures were calculated by `src/metrics.py`, not by the model, and the text was
> checked with `verify_numbers()` in `src/report_generator.py` (no figure in this report is missing from the facts).
> The data is synthetic. To regenerate with your own key: `python src/run_pipeline.py --provider anthropic` (or `openai`).

## Portfolio at a glance

The portfolio of 15 projects has a combined budget of EUR 9.55M and an average health score of 67 out of 100 (weighted by budget). Eight projects are Green, five are Amber and two are Red. At the current pace the portfolio will cost EUR 10.55M, about EUR 1.0M (10.5%) more than planned, and it is delivering work more slowly than planned (portfolio SPI 0.84) while spending slightly ahead of the value produced (portfolio CPI 0.91). Six projects meet the escalation rules. Ten people are loaded beyond their capacity, and the same few specialists appear on most of the struggling projects, so the delays are connected rather than independent.

## Projects needing executive attention

### P01 ERP Finance Migration - health 43 (Red)

This is the portfolio's most serious problem. The project is 58% complete against 86% planned (SPI 0.68, CPI 0.84). At the current pace it finishes on 30 May 2027, 163 days after the planned date of 18 Dec 2026, and it is forecast to cost EUR 2.16M against a EUR 1.80M budget, an overrun of EUR 355k (19.7%). It meets every escalation trigger: Red health score, SPI and CPI below their thresholds, a forecast slip above 30 days and an open critical issue. The critical issue is the failed ledger data migration reconciliation (owner Lena Hartmann, already escalated). Behind it sit two further high-scoring risks: the cut-over overlapping the Finance year-end close, and the end of the ERP consultants' contract in December. Because the CRM (P07), supplier portal (P15) and reporting automation (P13) projects depend on ERP data, this delay will spread.

**Recommendation**
- Lena Hartmann: bring a decision on a third trial load and the data-cleansing squad to the next steering meeting.
- Lena Hartmann: agree a new baseline or reduced first-release scope, because the current end date is no longer credible. This is a judgement call for the sponsor (CFO).
- Resource owners: protect Jonas Keller (140% utilised across four projects) for the schema work this project depends on.

### P14 Customer Support Chatbot - health 50 (Red)

The chatbot is 40% complete against 54% planned (SPI 0.74, CPI 0.78) and is forecast to finish on 26 May 2027, 89 days late, at EUR 538k against a EUR 420k budget (EUR 118k, 28.0% over). That is the largest percentage overrun in the portfolio. The top open items are answer accuracy below target, LLM usage cost above forecast and scope creep from an unapproved voice-channel request, each scoring 20. The project manager, Anna Köhler, is allocated at 150% across four projects, which makes it hard to hold scope and quality at the same time.

**Recommendation**
- Anna Köhler: route the voice-channel request through change control and defer it to a later phase.
- Karim Aziz: introduce cost caps and response caching, and report usage cost weekly until it is back inside the forecast.
- Sponsor (COO): decide whether to continue with a reduced intent scope or pause until the accuracy issue is resolved. This is a judgement call.

### P04 Warehouse Management System Upgrade - health 56 (Amber)

The upgrade is 50% complete against 65% planned (SPI 0.77, CPI 0.87), forecast to finish on 29 Jul 2027, 125 days late, with a forecast overrun of EUR 180k (15.0%). The scanner firmware is incompatible with the new system version and no vendor patch is available yet. The only database administrator, Jonas Keller, is at 140%, which delays the schema migration, and the go-live is planned during the annual stock-take.

**Recommendation**
- Emre Yilmaz: escalate the firmware problem to the vendor and keep the interim workaround in place.
- Emre Yilmaz: move the go-live outside the stock-take window or run a pilot site first.
- Portfolio office: fund a contract DBA so the schema migration is not waiting on one person.

### P12 Cloud Migration Wave 2 - health 60 (Amber)

The project is 61% complete against 73% planned (SPI 0.84, CPI 0.88) and is forecast to finish on 22 Mar 2027, 59 days late, at EUR 1.25M against EUR 1.10M (EUR 146k, 13.3% over). Network latency above the service level and a cut-over weekend that collides with the financial month-end are the leading items. Cloud architect Sofia Lindqvist is at 120% and programme manager Lena Hartmann at 110%.

**Recommendation**
- Lena Hartmann: move the cut-over by one week and confirm it with Finance.
- Leon Wagner: deliver the upgraded network connection and report the latency result.
- Lena Hartmann: backfill the cloud architect role so design reviews on dependent projects are not deferred.

### P07 CRM Rollout for Sales - health 63 (Amber)

The rollout is 72% complete against 87% planned (SPI 0.83, CPI 0.90), forecast to finish on 28 Jan 2027, 55 days late, with an overrun of EUR 78k (11.1%). The main problem is people, not technology: low user adoption (escalated) and limited sales availability for acceptance testing during the quota season. It also depends on cleansed customer data from the ERP project (P01).

**Recommendation**
- Julia Neumann: ask the sales directors to make training attendance mandatory and appoint regional super-users.
- Julia Neumann: shorten acceptance testing to the critical flows and run evening sessions.

### P10 Predictive Maintenance Pilot - health 68 (Amber)

The pilot is 55% complete against 72% planned (SPI 0.77, CPI 0.90), forecast to finish on 8 Apr 2027, 83 days late, EUR 60k (11.1%) over budget. A sensor delivery slipped by six weeks (escalated) and early data quality is a concern for the model. Data engineer Ivan Petrov is at 120%.

**Recommendation**
- Emre Yilmaz: continue the sponsor escalation to the vendor and re-sequence the second pilot plant.
- Clara Fischer: report whether the data gaps are tolerable for modelling before more budget is spent. This is a judgement call.

## Watch list

- **P05 Data Platform Modernisation** (health 72, Amber, not escalated): SPI 0.94 and CPI 0.93, forecast 25 days late and EUR 70k over budget. It depends on the cloud landing zone from P12 and on extract access from source-system owners, so it will move if P12 slips.

## Resource conflicts

Six people are above 110% utilisation: Anna Köhler (150%, 4 projects), Jonas Keller (140%, 4 projects), and Sofia Lindqvist, Marco Rossi, Hannah Vogel and Ivan Petrov (120% each). Four more people are at 110%. The over-allocated people are concentrated on P01, P04, P12, P14 and P07, which are the projects with the largest delays. Reducing this overload is likely to help schedule more than adding budget.

## Decisions requested from the steering committee

1. P01: approve a re-baseline of the ERP Finance Migration, including whether to phase the go-live around the Finance year-end close.
2. P01 and P12: approve a contract extension for the ERP consultants and a contract cloud architect backfill.
3. P04: approve funding for a contract database administrator and agree to move the go-live outside the stock-take.
4. P14: decide between a reduced-scope continuation and a pause of the chatbot until accuracy is resolved.
5. Portfolio: set a rule that no person is planned above 110% across projects, and rebalance the six people above that line.
