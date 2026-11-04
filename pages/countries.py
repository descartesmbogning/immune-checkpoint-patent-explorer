import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Output, callback, html

import components as c
import data
from theme import CATEGORICAL, NEUTRAL, SEQUENTIAL, mark_incomplete

dash.register_page(__name__, path="/countries", name="Countries", order=2)

layout = html.Div([
    c.page_header("Applicant countries",
                  "Where the organisations and people who file the patents are based. "
                  "A document with applicants from two countries counts once for each."),
    dbc.Row([
        dbc.Col(c.card(c.graph("cty-map", 480), "Documents by applicant country"), lg=6),
        dbc.Col(c.card(c.graph("cty-share", 480), "Share of each year's documents: top 5 countries (from 2014)",
                       "Shares can add up to more than 100% because of international co-applicants."), lg=6),
    ], className="g-3"),
    c.card(c.table("cty-table"), "All applicant countries"),
])


@callback(Output("cty-map", "figure"), Output("cty-share", "figure"),
          Output("cty-table", "data"), Output("cty-table", "columns"), *c.FILTER_INPUTS)
def update(years, statuses, targets, strategies, types):
    p = data.filter_patents(years, statuses, targets, strategies, types)
    if p.empty:
        return c.empty_figure(), c.empty_figure(), [], []
    cty = data.COUNTRIES[data.COUNTRIES.lens_id.isin(p.lens_id)]
    t = data.entity_table(cty, p, "country", int(p.year.max()), extra=["region", "iso3"], network=data.CTY_NET)

    fig = px.choropleth(t, locations="iso3", color="Documents", hover_name="country",
                        hover_data={"iso3": False, "Documents": True, "Granted": True, "Share (%)": True},
                        color_continuous_scale=SEQUENTIAL, projection="natural earth")
    fig.update_geos(showframe=False, showcoastlines=False, landcolor="#f7f5f0", showcountries=True,
                    countrycolor="#e6e3dd")
    fig.update_layout(coloraxis_colorbar=dict(title="Documents", thickness=12, len=0.6))

    top5 = t.country.head(5).tolist()
    yr = (cty.merge(p[["lens_id", "year"]], on="lens_id").groupby(["year", "country"]).lens_id.nunique()
          .reset_index(name="n"))
    yr = yr[yr.country.isin(top5)]
    yr["Share of documents (%)"] = 100 * yr.n / yr.year.map(p.groupby("year").size())
    yr = yr[yr.year >= max(data.SHARE_START, int(p.year.min()))]
    cmap = {k: CATEGORICAL[i] if i < len(CATEGORICAL) else NEUTRAL for i, k in enumerate(top5)}
    fig2 = px.line(yr, x="year", y="Share of documents (%)", color="country", markers=True,
                   color_discrete_map=cmap, category_orders={"country": top5},
                   labels={"year": "Application year", "country": "Country"})
    fig2.update_layout(legend=dict(orientation="h", y=1.06, x=0))
    if p.year.max() > data.LAST_COMPLETE_YEAR:
        mark_incomplete(fig2, label="Incomplete")

    out = t.drop(columns=["iso3"]).rename(columns={"country": "Country", "region": "Region"})
    return fig, fig2, out.to_dict("records"), c.table_columns(out)
