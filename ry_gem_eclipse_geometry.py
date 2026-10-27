"""Sky-plane eclipse geometry for RY Gem.

Run without arguments for an interactive orbital-phase slider. Use --export to
write publication-sized PDF and PNG versions of the currently selected phase.
The disk radius is a trial value, not a measured eclipse radius.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse
from matplotlib.widgets import Button, Slider


@dataclass(frozen=True)
class System:
    separation: float = 27.845       # R_sun; WD solution
    inclination_deg: float = 82.287   # degrees; WD solution
    primary_radius: float = 2.621     # R_sun; WD solution
    donor_radius: float = 7.042       # R_sun; WD solution


SYSTEM = System()
DISK_COLOR = "#2b6081"
DONOR_COLOR = "#b27638"
INK = "#22272b"
MUTED = "#657179"


def projected_geometry(phase: float, system: System = SYSTEM) -> tuple[float, float, float, float]:
    """Return donor-center (x, y), vertical distance b, and half-chord w.

    Phase zero denotes primary eclipse, with the donor in the foreground.
    The orbit is assumed circular and the disk is assumed coplanar with it.
    """
    angle = 2.0 * np.pi * (phase % 1.0)
    inclination = np.deg2rad(system.inclination_deg)
    x = system.separation * np.sin(angle)
    y = system.separation * np.cos(inclination) * np.cos(angle)
    b = abs(y)
    w = np.sqrt(max(0.0, system.donor_radius**2 - b**2))
    return float(x), float(y), float(b), float(w)


def first_midline_contact(disk_radius: float, system: System = SYSTEM) -> float:
    """Find the pre-primary midline contact in the interval 0.75 < phase < 1."""
    low, high = 0.750001, 0.999999

    def gap(phase: float) -> float:
        x, _, _, w = projected_geometry(phase, system)
        return abs(x) - w - disk_radius

    if gap(low) <= 0 or gap(high) >= 0:
        raise ValueError("The trial disk radius does not give a unique pre-primary midline contact.")
    for _ in range(70):
        middle = (low + high) / 2.0
        if gap(middle) > 0:
            low = middle
        else:
            high = middle
    return (low + high) / 2.0


def _dimension(ax, x0: float, x1: float, y: float, label: str, color: str) -> None:
    ax.plot([x0, x1], [y, y], color=color, lw=0.95, zorder=7)
    for x in (x0, x1):
        ax.plot([x, x], [y - 0.30, y + 0.30], color=color, lw=0.95, zorder=7)
    ax.text((x0 + x1) / 2.0, y - 0.45, label, ha="center", va="top", color=color)


def draw_geometry(ax, phase: float, disk_radius: float, system: System = SYSTEM) -> None:
    """Draw the projected geometry, including the right triangle defining w."""
    ax.clear()
    x, y, b, w = projected_geometry(phase, system)
    inclination = np.deg2rad(system.inclination_deg)
    donor_in_front = np.cos(2.0 * np.pi * phase) >= 0

    disk = Ellipse(
        (0, 0), 2 * disk_radius, 2 * disk_radius * np.cos(inclination),
        facecolor=DISK_COLOR, edgecolor=DISK_COLOR, alpha=0.22, lw=1.5, zorder=2,
    )
    ax.add_patch(disk)
    ax.plot([-disk_radius, disk_radius], [0, 0], color=DISK_COLOR, lw=1.45, zorder=3)
    ax.add_patch(Circle((0, 0), system.primary_radius, color=INK, zorder=4))

    donor = Circle(
        (x, y), system.donor_radius,
        facecolor=DONOR_COLOR,
        edgecolor=DONOR_COLOR,
        alpha=0.18 if donor_in_front else 0.11,
        lw=1.7,
        zorder=5 if donor_in_front else 1,
    )
    ax.add_patch(donor)
    ax.add_patch(Circle((x, y), system.donor_radius, fill=False,
                        edgecolor=DONOR_COLOR, lw=1.35,
                        ls="-" if donor_in_front else "--", zorder=6))

    direction = 1.0 if x <= 0 else -1.0
    chord_end = x + direction * w
    ax.plot([x, x], [0, y], color=DONOR_COLOR, lw=1.15, ls=(0, (3, 2)), zorder=7)
    ax.plot([x, chord_end], [0, 0], color=DONOR_COLOR, lw=2.0, zorder=7)
    if b >= 0.65:
        ax.plot([x, chord_end], [y, 0], color=DONOR_COLOR, lw=1.1, zorder=7)
        ax.text(x + direction * (0.50 * w + 0.55), 0.50 * y + np.sign(y) * 0.65,
                r"$R_2$", color=DONOR_COLOR, ha="center", va="center", zorder=8)
        ax.text(x - direction * 0.8, 0.5 * y, r"$b$", color=DONOR_COLOR,
                ha="center", va="center", zorder=8)
    ax.plot([x, chord_end], [0, 0], marker="o", markersize=2.7,
            color=DONOR_COLOR, lw=0, zorder=8)
    ax.plot(x, y, marker="o", markersize=2.7, color=DONOR_COLOR, zorder=8)
    ax.text(x + direction * w / 2, -1.15 if y >= 0 else 1.15,
            r"$w$", color=DONOR_COLOR, ha="center", va="center", zorder=8)

    donor_label_y = y + (system.donor_radius + 1.0) * (1 if y >= 0 else -1)
    ax.text(x, donor_label_y, "Donor", ha="center",
            va="bottom" if y >= 0 else "top", color=DONOR_COLOR)
    ax.text(3.0, 3.15, "Primary", color=INK, ha="left", va="center")
    ax.text(0, -3.1, r"Illustrative H$\alpha$ region", color=DISK_COLOR,
            ha="center", va="top")
    ax.text(33.0, 12.5, rf"$\phi={phase:.4f}$", ha="right", va="top", color=INK)

    if abs(x) > 5.0:
        _dimension(ax, 0, x, -10.4, r"$|x|$", MUTED)
    _dimension(ax, 0, -disk_radius, -6.5, r"$R_{\rm d}$", DISK_COLOR)

    ax.axhline(0, color="#bac2c7", lw=0.65, ls=(0, (4, 3)), zorder=0)
    ax.axvline(0, color="#bac2c7", lw=0.65, ls=(0, (4, 3)), zorder=0)
    ax.set_xlim(-36.0, 36.0)
    ax.set_ylim(-14.5, 14.5)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks(np.arange(-30, 31, 10))
    ax.set_yticks([-10, 0, 10])
    ax.set_xlabel(r"Sky-plane $x$ ($R_\odot$)")
    ax.set_ylabel(r"Sky-plane $y$ ($R_\odot$)")
    ax.tick_params(direction="in", top=True, right=True, length=3.5, width=0.8)
    for spine in ax.spines.values():
        spine.set_linewidth(0.8)


def export_figure(phase: float, disk_radius: float, output: Path) -> tuple[Path, Path]:
    """Save the same clean plot as a vector PDF and a 600-dpi PNG."""
    output = output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    fig.subplots_adjust(left=0.105, right=0.975, bottom=0.19, top=0.91)
    draw_geometry(ax, phase, disk_radius)
    pdf = output.parent / f"{output.name}.pdf"
    png = output.parent / f"{output.name}.png"
    fig.savefig(pdf, metadata={"Title": "RY Gem sky-plane eclipse geometry"})
    fig.savefig(png, dpi=600)
    plt.close(fig)
    return pdf, png


def show_interactive(phase: float, disk_radius: float, output: Path) -> None:
    """Open the phase slider; the button exports the selected configuration."""
    fig, ax = plt.subplots(figsize=(9.0, 5.0))
    fig.subplots_adjust(left=0.10, right=0.97, bottom=0.23, top=0.94)
    draw_geometry(ax, phase, disk_radius)

    slider_ax = fig.add_axes((0.14, 0.105, 0.59, 0.034))
    slider = Slider(slider_ax, "Orbital phase", 0.0, 1.0,
                    valinit=phase, valstep=0.0001, color=DISK_COLOR)
    button_ax = fig.add_axes((0.77, 0.073, 0.17, 0.09))
    button = Button(button_ax, "Export PDF / PNG", color="#eef2f4", hovercolor="#dfe9ef")

    def update(selected_phase: float) -> None:
        draw_geometry(ax, selected_phase, disk_radius)
        fig.canvas.draw_idle()

    def save(_event) -> None:
        pdf, png = export_figure(slider.val, disk_radius, output)
        print(f"Saved {pdf}\nSaved {png}")

    slider.on_changed(update)
    button.on_clicked(save)
    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", type=float, default=None,
                        help="Initial orbital phase (0 to 1); default: trial first midline contact")
    parser.add_argument("--disk-radius", type=float, default=11.0,
                        help="Illustrative disk radius in solar radii (default: 11.0)")
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("ry_gem_eclipse_geometry"),
                        help="Output path prefix for the PDF and PNG")
    parser.add_argument("--export", action="store_true",
                        help="Save PDF and PNG without opening the interactive window")
    args = parser.parse_args()
    if not (0.0 < args.disk_radius < SYSTEM.separation):
        parser.error("--disk-radius must be between zero and the orbital separation")
    if args.phase is None:
        try:
            phase = first_midline_contact(args.disk_radius)
        except ValueError as exc:
            parser.error(str(exc) + " Specify --phase explicitly for this radius.")
    else:
        phase = args.phase
    if not 0.0 <= phase <= 1.0:
        parser.error("--phase must be between 0 and 1")

    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "STIXGeneral", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "font.size": 9.0,
        "axes.labelsize": 9.5,
        "xtick.labelsize": 8.5,
        "ytick.labelsize": 8.5,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })
    if args.export:
        pdf, png = export_figure(phase, args.disk_radius, args.output)
        print(f"Saved {pdf}\nSaved {png}")
    else:
        show_interactive(phase, args.disk_radius, args.output)


if __name__ == "__main__":
    main()
