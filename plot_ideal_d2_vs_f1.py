from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ABCD import runner
from constants import wvln_to_f2, wvln_to_ideal_d2


f1_options = [0.0015, 0.002, 0.0028, 0.003, 0.0031, 0.0033, 0.004, 0.0045,
              0.00451, 0.0046, 0.0055, 0.0062, 0.00624, 0.0075, 0.008, 0.0096,
              0.011, 0.0139, 0.0153, 0.0184]  # in meters

total_distance = 0.2  # meters
output_dir = Path(__file__).with_name("plots") / "ideal-d2-vs-f1"
output_dir.mkdir(parents=True, exist_ok=True)


def make_plots():
    for wavelen in sorted(wvln_to_ideal_d2.keys()):
        f2 = wvln_to_f2[wavelen]
        ideal_d2_m = []

        for f1 in f1_options:
            d1 = f1
            d2 = f2
            _, _, _, _, d2_ideal = runner(
                wavelen,
                d1,
                f1,
                total_distance - d1,
                f2,
                d2,
            )
            ideal_d2_m.append(d2_ideal)

        f1_mm = np.array(f1_options) * 1e3
        ideal_d2_mm = np.array(ideal_d2_m) * 1e3

        fig, ax = plt.subplots(figsize=(8.5, 5))
        ax.plot(f1_mm, ideal_d2_mm, marker="o", linewidth=1.8, color="C0")

        f2_mm = f2 * 1e3
        y_min = min(float(np.min(ideal_d2_mm)), f2_mm)
        y_max = max(float(np.max(ideal_d2_mm)), f2_mm)
        pad = 0.05 * (y_max - y_min if y_max > y_min else 1.0)
        ax.set_ylim(y_min - pad, y_max + pad)

        ax.axhline(f2_mm, color="C1", linestyle="--", linewidth=1.5)
        ax.text(0.98, 0.94, f"f2 = {f2_mm:.2f} mm", transform=ax.transAxes,
                ha="right", va="top", color="C1", fontsize=10)

        ax.set_xlabel("f1 (mm)")
        ax.set_ylabel("Ideal d2 (mm)")
        ax.set_title(f"{wavelen} nm")
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        out_path = output_dir / f"{wavelen}nm_ideal_d2_vs_f1.png"
        fig.savefig(out_path, dpi=200)
        plt.close(fig)
        print(f"Saved {out_path}")


if __name__ == "__main__":
    make_plots()
