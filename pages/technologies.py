import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Output, callback, html

import components as c
import data
from theme import CATEGORICAL, NEUTRAL, SEQUENTIAL, mark_incomplete

dash.register_page(__name__, path="/technologies", name="Technologies", order=3)

layout = html.Div([
    c.page_header("Technologies",
                  "What the patents protect: which checkpoint they target and which strategy they use. "
                  "Labels come from keywords in titles and abstracts, so treat them as indicative."),
    c.card(c.graph("tech-heat", 380), "Documents per checkpoint target and application year",
           "A document naming two targets (for example a PD-1 × LAG-3 bispecific) counts in both rows."),
    dbc.Row([
        dbc.Col(c.card(c.graph("tech-strat", 460), "Strategies over time: share of each year's documents (from 2014)"), lg=7),
        dbc.Col(c.card(c.graph("tech-topics", 460), "Topics found by topic modelling (2024 analysis)"), lg=5),
    ], className="g-3"),
    c.card(c.table("tech-table", 10), "Documents with their labels",
           "Click a title to open the patent on Lens.org."),
])


@callback(Output("tech-heat", "figure"), Output("tech-strat", "figure"), Output("tech-topics", "figure"),
          Output("tech-table", "data"), Output("tech-table", "columns"), *c.FILTER_INPUTS)
def update(years, statuses, targets, strategies, types):
    p = data.filter_patents(years, statuses, targets, strategies, types)
    if p.empty:
        e = c.empty_figure()
        return e, e, e, [], []
    p2 = p[p.year >= max(2010, int(p.year.min()))]

    heat = p2.explode("target_list").groupby(["target_list", "year"]).size().reset_index(name="Documents")
    order = [t for t in data.TARGETS if t in set(heat.target_list)]
    years_all = list(range(int(p2.year.min()), int(p2.year.max()) + 1))
    piv = (heat.pivot(index="target_list", columns="year", values="Documents")
           .reindex(index=order, columns=years_all).fillna(0).astype(int))
    fig = px.imshow(piv, color_continuous_scale=["#ffffff"] + SEQUENTIAL, aspect="auto", text_auto=True,
                    labels=dict(x="Application year", y="", color="Documents"))
    fig.update_traces(textfont_size=10)
    fig.update_layout(coloraxis_showscale=False)

    st = p2.explode("strategy_list")
    st = st[st.strategy_list != "Single agent / not stated"]
    s = st.groupby(["year", "strategy_list"]).size().reset_index(name="n")
    s["Share of documents (%)"] = 100 * s.n / s.year.map(p2.groupby("year").size())
    top = st.strategy_list.value_counts().head(5).index.tolist()
    s = s[s.strategy_list.isin(top) & (s.year >= data.SHARE_START)]
    fig2 = px.line(s, x="year", y="Share of documents (%)", color="strategy_list", markers=True,
                   color_discrete_map={k: CATEGORICAL[i] for i, k in enumerate(top)},
                   category_orders={"strategy_list": top},
                   labels={"year": "Application year", "strategy_list": "Strategy"})
    fig2.update_layout(legend=dict(orientation="h", y=1.12, x=0))
    if p.year.max() > data.LAST_COMPLETE_YEAR:
        mark_incomplete(fig2, label="Incomplete")

    tp = p.topic.value_counts().reset_index()
    tp.columns = ["Topic", "Documents"]
    tp = tp.iloc[::-1]
    fig3 = px.bar(tp, x="Documents", y="Topic", orientation="h", color_discrete_sequence=[CATEGORICAL[0]],
                  labels={"Topic": ""})
    fig3.update_xaxes(nticks=4)
    fig3.update_traces(marker_color=[NEUTRAL if t == "Unassigned" else CATEGORICAL[0] for t in tp.Topic])

    out = p.sort_values(["year", "cited_by_patents"], ascending=False)[
        ["title", "url", "year", "jurisdiction", "status", "targets", "strategies"]].copy()
    out["Title"] = [f"[{t[:140]}]({u})" for t, u in zip(out.title, out.url)]
    out["Targets"] = out.targets.str.replace(data.SEP, ", ")
    out["Strategies"] = out.strategies.str.replace(data.SEP, ", ")
    out = out.rename(columns={"year": "Year", "jurisdiction": "Office", "status": "Status"})[
        ["Title", "Year", "Office", "Status", "Targets", "Strategies"]]
    return fig, fig2, fig3, out.to_dict("records"), c.table_columns(out, link_cols=("Title",))
