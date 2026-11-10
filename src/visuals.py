import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc

PITCH_LENGTH, PITCH_WIDTH = 120, 80

def draw_pitch(ax):
    ax.set_xlim(0, PITCH_LENGTH)
    ax.set_ylim(0, PITCH_WIDTH)
    ax.set_aspect("equal")
    ax.add_patch(Rectangle((0, 0), 120, 80, fill=False, linewidth=1.5))
    ax.plot([60, 60], [0, 80], linewidth=1)
    ax.add_patch(Circle((60, 40), 9.15, fill=False, linewidth=1))
    ax.add_patch(Rectangle((0, 18), 18, 44, fill=False, linewidth=1))
    ax.add_patch(Rectangle((102, 18), 18, 44, fill=False, linewidth=1))
    ax.add_patch(Rectangle((0, 30), 6, 20, fill=False, linewidth=1))
    ax.add_patch(Rectangle((114, 30), 6, 20, fill=False, linewidth=1))
    ax.axis("off")

def plot_shots(ax, shots):
    if shots.empty:
        ax.text(60, 40, "No shot events found", ha="center", va="center")
        return
    for _, row in shots.dropna(subset=["x", "y"]).iterrows():
        is_goal = row["shot_outcome"] == "Goal"
        ax.scatter(row["x"], row["y"], s=70 if is_goal else 35,
                   marker="*", edgecolors="black", linewidths=.5)
    ax.set_title("Shots (stars = goals)", fontsize=10)

def plot_passes(ax, passes):
    if passes.empty:
        ax.text(60, 40, "No completed passes found", ha="center", va="center")
        return
    sample = passes.dropna(subset=["x", "y", "end_x", "end_y"]).head(180)
    for _, row in sample.iterrows():
        ax.annotate("", xy=(row["end_x"], row["end_y"]), xytext=(row["x"], row["y"]),
                    arrowprops={"arrowstyle": "->", "linewidth": .65, "alpha": .45})
    ax.set_title(f"Completed passes (showing up to {len(sample)})", fontsize=10)
