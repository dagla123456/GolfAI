import pandas as pd
import plotly.graph_objects as go


def build_v4_dispersion_chart(data):
    points = data.get("shot_pattern_points", [])
    if not points:
        return None

    df = pd.DataFrame(points, columns=["Side Carry", "Carry Distance"])

    mean_side = data.get("mean_side", 0)
    mean_carry = data.get("mean_carry", 0)
    corridor_m = data.get("corridor_m", 5)

    fig = go.Figure()

    # Target corridor shading
    fig.add_vrect(
        x0=-corridor_m,
        x1=corridor_m,
        fillcolor="rgba(34,139,34,0.12)",
        line_width=0
    )

    # Target line
    fig.add_vline(
        x=0,
        line_width=2,
        line_dash="dash",
        line_color="rgba(60,60,60,0.8)"
    )

    # Shot points
    fig.add_trace(go.Scatter(
        x=df["Side Carry"],
        y=df["Carry Distance"],
        mode="markers",
        marker=dict(size=9, color="rgba(31,74,53,0.75)"),
        name="Shots"
    ))

    # Centroid
    fig.add_trace(go.Scatter(
        x=[mean_side],
        y=[mean_carry],
        mode="markers",
        marker=dict(size=12, color="rgba(200,60,60,1)", symbol="diamond"),
        name="Center"
    ))

    fig.update_layout(
        title="Shot Dispersion",
        height=420,
        margin=dict(l=20, r=20, t=45, b=20),
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    fig.update_xaxes(title="Side Carry (m)", zeroline=False, gridcolor="rgba(0,0,0,0.08)")
    fig.update_yaxes(title="Carry Distance (m)", zeroline=False, gridcolor="rgba(0,0,0,0.08)")

    return fig


def build_v4_distance_chart(distance_info):
    if not distance_info.get("has_distance_intel", False):
        return None

    avg = float(distance_info.get("avg_carry", 0))
    rmin = float(distance_info.get("reliable_min", 0))
    rmax = float(distance_info.get("reliable_max", 0))
    fmin = float(distance_info.get("full_min", 0))
    fmax = float(distance_info.get("full_max", 0))

    fig = go.Figure()

    # Full range
    fig.add_trace(go.Scatter(
        x=[fmin, fmax],
        y=[1, 1],
        mode="lines",
        line=dict(width=10, color="rgba(130,130,130,0.35)"),
        hoverinfo="skip",
        showlegend=False
    ))

    # Reliable range
    fig.add_trace(go.Scatter(
        x=[rmin, rmax],
        y=[1, 1],
        mode="lines",
        line=dict(width=18, color="rgba(31,74,53,0.85)"),
        hoverinfo="skip",
        showlegend=False
    ))

    # Average marker
    fig.add_trace(go.Scatter(
        x=[avg],
        y=[1],
        mode="markers+text",
        marker=dict(size=14, color="rgba(200,60,60,1)"),
        text=[f"Avg {avg:.1f}m"],
        textposition="top center",
        showlegend=False
    ))

    fig.update_layout(
        title="Distance Range",
        height=220,
        margin=dict(l=20, r=20, t=45, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    fig.update_yaxes(visible=False, range=[0.8, 1.2])
    fig.update_xaxes(title="Carry Distance (m)", gridcolor="rgba(0,0,0,0.08)")

    return fig


def build_v4_progress_chart(trend):
    if not trend.get("has_history", False):
        return None

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=trend["dates"],
        y=trend["performance"],
        mode="lines+markers",
        name="Performance",
        line=dict(width=3, color="rgba(31,74,53,1)")
    ))

    fig.add_trace(go.Scatter(
        x=trend["dates"],
        y=trend["dispersion"],
        mode="lines+markers",
        name="Dispersion",
        line=dict(width=3, color="rgba(200,120,40,1)")
    ))

    fig.update_layout(
        title="Progress Over Time",
        height=360,
        margin=dict(l=20, r=20, t=45, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(orientation="h")
    )

    fig.update_xaxes(gridcolor="rgba(0,0,0,0.08)")
    fig.update_yaxes(gridcolor="rgba(0,0,0,0.08)")

    return fig
