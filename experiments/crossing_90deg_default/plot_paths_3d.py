import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (needed for 3D projection)


def plot_3d_paths(drone_a, drone_b, title="Two-drone 3D trajectories", output_path=None):
    """
    Plot two 3D trajectories with a more polished, publication-style appearance.

    Parameters
    ----------
    drone_a : dict
        Dictionary with keys "x", "y", "z" as 1D numpy arrays for drone A.
    drone_b : dict
        Dictionary with keys "x", "y", "z" as 1D numpy arrays for drone B.
    title : str, optional
        Figure title.
    output_path : str, optional
        If provided, the figure is saved to this path (e.g. "paths_3d.png").

    Returns
    -------
    (fig, ax) : tuple
        Matplotlib figure and 3D axes objects.
    """

    plt.style.use("seaborn-v0_8-whitegrid")

    fig = plt.figure(figsize=(8, 6), dpi=150)
    ax = fig.add_subplot(111, projection="3d")

    colors = {"A": "#1f77b4", "B": "#ff7f0e"}
    lw_main = 2.5

    # Main trajectory lines
    ax.plot(
        drone_a["x"],
        drone_a["y"],
        drone_a["z"],
        color=colors["A"],
        lw=lw_main,
        label="Drone A",
    )
    ax.plot(
        drone_b["x"],
        drone_b["y"],
        drone_b["z"],
        color=colors["B"],
        lw=lw_main,
        label="Drone B",
    )

    # Start / end markers
    for drone, key in ((drone_a, "A"), (drone_b, "B")):
        ax.scatter(
            drone["x"][0],
            drone["y"][0],
            drone["z"][0],
            color=colors[key],
            s=40,
            marker="o",
            edgecolor="k",
            zorder=5,
        )
        ax.scatter(
            drone["x"][-1],
            drone["y"][-1],
            drone["z"][-1],
            color=colors[key],
            s=40,
            marker="X",
            edgecolor="k",
            zorder=6,
        )

    ax.set_xlabel("X [m]", labelpad=8)
    ax.set_ylabel("Y [m]", labelpad=8)
    ax.set_zlabel("Altitude [m]", labelpad=8)

    ax.set_title(title, pad=16, fontsize=12, weight="bold")

    # Light, unobtrusive grid
    ax.xaxis._axinfo["grid"]["linewidth"] = 0.3
    ax.yaxis._axinfo["grid"]["linewidth"] = 0.3
    ax.zaxis._axinfo["grid"]["linewidth"] = 0.3

    # Enforce approximately equal aspect ratio
    xs = np.concatenate([drone_a["x"], drone_b["x"]])
    ys = np.concatenate([drone_a["y"], drone_b["y"]])
    zs = np.concatenate([drone_a["z"], drone_b["z"]])

    ranges = np.array([xs.max() - xs.min(), ys.max() - ys.min(), zs.max() - zs.min()])
    max_range = 0.55 * float(ranges.max())

    mid_x = 0.5 * (xs.max() + xs.min())
    mid_y = 0.5 * (ys.max() + ys.min())
    mid_z = 0.5 * (zs.max() + zs.min())

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    # Camera angle tuned for clarity
    ax.view_init(elev=25, azim=-60)

    legend = ax.legend(frameon=True, loc="upper left")
    legend.get_frame().set_alpha(0.9)

    fig.tight_layout()

    if output_path is not None:
        fig.savefig(output_path, bbox_inches="tight")

    return fig, ax


def _demo(output_path="paths_3d_demo.png"):
    """
    Quick visual test: generate two synthetic paths and save a demo figure.
    """
    t = np.linspace(0.0, 1.0, 200)

    # Simple synthetic crossing scenario for visual inspection
    xa = 1000 * (t - 0.5)
    ya = 100.0 + 20.0 * np.sin(2 * np.pi * t)
    za = 200.0 * (t - 0.5)

    xb = 200.0 * (0.5 - t)
    yb = 80.0 + 30.0 * np.cos(2 * np.pi * t)
    zb = 300.0 * (0.5 - t)

    drone_a = {"x": xa, "y": ya, "z": za}
    drone_b = {"x": xb, "y": yb, "z": zb}

    plot_3d_paths(drone_a, drone_b, output_path=output_path)


if __name__ == "__main__":
    _demo()

