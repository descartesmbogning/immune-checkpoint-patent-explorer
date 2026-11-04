import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Output, callback, html

import components as c
import data
from theme import CATEGORICAL, NEUTRAL, SEQUENTIAL

dash.register_page(__name__, path="/filing-offices", name="Filing offices", order=4)

OFFICE_COLORS = {"National office": CATEGORICAL[0], "International (PCT)": CATEGORICAL[1],
                 "Regional office": CATEGORICAL[3]}

layout = html.Div([
    c.page_header("Filing offices",
                  "Where protection is sought: national patent offices, the international PCT route (WO) "
                  "and regional offices such as the EPO. This shows target markets, not where inventors work."),
    dbc.Row([
        dbc.Col(c.card(c.graph("jur-bar", 520), "Documents by filing office"), lg=5),
        dbc.Col(c.card(c.graph("jur-heat", 520), "Top 8 offices by application year"), lg=7),
    ], className="g-3"),
    c.card(c.table("jur-table"), "All filing offices"),
])


@callback(Output("jur-bar", "figure"), Output("jur-heat", "figure"),
          Output("jur-table", "data"), Output("jur-table", "columns"), *c.FILTER_INPUTS)
def update(years, statuses, targets, strategies, types):
    p = data.filter_patents(years, statuses, targets, strategies, types)
    if p.empty:
        return c.empty_figure(), c.empty_figure(), [], []
    j = p.merge(data.JURISDICTIONS, left_on="jurisdiction", right_on="code", how="left")
    t = (j.groupby(["name", "office_type", "region"], dropna=False)
         .agg(Documents=("lens_id", "nunique"),
              Granted=("status", lambda s: int((s == "Granted / in force").sum())),
              Citations=("cited_by_patents", "sum"), **{"First year": ("year", "min"), "Last year": ("year", "max")})
         .reset_index().sort_values("Documents", ascending=False))
    t["Share (%)"] = (100 * t.Documents / len(p)).round(2)

    top = t.head(15).iloc[::-1]
    fig = px.bar(top, x="Documents", y="name", color="office_type", orientation="h",
                 color_discrete_map=OFFICE_COLORS, labels={"name": "", "office_type": "Office type"})
    fig.update_layout(yaxis=dict(categoryorder="array", categoryarray=top.name.tolist()),
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0), margin=dict(t=90))

    top8 = t.name.head(8).tolist()
    h = j[j.name.isin(top8) & (j.year >= max(2010, int(p.year.min())))].groupby(["name", "year"]).size()
    yrs = list(range(max(2010, int(p.year.min())), int(p.year.max()) + 1))
    piv = h.unstack(fill_value=0).reindex(index=top8, columns=yrs).fillna(0).astype(int)
    fig2 = px.imshow(piv, color_continuous_scale=["#ffffff"] + SEQUENTIAL, aspect="auto", text_auto=True,
                     labels=dict(x="Application year", y="", color="Documents"))
    fig2.update_traces(textfont_size=10)
    fig2.update_layout(coloraxis_showscale=False)

    out = t.rename(columns={"name": "Office", "office_type": "Type", "region": "Region"})
    return fig, fig2, out.to_dict("records"), c.table_columns(out)
