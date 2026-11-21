# Power BI dashboard - build kit

> **Honest note:** a `.pbix` file can only be created inside Power BI Desktop (Windows), so it is not included
> as a binary. Everything needed to build it in about 45 minutes is here: loading queries, the data model,
> every DAX measure, a theme and a page-by-page layout. The same KPIs and charts are already working in the
> web dashboard at the repo root (`index.html`, screenshots in `../screenshots/`), so you can compare your
> Power BI report against it. When finished, save your report as `powerbi/AI-Portfolio-Control-Tower.pbix`
> and put screenshots of each page in `powerbi/screenshots/`.

## 1. Load the data
1. Open Power BI Desktop > **Home > Transform data > Manage Parameters > New**. Name `DataFolder`, type Text, value = full path of the repo's `data` folder.
2. Create five blank queries with the code in [`power-query.m`](power-query.m): `project_metrics`, `raid`, `monthly_trend`, `resource_utilisation`, `allocations`.
3. **Close & Apply**.

> Run `python src/run_pipeline.py` first so `data/processed/*.csv` exist (they are also committed in this repo).

## 2. Model (Model view)
| From (one) | To (many) | Column |
|---|---|---|
| `project_metrics` | `raid` | `project_id` |
| `project_metrics` | `monthly_trend` | `project_id` |
| `project_metrics` | `allocations` | `project_id` |
| `resource_utilisation` | `allocations` | `resource_id` |

All relationships: single direction, one-to-many. Sort `project_metrics[rag]` by a helper column (Red=1, Amber=2, Green=3) if you want Red first.

## 3. Measures
Create an empty table `_Measures`, then add every measure from [`measures.dax`](measures.dax).

## 4. Theme
**View > Themes > Browse for themes** and choose [`theme.json`](theme.json).

## 5. Pages
**Page 1 - Executive overview**
- Top row of 5 cards: `Avg Health Score` (large), `Forecast Overrun EUR`, `SPI`, `CPI`, `Projects Needing Escalation`.
- Card with the `Headline` measure.
- Table of `project_metrics`: project_name, department, `RAG Label`, health_score, spi, cpi, slip_days, forecast_overrun_pct. Conditional formatting: background colour from `RAG Colour` on the status column; red font where spi < 0.8 or cpi < 0.85. Sort by health_score ascending.
- Slicers: department, rag.

**Page 2 - Budget and schedule variance**
- Clustered bar: project_name vs `Forecast Overrun %` (sorted descending).
- Clustered bar: project_name vs `Max Slip Days`.
- Scatter: x = `SPI`, y = `CPI`, size = `Budget (BAC)`, details = project_name. Add constant lines at 1.0 on both axes - bottom-left quadrant is the danger zone.

**Page 3 - Project drill-through**
- Create the page, drag `project_id` into **Drill through**.
- Line chart: `monthly_trend[month_end]` on axis, values `SPI Trend` and `CPI Trend`; constant line at 1.
- Card visuals for the five health sub-scores (use `project_metrics[score_schedule]` etc., aggregation Average).
- Table: top open `raid` items (filter status is not Closed), sorted by score.

**Page 4 - Risks and issues**
- Matrix: rows `raid[impact]` (descending), columns `raid[probability]`, values count of `raid_id`, filter type = Risk and status is not Closed, conditional background colour by value.
- Table: all open `raid` rows with score >= 15.
- Cards: `Open Risks`, `Open Issues`, `Critical Issues`, `Risk Exposure`.

**Page 5 - Resources**
- Bar chart: `resource_utilisation[name]` vs `utilisation_pct`, with constant lines at 100 and 110; colour by `status`.
- Matrix: rows = resource name, columns = project_id, values = sum of `allocation_fte` (shows who is shared across troubled projects).
- Cards: `Over-allocated People`, `Stretched People`.

**Page 6 - AI report**
- Text box containing the executive summary pasted from `reports/executive-status-report-2026-10.md` (or refresh it after running the pipeline with your own API key).

## 6. Accessibility checklist
- Each visual has alt text (Format > General > Alt text).
- Status is shown with text and icon (`RAG Label`), not colour alone.
- Check **View > Show gridlines / tab order** so keyboard order is logical.

## 7. Publish
Save as `AI-Portfolio-Control-Tower.pbix`. The free Power BI service cannot embed publicly without a licence, so use screenshots in the repo and the web dashboard for the live demo.
