"""Immune Checkpoint Patents Explorer — Dash entry point.

Local:  python app.py            (http://127.0.0.1:8050)
Render: gunicorn app:server      (see render.yaml)
"""
import os

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html

import theme  # noqa: F401  (registers the CognosX Plotly template)
import components as c
import data

FONTS = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, FONTS],
    suppress_callback_exceptions=True,
    title="Immune Checkpoint Patents Explorer",
    update_title=None,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"},
               {"name": "description", "content": "Who patents immune checkpoint therapies, where, and on what: "
                                                  "an interactive view of 3,320 patent documents from Lens.org."}],
)
app._favicon = "favicon.png"
server = app.server

app.layout = html.Div([
    dcc.Location(id="url"),
    c.navbar(),
    c.filter_panel(),
    dbc.Container(dash.page_container, fluid=True, className="page-body"),
    c.footer(),
])


@app.callback(Output("nav-collapse", "is_open"), Input("nav-toggler", "n_clicks"),
              State("nav-collapse", "is_open"), prevent_initial_call=True)
def toggle_nav(n, is_open):
    return not is_open


@app.callback(Output("filter-collapse", "is_open"), Input("filter-toggle", "n_clicks"),
              State("filter-collapse", "is_open"), prevent_initial_call=True)
def toggle_filters(n, is_open):
    return not is_open


@app.callback(Output("filter-panel", "style"), Input("url", "pathname"))
def hide_filters_on_about(path):
    return {"display": "none"} if path == "/about" else {}


@app.callback(Output("filter-summary", "children"), *c.FILTER_INPUTS)
def summarise_filters(years, statuses, targets, strategies, types):
    n = len(data.filter_patents(years, statuses, targets, strategies, types))
    msg = f"{n:,} of {len(data.PATENTS):,} documents match."
    if years and years[1] > data.LAST_COMPLETE_YEAR:
        msg += f" Years after {data.LAST_COMPLETE_YEAR} are incomplete: patents publish about 18 months after filing."
    return msg


if __name__ == "__main__":
    app.run(debug=os.environ.get("DEBUG", "0") == "1", host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))
