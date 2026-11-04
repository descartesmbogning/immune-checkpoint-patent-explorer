import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Output, callback, html

import components as c
import data
from theme import CLASS_COLORS

dash.register_page(__name__, path="/inventors", name="Inventors", order=6)

layout = html.Div([
    c.page_header("Inventors", "The people named as inventors on the documents."),
    dbc.Alert(
        "Inventor names are not disambiguated. Common names (for example Li Jing or Wang Wei) may merge "
        "several different people, so treat rankings as indicative, not as profiles of individuals.",
        color="warning", className="note-alert"),
    c.card(c.graph("inv-top", 560), "Top 20 inventor names by number of documents"),
    c.card(c.table("inv-table"), "All inventor names"),
])


@callback(Output("inv-top", "figure"), Output("inv-table", "data"), Output("inv-table", "columns"),
          *c.FILTER_INPUTS)
def update(years, statuses, targets, strategies, types):
    p = data.filter_patents(years, statuses, targets, strategies, types)
    if p.empty:
        return c.empty_figure(), [], []
    inv = data.INVENTORS[data.INVENTORS.lens_id.isin(p.lens_id)]
    t = data.entity_table(inv, p, "inventor", int(p.year.max()))
    top = t.head(20).iloc[::-1]
    fig = px.bar(top, x="Documents", y="inventor", color="Class", orientation="h",
                 color_discrete_map=CLASS_COLORS, hover_data=["Citations", "First year", "Last year"],
                 labels={"inventor": ""})
    fig.update_layout(yaxis=dict(categoryorder="array", categoryarray=top.inventor.tolist()),
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, title="Activity class"), margin=dict(t=90))
    out = t.rename(columns={"inventor": "Inventor"})
    return fig, out.to_dict("records"), c.table_columns(out)
