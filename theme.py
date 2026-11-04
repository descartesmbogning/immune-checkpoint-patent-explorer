"""CognosX look for the explorer: colours from the brand charter and one Plotly template."""
import plotly.graph_objects as go
import plotly.io as pio

INK, MUTED, LINE, PAPER, SOFT = "#141414", "#5c5c5c", "#e6e3dd", "#ffffff", "#f7f5f0"
AMBER, AMBER_INK = "#FEA500", "#9a5b00"
CATEGORICAL = ["#C98000", "#2F64B5", "#C24A2E", "#0E9A7E", "#8A4FB0"]   # fixed order, never cycled
NEUTRAL = "#9a9890"                                                       # "other" and context series
SEQUENTIAL = ["#fbe9c7", "#f6cf85", "#eeb043", "#d98e0b", "#b87500", "#8f5a00", "#5f3c00"]

# Fixed colours so a category keeps its colour on every page
STATUS_COLORS = {
    "Granted / in force": CATEGORICAL[3],
    "Pending application": CATEGORICAL[0],
    "Discontinued / expired": CATEGORICAL[2],
    "Other / unknown": NEUTRAL,
}
TYPE_COLORS = {
    "Commercial": CATEGORICAL[0],
    "Academic / research": CATEGORICAL[1],
    "Individual": CATEGORICAL[4],
    "Government": CATEGORICAL[3],
    "Unknown": NEUTRAL,
}
CLASS_COLORS = {
    "Continuant": CATEGORICAL[3],
    "Newcomer": CATEGORICAL[0],
    "Terminator": CATEGORICAL[2],
    "Transient": NEUTRAL,
}

pio.templates["cognosx"] = go.layout.Template(
    layout=dict(
        font=dict(family="Inter, Helvetica Neue, Arial, sans-serif", size=13, color=INK),
        title=dict(font=dict(size=15, color=INK), x=0, xanchor="left"),
        paper_bgcolor=PAPER,
        plot_bgcolor=PAPER,
        colorway=CATEGORICAL,
        xaxis=dict(automargin=True, gridcolor=LINE, linecolor=MUTED, tickcolor=MUTED, zeroline=False, title_font=dict(color=MUTED)),
        yaxis=dict(automargin=True, gridcolor=LINE, linecolor=MUTED, tickcolor=MUTED, zeroline=False, title_font=dict(color=MUTED)),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=12), title_font=dict(color=MUTED)),
        hoverlabel=dict(bgcolor=PAPER, bordercolor=LINE, font=dict(color=INK)),
        margin=dict(l=60, r=20, t=60, b=50),
    )
)
pio.templates.default = "cognosx"


def mark_incomplete(fig, start=2021.5, end=2023.5, label="Incomplete years"):
    """Shade the last application years, which are still filling up (patents publish ~18 months late)."""
    fig.add_vrect(x0=start, x1=end, fillcolor=SOFT, opacity=1, layer="below", line_width=0,
                  annotation_text=label, annotation_position="top left",
                  annotation_font=dict(size=11, color=MUTED))
    return fig
