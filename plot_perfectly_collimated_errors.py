from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ABCD import runner
from constants import wvln_to_f2, wvln_to_ideal_d2


f1_options = [0.0015, 0.002, 0.0028, 0.003, 0.0031, 0.0033, 0.004, 0.0045,
              0.00451, 0.0046, 0.0055, 0.0062, 0.00624, 0.0075, 0.008, 0.0096,
              0.011, 0.0139, 0.0153, 0.0184]  # in meters

total_distance = 0.2  # meters
output_dir = Path(__file__).with_name("plots") / "perfectly-collimated-error-plots"
output_dir.mkdir(parents=True, exist_ok=True)


def make_plots():
    for wavelen in sorted(wvln_to_ideal_d2.keys()):
        f2 = wvln_to_f2[wavelen]
        waist_errors_um = []
        d2_errors_mm = []

        for f1 in f1_options:
            d1 = f1
            d2 = f2
            _, w_c, w_o, _, d2_ideal = runner(
                wavelen,
                d1,
                f1,
                total_distance - d1,
                f2,
                d2,
            )
            waist_errors_um.append(abs(w_o - w_c) * 1e6)
            d2_errors_mm.append(abs(d2 - d2_ideal) * 1e3)

        f1_mm = np.array(f1_options) * 1e3

        fig, axes = plt.subplots(2, 1, figsize=(8.5, 7), sharex=True)
        ax1, ax2 = axes

        ax1.plot(f1_mm, waist_errors_um, marker="o", linewidth=1.8, color="C0")
        ax1.set_ylabel("Waist error (μm)")
        ax1.set_title(f"{wavelen} nm")
        ax1.grid(True, alpha=0.3)

        ax2.plot(f1_mm, d2_errors_mm, marker="o", linewidth=1.8, color="C1")
        ax2.set_xlabel("f1 (mm)")
        ax2.set_ylabel("d2 error (mm)")
        ax2.grid(True, alpha=0.3)

        fig.tight_layout()
        out_path = output_dir / f"{wavelen}nm_errors_vs_f1.png"
        fig.savefig(out_path, dpi=200)
        plt.close(fig)
        print(f"Saved {out_path}")


if __name__ == "__main__":
    make_plots()
