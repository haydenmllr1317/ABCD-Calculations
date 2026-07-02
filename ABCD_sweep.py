from ABCD import runner
import numpy as np
import matplotlib.pyplot as plt
from constants import map_to_f2

################################ USER INPUTS ###################################
f1 = 0.004           # 4 mm
total_distance = 0.2  # 200 mm

d1_min = 0.00395      # 3 mm
d1_max = 0.00415      # 5 mm
num_points = 1001

###############################################################################

summary = []

for wavelen in map_to_f2.keys():
    f2 = map_to_f2[wavelen]
    print(f"Wavelength: {wavelen} nm, f2: {f2:.3f} m")

    best = None

    d1_vals = []
    waist_error_vals = []
    output_waist_vals = []
    cavity_waist_vals = []
    d2_vals = []
    roc_vals = []

    print("Sweeping...")

    for d1 in np.linspace(d1_min, d1_max, num_points):

        w_i, w_c, w_o, R_o, d2 = runner(
            wavelen,
            d1,
            f1,
            total_distance - d1
        )

        waist_error = abs(w_o - w_c)

        d1_vals.append(d1 * 1e3)            # mm
        waist_error_vals.append(waist_error * 1e6)  # μm
        output_waist_vals.append(w_o * 1e6)         # μm
        cavity_waist_vals.append(w_c * 1e6)         # μm
        d2_vals.append(d2 * 1e3)                    # mm
        roc_vals.append(R_o)

        if best is None or waist_error < best["error"]:
            best = {
                "d1": d1,
                "f1": f1,
                "d12": total_distance - d1,
                "f2": map_to_f2[wavelen],
                "d2": d2,
                "w_i": w_i,
                "w_c": w_c,
                "w_o": w_o,
                "R_o": R_o,
                "error": waist_error,
            }

    ###############################################################################
    # Save best solution
    ###############################################################################


    summary.append("\n" + "="*60)
    summary.append(f"{wavelen} nm - BEST SOLUTION")
    summary.append("="*60)

    summary.append(f"d1          = {best['d1']*1e3:.3f} mm")
    summary.append(f"d12         = {best['d12']*1e3:.3f} mm")
    summary.append(f"d2          = {best['d2']*1e3:.3f} mm")

    summary.append(f"\nInput waist  = {best['w_i']*1e6:.3f} μm")
    summary.append(f"Cavity waist = {best['w_c']*1e6:.3f} μm")
    summary.append(f"Output waist = {best['w_o']*1e6:.3f} μm")

    summary.append(f"\nWaist error = {best['error']*1e6:.6f} μm")
    summary.append(f"Fractional error = {best['error']/best['w_c']:.6e}")

    summary.append(f"\nOutput ROC = {best['R_o']}")
    summary.append("="*60 + "\n")

    ###############################################################################
    # Plot results
    ###############################################################################

    plt.figure(figsize=(8,5))
    plt.plot(d1_vals, waist_error_vals)
    plt.xlabel("d1 (mm)")
    plt.ylabel("Waist error (μm)")
    plt.title(f"{wavelen} nm Mode Matching Error vs d1")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"plots/{wavelen}_nm_mode_matching_error_vs_d1.png")


with open("mode_match_results.txt", "w") as f:
    f.write("\n".join(summary))