import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Output, callback, html

import components as c
import data
from theme import CATEGORICAL, mark_incomplete

dash.register_page(__name__, path="/science-links", name="Science links", order=5)

layout = html.Div([
    c.page_header("Science links and influence",
                  "Two signals in the patent record: how often a patent cites research papers (its link to "
                  "science) and how often later patents cite it (its influence on later inventions)."),
    dbc.Row([
        dbc.Col(c.card(c.graph("sci-npl", 420), "Share of documents that cite research papers",
                       "Older documents have had more time to collect examiner citations."), lg=6),
        dbc.Col(c.card(c.graph("sci-bins", 420), "Documents by number of research papers cited"), lg=6),
    ], className="g-3"),
    c.card(c.table("sci-table"), "Most-cited documents (cited by later patents)",
           "Citations favour older documents; compare documents filed in the same years."),
])

BINS = [-1, 0, 5, 20, 50, 10_000]
BIN_LABELS = ["None", "1–5", "6–20", "21–50", "More than 50"]


@callback(Output("sci-npl", "figure"), Output("sci-bins", "figure"),
          Output("sci-table", "data"), Output("sci-table", "columns"), *c.FILTER_INPUTS)
def update(years, statuses, targets, strategies, types):
    p = data.filter_patents(years, statuses, targets, strategies, types)
    if p.empty:
        return c.empty_figure(), c.empty_figure(), [], []
    y = p[p.year >= max(data.SHARE_START, int(p.year.min()))].groupby("year").agg(
        share=("npl_citations", lambda s: 100 * (s > 0).mean()), n=("lens_id", "size")).reset_index()
    fig = px.line(y, x="year", y="share", markers=True, hover_data={"n": True},
                  labels={"year": "Application year", "share": "Documents citing papers (%)", "n": "Documents"},
                  color_discrete_sequence=[CATEGORICAL[1]])
    fig.update_yaxes(range=[0, 100])
    if p.year.max() > data.LAST_COMPLETE_YEAR:
        mark_incomplete(fig, label="Incomplete")

    b = pd.cut(p.npl_citations, BINS, labels=BIN_LABELS).value_counts().reindex(BIN_LABELS).reset_index()
    b.columns = ["Research papers cited", "Documents"]
    fig2 = px.bar(b, x="Research papers cited", y="Documents", color_discrete_sequence=[CATEGORICAL[0]])

    top = p.sort_values("cited_by_patents", ascending=False).head(100).copy()
    apps = (data.APPLICANTS[data.APPLICANTS.lens_id.isin(top.lens_id)].groupby("lens_id").applicant
            .agg(lambda s: ", ".join(s.head(3))))
    top["Applicants"] = top.lens_id.map(apps)
    top["Title"] = [f"[{t[:140]}]({u})" for t, u in zip(top.title, top.url)]
    out = top.rename(columns={"year": "Year", "jurisdiction": "Office", "cited_by_patents": "Cited by patents",
                              "npl_citations": "Papers cited", "status": "Status"})[
        ["Title", "Applicants", "Year", "Office", "Status", "Cited by patents", "Papers cited"]]
    return fig, fig2, out.to_dict("records"), c.table_columns(out, link_cols=("Title",))
