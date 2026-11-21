// =====================================================================
// Power Query (M) - load the portfolio tables.
// Home > Transform data > New Source > Blank Query > Advanced Editor.
// Create one parameter first: Manage Parameters > New, name DataFolder, type Text,
// value = full path of the repo's data folder, e.g.  C:\Users\you\ai-portfolio-control-tower\data
// Then create one query per block below (name the query as in the comment).
// =====================================================================

// ---- query name: project_metrics ----
let
    Source   = Csv.Document(File.Contents(DataFolder & "\processed\project_metrics.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed    = Table.TransformColumnTypes(Promoted, {
        {"project_id", type text}, {"project_name", type text}, {"department", type text}, {"project_manager", type text},
        {"sponsor", type text}, {"methodology", type text}, {"rag", type text}, {"escalation_reasons", type text},
        {"start_date", type date}, {"planned_end_date", type date}, {"forecast_end_date", type date},
        {"bac", type number}, {"pv", type number}, {"ev", type number}, {"ac", type number}, {"eac", type number},
        {"spi", type number}, {"cpi", type number}, {"health_score", Int64.Type}, {"slip_days", Int64.Type},
        {"forecast_overrun_pct", type number}, {"actual_pct_complete", type number}, {"planned_pct_complete", type number},
        {"escalate", type logical}}, "en-US")
in
    Typed

// ---- query name: raid ----
let
    Source   = Csv.Document(File.Contents(DataFolder & "\csv\raid.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed    = Table.TransformColumnTypes(Promoted, {{"probability", Int64.Type}, {"impact", Int64.Type}, {"score", Int64.Type},
                                                      {"due_date", type date}, {"raised_date", type date}}, "en-US")
in
    Typed

// ---- query name: monthly_trend ----
let
    Source   = Csv.Document(File.Contents(DataFolder & "\processed\monthly_trend.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed    = Table.TransformColumnTypes(Promoted, {{"month_end", type date}, {"planned_pct_complete", type number}, {"actual_pct_complete", type number},
                                                      {"actual_cost_eur", type number}, {"ev", type number}, {"pv", type number},
                                                      {"spi", type number}, {"cpi", type number}}, "en-US")
in
    Typed

// ---- query name: resource_utilisation ----
let
    Source   = Csv.Document(File.Contents(DataFolder & "\processed\resource_utilisation.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed    = Table.TransformColumnTypes(Promoted, {{"capacity_fte", type number}, {"allocation_fte", type number}, {"utilisation_pct", Int64.Type}, {"projects", Int64.Type}}, "en-US")
in
    Typed

// ---- query name: allocations ----
let
    Source   = Csv.Document(File.Contents(DataFolder & "\csv\allocations.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed    = Table.TransformColumnTypes(Promoted, {{"allocation_fte", type number}}, "en-US")
in
    Typed
