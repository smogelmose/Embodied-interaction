"""
generate_report_figures.py

The BESS values below are the annotations used in the running system
(Metamorphic_Efforts.twee, ME.passageData). 
The descriptor logic mirrors ME.computeDescriptors in story-javascript.js.

Run:
    python report_figures.py

Outputs are written relative to the script.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, asdict
from typing import Dict, List

import matplotlib.pyplot as plt


# ------------------------------------------------------------------
# BESS annotation: 10 passages
# ------------------------------------------------------------------

@dataclass
class Passage:
    p: int
    drive: str
    flow: float
    intensity: float
    shape_grow: float
    shape_rise: float
    shape_advance: float
    body_connectivity: float
    body_sequencing: float
    kinesphere: float
    space_approach: float
    space_plane: float


PASSAGES: List[Passage] = [
    Passage( 1, "Press", flow=0.15, intensity=0.40, shape_grow=0.10, shape_rise=0.00, shape_advance=0.00, body_connectivity=0.50, body_sequencing=0.30, kinesphere=0.30, space_approach=0.90, space_plane=0.20),
    Passage( 2, "Press", flow=0.15, intensity=0.35, shape_grow=0.05, shape_rise=0.00, shape_advance=0.00, body_connectivity=0.50, body_sequencing=0.30, kinesphere=0.30, space_approach=0.85, space_plane=0.20),
    Passage( 3, "Press", flow=0.20, intensity=0.55, shape_grow=0.20, shape_rise=0.10, shape_advance=0.10, body_connectivity=0.45, body_sequencing=0.35, kinesphere=0.35, space_approach=0.65, space_plane=0.30),
    Passage( 4, "Press", flow=0.18, intensity=0.65, shape_grow=0.20, shape_rise=0.05, shape_advance=0.10, body_connectivity=0.45, body_sequencing=0.35, kinesphere=0.35, space_approach=0.75, space_plane=0.30),
    Passage( 5, "Wring", flow=0.30, intensity=0.75, shape_grow=0.30, shape_rise=0.10, shape_advance=0.20, body_connectivity=0.40, body_sequencing=0.40, kinesphere=0.40, space_approach=0.32, space_plane=0.40),
    Passage( 6, "Press", flow=0.50, intensity=0.80, shape_grow=0.40, shape_rise=0.30, shape_advance=0.35, body_connectivity=0.45, body_sequencing=0.50, kinesphere=0.50, space_approach=0.70, space_plane=0.50),
    Passage( 7, "Wring", flow=0.35, intensity=0.80, shape_grow=0.35, shape_rise=0.20, shape_advance=0.30, body_connectivity=0.45, body_sequencing=0.40, kinesphere=0.45, space_approach=0.45, space_plane=0.45),
    Passage( 8, "Glide", flow=0.75, intensity=0.60, shape_grow=0.55, shape_rise=0.45, shape_advance=0.65, body_connectivity=0.55, body_sequencing=0.60, kinesphere=0.55, space_approach=0.80, space_plane=0.55),
    Passage( 9, "Glide", flow=0.40, intensity=0.85, shape_grow=0.65, shape_rise=0.55, shape_advance=0.80, body_connectivity=0.50, body_sequencing=0.35, kinesphere=0.60, space_approach=0.70, space_plane=0.55),
    Passage(10, "Slash", flow=0.65, intensity=0.80, shape_grow=0.20, shape_rise=0.20, shape_advance=0.00, body_connectivity=0.30, body_sequencing=0.15, kinesphere=0.30, space_approach=0.35, space_plane=0.30),
]


# ------------------------------------------------------------------
# Larboulette and Gibet descriptors
# ------------------------------------------------------------------
# Mirrors ME.computeDescriptors (story-javascript.js), W=5 sliding window.
# Cold start (history length < 2) returns 0.5 across all four descriptors.

DESCRIPTOR_WINDOW: int = 5


def compute_descriptors(history: List[Passage]) -> Dict[str, float]:
    """Compute the four Larboulette & Gibet descriptors on a BESS history.

    Mirrors the JS implementation in ME.computeDescriptors so the figure stays
    consistent with what TouchDesigner sees at runtime.
    """
    if not history or len(history) < 2:
        return {"ld_weight": 0.5, "ld_time": 0.5, "ld_space": 0.5, "ld_flow": 0.5}

    w = min(DESCRIPTOR_WINDOW, len(history))
    win = history[-w:]
    n = len(win)

    # Weight: max intensity over window (peak kinetic energy proxy)
    ld_weight = max(p.intensity for p in win)

    # Time: mean absolute delta of intensity and flow (summed acceleration proxy)
    time_sum = 0.0
    time_samples = 0
    for i in range(1, n):
        time_sum += abs(win[i].intensity - win[i - 1].intensity)
        time_sum += abs(win[i].flow - win[i - 1].flow)
        time_samples += 2
    ld_time = min(1.0, (time_sum / time_samples) * 5) if time_samples else 0.5

    # Space: path/displacement ratio of space_approach trajectory (directness)
    # Exact L&G formula: ratio near 1 is Direct, higher is Indirect.
    # Mapped to [0, 1] where 1 is Direct.
    path_len = 0.0
    for i in range(1, n):
        path_len += abs(win[i].space_approach - win[i - 1].space_approach)
    disp = abs(win[n - 1].space_approach - win[0].space_approach)
    ratio = path_len / disp if disp > 0.01 else 1.0
    ld_space = max(0.0, min(1.0, 1 - (ratio - 1) / 4))

    # Flow: aggregated jerk of the flow channel itself (second derivative)
    # Honest second-order measure: jerk of annotated flow trajectory.
    jerk_sum = 0.0
    jerk_samples = 0
    for i in range(2, n):
        d1 = win[i].flow - win[i - 1].flow
        d0 = win[i - 1].flow - win[i - 2].flow
        jerk_sum += abs(d1 - d0)
        jerk_samples += 1
    ld_flow = min(1.0, (jerk_sum / jerk_samples) * 10) if jerk_samples else 0.5

    return {
        "ld_weight": round(ld_weight, 3),
        "ld_time":   round(ld_time, 3),
        "ld_space":  round(ld_space, 3),
        "ld_flow":   round(ld_flow, 3),
    }


def descriptor_trajectory(passages: List[Passage]) -> List[Dict[str, float]]:
    """Run compute_descriptors at each passage with the running history up to and including that passage."""
    out = []
    for i in range(len(passages)):
        history = passages[: i + 1]
        out.append(compute_descriptors(history))
    return out


# ------------------------------------------------------------------
# Figures
# ------------------------------------------------------------------

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def _annotate_drives(ax, passages: List[Passage]) -> None:
    """Add Action Drive labels above each passage's x-tick."""
    for p in passages:
        ax.annotate(
            p.drive,
            xy=(p.p, 1.0),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=10,
            color="#444",
            xycoords=("data", "axes fraction"),
        )


def plot_bess_trajectory(passages: List[Passage], out_path: str) -> None:
    """Plot six BESS channels across the 10-passage arc."""
    xs = [p.p for p in passages]
    series = [
        ("flow",              [p.flow              for p in passages], "o", "#1f77b4"),
        ("intensity",         [p.intensity         for p in passages], "s", "#ff7f0e"),
        ("shape_advance",     [p.shape_advance     for p in passages], "^", "#2ca02c"),
        ("body_connectivity", [p.body_connectivity for p in passages], "D", "#d62728"),
        ("body_sequencing",   [p.body_sequencing   for p in passages], "v", "#9467bd"),
        ("space_approach",    [p.space_approach    for p in passages], "P", "#8c564b"),
    ]

    fig, ax = plt.subplots(figsize=(14, 7))
    for label, ys, marker, color in series:
        ax.plot(xs, ys, marker=marker, color=color, linewidth=1.5, markersize=8, label=label)

    ax.set_xlim(0.7, 10.3)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xticks(range(1, 11))
    ax.set_xlabel("Passage", fontsize=12)
    ax.set_ylabel("BESS value (0 to 1)", fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower left", ncol=3, fontsize=10)

    _annotate_drives(ax, passages)

    fig.suptitle("BESS value trajectory across the 10-passage arc", fontsize=14, y=0.995)
    plt.tight_layout(rect=(0, 0, 1, 0.94))
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_path}")


def plot_descriptors_computed(passages: List[Passage], out_path: str) -> None:
    """Plot Larboulette and Gibet descriptors computed on the BESS trajectory."""
    descriptors = descriptor_trajectory(passages)
    xs = [p.p for p in passages]

    series = [
        ("ld_weight (max kinetic energy)",   [d["ld_weight"] for d in descriptors], "o", "#1f77b4"),
        ("ld_time (summed acceleration)",    [d["ld_time"]   for d in descriptors], "s", "#ff7f0e"),
        ("ld_space (path/displacement)",     [d["ld_space"]  for d in descriptors], "^", "#2ca02c"),
        ("ld_flow (aggregated jerk)",        [d["ld_flow"]   for d in descriptors], "D", "#d62728"),
    ]

    fig, ax = plt.subplots(figsize=(14, 7))
    for label, ys, marker, color in series:
        ax.plot(xs, ys, marker=marker, color=color, linewidth=1.8, markersize=8, label=label)

    ax.set_xlim(0.7, 10.3)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xticks(range(1, 11))
    ax.set_xlabel("Passage", fontsize=12)
    ax.set_ylabel("Descriptor value (0 to 1)", fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower left", fontsize=10)

    _annotate_drives(ax, passages)

    fig.suptitle(
        f"Larboulette & Gibet descriptors computed on the BESS trajectory\n"
        f"(sliding window, W={DESCRIPTOR_WINDOW} passages)",
        fontsize=14,
        y=0.998,
    )
    plt.tight_layout(rect=(0, 0, 1, 0.90))
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_path}")


# ------------------------------------------------------------------
# CSV export
# ------------------------------------------------------------------

def export_csv(passages: List[Passage], out_dir: str) -> None:
    """Write the BESS values and computed descriptors as CSV for inspection."""
    bess_path = os.path.join(out_dir, "bess_values.csv")
    desc_path = os.path.join(out_dir, "descriptors_computed.csv")

    bess_fields = list(asdict(passages[0]).keys())
    with open(bess_path, "w", encoding="utf-8") as f:
        f.write(",".join(bess_fields) + "\n")
        for p in passages:
            row = asdict(p)
            f.write(",".join(str(row[k]) for k in bess_fields) + "\n")
    print(f"Wrote {bess_path}")

    descriptors = descriptor_trajectory(passages)
    with open(desc_path, "w", encoding="utf-8") as f:
        f.write("p,drive,ld_weight,ld_time,ld_space,ld_flow\n")
        for p, d in zip(passages, descriptors):
            f.write(f"{p.p},{p.drive},{d['ld_weight']},{d['ld_time']},{d['ld_space']},{d['ld_flow']}\n")
    print(f"Wrote {desc_path}")


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

def main() -> None:
    plot_bess_trajectory(PASSAGES, os.path.join(OUTPUT_DIR, "bess_trajectory.png"))
    plot_descriptors_computed(PASSAGES, os.path.join(OUTPUT_DIR, "descriptors_computed.png"))
    export_csv(PASSAGES, OUTPUT_DIR)


if __name__ == "__main__":
    main()
