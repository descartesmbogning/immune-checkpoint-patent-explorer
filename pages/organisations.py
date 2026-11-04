import urllib.parse

import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Output, callback, html

import components as c
import data
from theme import TYPE_COLORS, mark_incomplete

dash.register_page(__name__, path="/organisations", name="Organisations", order=1)

layout = html.Div([
    c.page_header("Organisations",
                  "Companies, universities, hospitals and research institutes that file the patents. "
                  "Individuals named as applicants are counted in the type mix but left out of the ranking."),
    dbc.Row([
        dbc.Col(c.card(c.graph("org-top", 560), "Top 20 organisations by number of documents"), lg=7),
        dbc.Col(c.card(c.graph("org-mix", 560), "Who files: share of documents by applicant type",
                       "A document with applicants of two types counts for both."), lg=5),
    ], className="g-3"),
    c.card(c.table("org-table"), "All organisations",
           "Class compares each organisation's first and last filing year with the last year selected. "
           "Centrality comes from the co-applicant network in the full dataset. Use the column filters "
           "(for example >10) and the Export button."),
])


def lens_link(name):
    q = urllib.parse.quote(f'applicant.name:"{name}"')
    return f"[{name}](https://www.lens.org/lens/search/patent/list?q={q})"


@callback(Output("org-top", "figure"), Output("org-mix", "figure"),
          Output("org-table", "data"), Output("org-table", "columns"), *c.FILTER_INPUTS)
def update(years, statuses, targets, strategies, types):
    p = data.filter_patents(years, statuses, targets, strategies, types)
    if p.empty:
        return c.empty_figure(), c.empty_figure(), [], []
    ref = int(p.year.max())
    apps = data.APPLICANTS[data.APPLICANTS.lens_id.isin(p.lens_id)]
    orgs = apps[apps.type != "Individual"]

    t = data.entity_table(orgs, p, "applicant", ref, extra=["country", "type"], network=data.ORG_NET)
    top = t.head(20).iloc[::-1]
    fig = px.bar(top, x="Documents", y="applicant", color="type", orientation="h",
                 color_discrete_map=TYPE_COLORS, hover_data=["country", "Citations", "First year", "Last year"],
                 labels={"applicant": "", "type": "Applicant type"})
    fig.update_layout(yaxis=dict(categoryorder="array", categoryarray=top.applicant.tolist()),
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0), margin=dict(t=90))

    mix = (apps.merge(p[["lens_id", "year"]], on="lens_id").drop_duplicates(["lens_id", "type"])
           .groupby(["year", "type"]).size().reset_index(name="n"))
    totals = p.groupby("year").size()
    mix["Share of documents (%)"] = 100 * mix.n / mix.year.map(totals)
    mix = mix[mix.year >= max(data.SHARE_START, int(p.year.min()))]
    fig2 = px.line(mix, x="year", y="Share of documents (%)", color="type", markers=True,
                   color_discrete_map=TYPE_COLORS, category_orders={"type": data.APPLICANT_TYPES},
                   labels={"year": "Application year", "type": "Applicant type"})
    fig2.update_layout(legend=dict(orientation="h", y=1.06, x=0))
    if p.year.max() > data.LAST_COMPLETE_YEAR:
        mark_incomplete(fig2, label="Incomplete")

    out = t.rename(columns={"applicant": "Organisation", "country": "Country", "type": "Type"})
    out["Organisation"] = out["Organisation"].map(lens_link)
    return fig, fig2, out.to_dict("records"), c.table_columns(out, link_cols=("Organisation",))
