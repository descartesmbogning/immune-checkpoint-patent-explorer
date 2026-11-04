import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Output, callback, html

import components as c
import data
from theme import STATUS_COLORS, mark_incomplete

dash.register_page(__name__, path="/", name="Overview", order=0)

layout = html.Div([
    c.page_header(
        "Immune checkpoint therapy patents, 1997–2023",
        "Who files patents on PD-1, PD-L1, CTLA-4 and newer checkpoint targets, where, and for what. "
        "Use the filters above; every page updates."),
    dbc.Row(id="ov-kpis", className="g-3 mb-3"),
    c.card(c.graph("ov-trend", 440), "Patent documents by application year and legal status",
           "Shaded years are incomplete in this January 2024 export, so the drop after 2021 is not a real decline."),
    c.card(html.Div(id="ov-findings"), "What the data show"),
])


@callback(Output("ov-kpis", "children"), Output("ov-trend", "figure"), Output("ov-findings", "children"),
          *c.FILTER_INPUTS)
def update(years, statuses, targets, strategies, types):
    p = data.filter_patents(years, statuses, targets, strategies, types)
    if p.empty:
        return [c.kpi("0", "documents")], c.empty_figure(), "No documents match these filters."

    ids = set(p.lens_id)
    apps = data.APPLICANTS[data.APPLICANTS.lens_id.isin(ids)]
    cty = data.COUNTRIES[data.COUNTRIES.lens_id.isin(ids)]
    granted = (p.status == "Granted / in force").mean() * 100
    orgs = apps.loc[apps.type != "Individual", "applicant"].nunique()

    # China's share in the last two complete years vs five years earlier
    def share(country, y0, y1):
        sub = p[p.year.between(y0, y1)]
        if sub.empty:
            return None
        return 100 * cty[cty.lens_id.isin(sub.lens_id) & (cty.country == country)].lens_id.nunique() / len(sub)

    cn_now, cn_then = share("China", 2020, 2021), share("China", 2015, 2016)
    kpis = [
        c.kpi(f"{len(p):,}", "patent documents"),
        c.kpi(f"{granted:.0f}%", "granted or in force", f"{(p.status == 'Pending application').mean()*100:.0f}% pending"),
        c.kpi(f"{orgs:,}", "organisations filing"),
        c.kpi(f"{cty.country.nunique()}", "applicant countries"),
        c.kpi(f"{cn_now:.0f}%" if cn_now is not None else "–", "with a Chinese applicant, 2020–21",
              f"{cn_then:.0f}% in 2015–16" if cn_then is not None else None),
    ]

    yearly = p.groupby(["year", "status"]).size().reset_index(name="Documents")
    fig = px.bar(yearly, x="year", y="Documents", color="status", color_discrete_map=STATUS_COLORS,
                 category_orders={"status": data.STATUSES},
                 labels={"year": "Application year", "status": "Legal status"})
    fig.update_layout(bargap=0.15, legend=dict(orientation="h", y=1.08, x=0))
    if p.year.max() > data.LAST_COMPLETE_YEAR:
        mark_incomplete(fig)

    # Plain-language findings, computed from the current selection
    top_org = (apps[apps.type != "Individual"].groupby("applicant").lens_id.nunique().sort_values(ascending=False))
    top_cty = cty.groupby("country").lens_id.nunique().sort_values(ascending=False)
    tgt = p.target_list.explode().value_counts()
    strat = p.strategy_list.explode().value_counts()
    peak = p[p.year <= data.LAST_COMPLETE_YEAR].groupby("year").size()
    items = []
    if not peak.empty:
        items.append(f"Filing grew fast after 2014; among complete years the busiest was {peak.idxmax()} "
                     f"with {peak.max():,} documents.")
    if len(top_cty) >= 2:
        items.append(f"{top_cty.index[0]} ({top_cty.iloc[0]:,}) and {top_cty.index[1]} ({top_cty.iloc[1]:,}) "
                     f"are the leading applicant countries.")
    if not top_org.empty:
        items.append(f"The most active organisation is {top_org.index[0]} with {top_org.iloc[0]:,} documents.")
    if "PD-1" in tgt:
        newer = sum(tgt.get(k, 0) for k in ("LAG-3", "TIM-3", "TIGIT"))
        items.append(f"PD-1 is named in {tgt['PD-1']:,} documents; LAG-3, TIM-3 and TIGIT together in {newer:,}.")
    if "Combination therapy" in strat:
        items.append(f"{100*strat['Combination therapy']/len(p):.0f}% of documents describe a combination therapy.")
    return kpis, fig, html.Ul([html.Li(i) for i in items], className="findings")
