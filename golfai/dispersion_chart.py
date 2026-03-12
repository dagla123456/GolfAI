import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


def render_professional_dispersion_chart(data):
    points = data.get("shot_pattern_points", [])
    if not points:
        return None

    df = pd.DataFrame(points, columns=["Side Carry", "Carry Distance"])

    mean_side = data.get("mean_side", 0)
    mean_carry = data.get("mean_carry", 0)
    ellipse_width = data.get("ellipse_width", 0)
    ellipse_height = data.get("ellipse_height", 0)
    corridor_m = data.get("corridor_m", 5)

    fig, ax = plt.subplots(figsize=(6.8, 5.6))

    # central target corridor
    ax.axvspan(-corridor_m, corridor_m, alpha=0.12)
    ax.axvline(0, linewidth=1.8, linestyle="--")

    # shots
    ax.scatter(
        df["Side Carry"],
        df["Carry Distance"],
        s=52,
        alpha=0.82
    )

    # centroid
    ax.scatter(
        mean_side,
        mean_carry,
        marker="D",
        s=110,
        zorder=5
    )

    # confidence ellipse
    if ellipse_width > 0 and ellipse_height > 0:
        ellipse = Ellipse(
            (mean_side, mean_carry),
            width=ellipse_width * 2,
            height=ellipse_height * 2,
            fill=False,
            linewidth=2.2
        )
        ax.add_patch(ellipse)

    # layout
    ax.set_title("Shot Dispersion", pad=10)
    ax.set_xlabel("Side Carry (m)")
    ax.set_ylabel("Carry Distance (m)")
    ax.grid(True, linewidth=0.45, alpha=0.5)

    x_pad = max(corridor_m, abs(df["Side Carry"]).max() if len(df) else 5) + 4
    y_min = max(0, df["Carry Distance"].min() - 8)
    y_max = df["Carry Distance"].max() + 8
    ax.set_xlim(-x_pad, x_pad)
    ax.set_ylim(y_min, y_max)

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

    plt.tight_layout()
    return fig
