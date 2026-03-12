
import matplotlib.pyplot as plt

def render_distance_range_chart(distance_info):

    if not distance_info.get("has_distance_intel", False):
        return

    avg = distance_info.get("avg_carry", 0)
    rmin = distance_info.get("reliable_min", 0)
    rmax = distance_info.get("reliable_max", 0)
    fmin = distance_info.get("full_min", 0)
    fmax = distance_info.get("full_max", 0)

    fig, ax = plt.subplots(figsize=(6,1.6))

    ax.hlines(1, fmin, fmax, linewidth=6)
    ax.hlines(1, rmin, rmax, linewidth=10)

    ax.scatter(avg,1,s=120,zorder=5)

    ax.set_yticks([])
    ax.set_xlabel("Carry Distance (m)")
    ax.set_title("Distance Range")

    for spine in ["left","right","top"]:
        ax.spines[spine].set_visible(False)

    plt.tight_layout()

    return fig
