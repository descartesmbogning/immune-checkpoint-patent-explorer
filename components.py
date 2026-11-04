"""Shared layout pieces: navigation, global filters, number cards, tables, footer."""
import dash_bootstrap_components as dbc
from dash import Input, dash_table, dcc, html

import data

PAGES = [
    ("Overview", "/"),
    ("Organisations", "/organisations"),
    ("Countries", "/countries"),
    ("Technologies", "/technologies"),
    ("Filing offices", "/filing-offices"),
    ("Science links", "/science-links"),
    ("Inventors", "/inventors"),
    ("About", "/about"),
]


def navbar():
    return dbc.Navbar(
        dbc.Container([
            html.A(html.Div([
                html.Span("Immune Checkpoint Patents", className="brand-title"),
                html.Span("Explorer", className="brand-sub"),
            ], className="brand"), href="/", style={"textDecoration": "none"}),
            dbc.NavbarToggler(id="nav-toggler"),
            dbc.Collapse(
                dbc.Nav([dbc.NavItem(dbc.NavLink(name, href=href, active="exact")) for name, href in PAGES],
                        className="ms-auto", navbar=True),
                id="nav-collapse", navbar=True),
        ], fluid=True),
        color="#0a0a0a", dark=True, sticky="top", className="navbar-cx",
    )


def filter_panel():
    """One filter bar shared by all pages; each page listens to these ids."""
    def dd(id_, label, options, placeholder):
        return dbc.Col([
            dbc.Label(label, html_for=id_, className="filter-label"),
            dcc.Dropdown(id=id_, options=options, multi=True, placeholder=placeholder),
        ], xs=12, md=6, lg=3)

    return html.Div(dbc.Container([
        dbc.Button("Filters", id="filter-toggle", color="light", size="sm", className="filter-toggle d-lg-none mb-2"),
        dbc.Collapse(html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Label("Application years", className="filter-label"),
                dcc.RangeSlider(id="f-years", min=data.YEAR_MIN, max=data.YEAR_MAX, step=1,
                                value=[2010, data.YEAR_MAX], allowCross=False,
                                marks={y: str(y) for y in range(2000, data.YEAR_MAX + 1, 5)} | {data.YEAR_MAX: str(data.YEAR_MAX)},
                                tooltip={"placement": "bottom", "always_visible": False}),
            ], xs=12, lg=12, className="mb-2"),
        ]),
        dbc.Row([
            dd("f-status", "Legal status", data.STATUSES, "All statuses"),
            dd("f-targets", "Checkpoint target", data.TARGETS, "All targets"),
            dd("f-strategies", "Strategy", data.STRATEGIES, "All strategies"),
            dd("f-types", "Applicant type", data.APPLICANT_TYPES, "All applicant types"),
        ], className="g-3"),
        ]), id="filter-collapse", is_open=False),
        html.Div(id="filter-summary", className="filter-summary"),
    ], fluid=True), id="filter-panel", className="filter-panel")


FILTER_INPUTS = [Input("f-years", "value"), Input("f-status", "value"), Input("f-targets", "value"),
                 Input("f-strategies", "value"), Input("f-types", "value")]


def page_header(title, lead):
    return html.Div([html.H1(title), html.P(lead, className="lead-text")], className="page-header")


def kpi(value, label, note=None):
    return dbc.Col(html.Div([
        html.Div(value, className="kpi-value"),
        html.Div(label, className="kpi-label"),
        html.Div(note, className="kpi-note") if note else None,
    ], className="kpi"), xs=6, md=4, lg=True)


def card(children, title=None, note=None):
    return html.Div([
        html.H2(title, className="card-title-cx") if title else None,
        children,
        html.P(note, className="chart-note") if note else None,
    ], className="card-cx")


def graph(id_, height=420):
    return dcc.Loading(dcc.Graph(id=id_, config={"displaylogo": False, "toImageButtonOptions": {"scale": 3}},
                                 style={"height": f"{height}px"}), type="circle", color="#C98000")


def table(id_, page_size=15):
    return dash_table.DataTable(
        id=id_, page_size=page_size, sort_action="native", filter_action="native",
        export_format="csv", export_headers="display", markdown_options={"link_target": "_blank"},
        style_table={"overflowX": "auto"},
        style_cell={"fontFamily": "Inter, Arial, sans-serif", "fontSize": 13, "padding": "6px 10px",
                    "textAlign": "left", "border": "none", "borderBottom": "1px solid #e6e3dd",
                    "maxWidth": 360, "whiteSpace": "normal", "height": "auto"},
        style_header={"fontWeight": 600, "backgroundColor": "#f7f5f0", "borderBottom": "2px solid #e6e3dd"},
        style_filter={"backgroundColor": "#ffffff"},
        style_data_conditional=[{"if": {"state": "active"}, "backgroundColor": "#fbe9c7", "border": "none"}],
    )


def table_columns(df, link_cols=()):
    return [{"name": c, "id": c, "presentation": "markdown"} if c in link_cols
            else {"name": c, "id": c, "type": "numeric" if df[c].dtype.kind in "if" else "text"}
            for c in df.columns]


def empty_figure(message="No documents match these filters."):
    import plotly.graph_objects as go
    fig = go.Figure()
    fig.add_annotation(text=message, showarrow=False, font=dict(size=14, color="#5c5c5c"))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig


def footer():
    return html.Footer(dbc.Container(html.Small([
        f"Data: Lens.org patent export of {data.DATA_DATE} · Analysis: Maxime Descartes Mbogning Fonkou · ",
        html.A("CognosX", href="https://cognosx.ca", target="_blank"),
        " · ", html.A("Methods and limits", href="/about"),
    ]), fluid=True), className="footer-cx")
