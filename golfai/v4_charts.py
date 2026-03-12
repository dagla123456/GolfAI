
import pandas as pd
import plotly.graph_objects as go


# -----------------------------
# DISPERSION CHART (MOCKUP STYLE)
# -----------------------------

def build_v4_dispersion_chart(data):

    points = data.get("shot_pattern_points", [])
    if not points:
        return None

    df = pd.DataFrame(points, columns=["Side Carry", "Carry Distance"])

    mean_side = data.get("mean_side", 0)
    mean_carry = data.get("mean_carry", 0)
    corridor = data.get("corridor_m", 5)

    fig = go.Figure()

    # target corridor
    fig.add_vrect(
        x0=-corridor,
        x1=corridor,
        fillcolor="rgba(0,200,120,0.15)",
        line_width=0
    )

    # target line
    fig.add_vline(
        x=0,
        line_width=2,
        line_dash="dash",
        line_color="rgba(200,200,200,0.7)"
    )

    # shot points
    fig.add_trace(go.Scatter(
        x=df["Side Carry"],
        y=df["Carry Distance"],
        mode="markers",
        marker=dict(
            size=10,
            color="rgba(0,220,160,0.8)"
        )
    ))

    # centroid
    fig.add_trace(go.Scatter(
        x=[mean_side],
        y=[mean_carry],
        mode="markers",
        marker=dict(
            size=16,
            color="rgba(255,80,80,1)",
            symbol="diamond"
        )
    ))

    fig.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="#0f1f26",
        paper_bgcolor="#0f1f26",
        font=dict(color="white")
    )

    fig.update_xaxes(
        title="Side Carry (m)",
        gridcolor="rgba(255,255,255,0.08)"
    )

    fig.update_yaxes(
        title="Carry Distance (m)",
        gridcolor="rgba(255,255,255,0.08)"
    )

    return fig


# -----------------------------
# DISTANCE PROFILE (MOCKUP STYLE)
# -----------------------------

def build_v4_distance_chart(distance_info):

    if not distance_info.get("has_distance_intel", False):
        return None

    avg = distance_info.get("avg_carry", 0)
    rmin = distance_info.get("reliable_min", 0)
    rmax = distance_info.get("reliable_max", 0)
    fmin = distance_info.get("full_min", 0)
    fmax = distance_info.get("full_max", 0)

    fig = go.Figure()

    # full range
    fig.add_trace(go.Bar(
        x=[fmax - fmin],
        y=["Carry"],
        base=fmin,
        orientation="h",
        marker=dict(color="rgba(255,255,255,0.15)")
    ))

    # reliable range
    fig.add_trace(go.Bar(
        x=[rmax - rmin],
        y=["Carry"],
        base=rmin,
        orientation="h",
        marker=dict(color="rgba(0,220,160,0.9)")
    ))

    # average marker
    fig.add_trace(go.Scatter(
        x=[avg],
        y=["Carry"],
        mode="markers+text",
        marker=dict(size=14, color="rgba(255,80,80,1)"),
        text=[f"{avg:.1f}m"],
        textposition="top center"
    ))

    fig.update_layout(
        height=220,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
        plot_bgcolor="#0f1f26",
        paper_bgcolor="#0f1f26",
        font=dict(color="white")
    )

    fig.update_xaxes(
        title="Carry Distance (m)",
        gridcolor="rgba(255,255,255,0.08)"
    )

    fig.update_yaxes(visible=False)

    return fig


# -----------------------------
# PROGRESS CHART
# -----------------------------

def build_v4_progress_chart(trend):

    if not trend.get("has_history", False):
        return None

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=trend["dates"],
        y=trend["performance"],
        mode="lines+markers",
        line=dict(width=3, color="rgba(0,220,160,1)")
    ))

    fig.update_layout(
        height=360,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="#0f1f26",
        paper_bgcolor="#0f1f26",
        font=dict(color="white")
    )

    fig.update_xaxes(gridcolor="rgba(255,255,255,0.08)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)")

    return fig
