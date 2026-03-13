import pandas as pd
import plotly.graph_objects as go
import numpy as np


def build_v4_dispersion_figure(data):
    points = data.get("shot_pattern_points", [])
    if not points:
        return None

    df = pd.DataFrame(points, columns=["Side Carry", "Carry Distance"])

    mean_side = float(data.get("mean_side", 0))
    mean_carry = float(data.get("mean_carry", 0))
    corridor_m = float(data.get("corridor_m", 5))
    ellipse_width = float(data.get("ellipse_width", 0))
    ellipse_height = float(data.get("ellipse_height", 0))

    x_min = min(df["Side Carry"].min(), -corridor_m) - 5
    x_max = max(df["Side Carry"].max(), corridor_m) + 5
    y_min = max(0, df["Carry Distance"].min() - 8)
    y_max = df["Carry Distance"].max() + 8

    fig = go.Figure()

    fig.add_vrect(
        x0=-corridor_m,
        x1=corridor_m,
        fillcolor="rgba(30,215,96,0.12)",
        line_width=0,
        layer="below"
    )

    fig.add_vline(
        x=0,
        line_width=2,
        line_dash="dash",
        line_color="rgba(220,220,220,0.7)"
    )

    fig.add_trace(go.Scatter(
        x=df["Side Carry"],
        y=df["Carry Distance"],
        mode="markers",
        marker=dict(
            size=10,
            color="rgba(0,220,160,0.82)",
            line=dict(width=1, color="rgba(255,255,255,0.12)")
        ),
        hovertemplate="Side: %{x:.1f}m<br>Carry: %{y:.1f}m<extra></extra>",
        showlegend=False
    ))

    if ellipse_width > 0 and ellipse_height > 0:
        t = np.linspace(0, 2 * np.pi, 120)
        ex = mean_side + ellipse_width * np.cos(t)
        ey = mean_carry + ellipse_height * np.sin(t)

        fig.add_trace(go.Scatter(
            x=ex,
            y=ey,
            mode="lines",
            line=dict(color="rgba(255,255,255,0.65)", width=2),
            hoverinfo="skip",
            showlegend=False
        ))

    fig.add_trace(go.Scatter(
        x=[mean_side],
        y=[mean_carry],
        mode="markers",
        marker=dict(
            size=16,
            color="rgba(255,90,90,1)",
            symbol="diamond"
        ),
        hovertemplate="Center<br>Side: %{x:.1f}m<br>Carry: %{y:.1f}m<extra></extra>",
        showlegend=False
    ))

    fig.update_layout(
        height=430,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="#142c34",
        plot_bgcolor="#0f1f26",
        font=dict(color="#e8f0f2")
    )

    fig.update_xaxes(
        title="Side Carry (m)",
        range=[x_min, x_max],
        gridcolor="rgba(255,255,255,0.08)",
        zeroline=False
    )

    fig.update_yaxes(
        title="Carry Distance (m)",
        range=[y_min, y_max],
        gridcolor="rgba(255,255,255,0.08)",
        zeroline=False
    )

    return fig
