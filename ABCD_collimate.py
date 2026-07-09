from ABCD import runner
import numpy as np
import matplotlib.pyplot as plt
from constants import wvln_to_f2, wvln_to_ideal_d2, wvln_to_d2_min, wvln_to_d2_max
# from constants import wvln_to_ideal_d2
from itertools import product


f1_options = [0.0015, 0.002, 0.0028, 0.003, 0.0031, 0.0033, 0.004, 0.0045,
              0.00451, 0.0046, 0.0055, 0.0062, 0.00624, 0.0075, 0.008, 0.0096,
              0.011, 0.0139, 0.0153, 0.0184]  # in meters

# f2_options = [0.03, 0.0351, 0.0401, 0.0502, 0.06, 0.0753, 0.1003, 0.1254,
#               0.1505, 0.1756, 0.2007, 0.2509, 0.3011, 0.350, 0.4, 0.45, 0.5018,
#               0.6, 0.7527, 0.85, 1.0035, 2.0, 2.5] # in meters

################################ USER INPUTS ###################################
# f1 = 0.004           # 4 mm
total_distance = 0.2  # 200 mm

d1_neg_delta = 0.05      # 5% under f1
d1_pos_delta = 0.05      # 5% over f1
# d2_neg_delta = 0.05      # 5% under f2
# d2_pos_delta = 0.05      # 5% over f2
num_points = 1001
###############################################################################

summary = []

for wavelen in wvln_to_ideal_d2.keys():
    f2 = wvln_to_f2[wavelen]
    best = None
    for f1 in f1_options:
        # print(f"Wavelength: {wavelen} nm, f2: {f2:.3f} m")

        # d1_vals = []
        # waist_error_vals = []
        # output_waist_vals = []
        # cavity_waist_vals = []
        # d2_vals = []
        # roc_vals = []

        # print("Sweeping...")

        d1_min = f1 * (1 - d1_neg_delta)
        d1_max = f1 * (1 + d1_pos_delta)
        
        d2_min = wvln_to_d2_min[wavelen]
        d2_max = wvln_to_d2_max[wavelen]

        for d1,d2 in product(np.linspace(d1_min, d1_max, num_points), np.linspace(d2_min, d2_max, num_points)):

            w_i, w_c, w_o, R_o, d2_ideal = runner(
                wavelen,
                d1,
                f1,
                total_distance - d1,
                f2,
                d2
            )

            waist_error = abs(w_o - w_c)
            d2_error = abs(d2 - d2_ideal)
            total_error = np.sqrt(waist_error**2 + d2_error**2)

            # d1_vals.append(d1 * 1e3)            # mm
            # waist_error_vals.append(waist_error * 1e6)  # μm
            # output_waist_vals.append(w_o * 1e6)         # μm
            # cavity_waist_vals.append(w_c * 1e6)         # μm
            # d2_vals.append(d2 * 1e3)                    # mm
            # roc_vals.append(R_o)

            if best is None or total_error < best["total_error"]:
                best = {
                    "d1": d1,
                    "f1": f1,
                    "d12": total_distance - d1,
                    "f2": f2,
                    "d2": d2,
                    "d2_ideal": d2_ideal,
                    "w_i": w_i,
                    "w_c": w_c,
                    "w_o": w_o,
                    "R_o": R_o,
                    "total_error": total_error,
                    "waist_error": waist_error,
                }

    ###############################################################################
    # Save best solution
    ###############################################################################

    # ideal_d2 = wvln_to_ideal_d2[wavelen]
    # best = min(bests, key=lambda x: (x["d2"]-ideal_d2)**2)  # Choose the solution with the closest d2 to the ideal

    summary.append("\n" + "="*60)
    summary.append(f"{wavelen} nm - BEST SOLUTION")
    summary.append("="*60)

    summary.append(f"f1          = {best['f1']*1e3:.3f} mm")
    summary.append(f"f2          = {best['f2']*1e3:.3f} mm")

    summary.append(f"d1          = {best['d1']*1e3:.3f} mm")
    summary.append(f"d12         = {best['d12']*1e3:.3f} mm")
    summary.append(f"d2          = {best['d2']*1e3:.3f} mm")
    summary.append(f"Ideal d2     = {best['d2_ideal']*1e3:.3f} mm")

    summary.append(f"\nInput waist  = {best['w_i']*1e6:.3f} μm")
    summary.append(f"Cavity waist = {best['w_c']*1e6:.3f} μm")
    summary.append(f"Output waist = {best['w_o']*1e6:.3f} μm")

    summary.append(f"\nWaist error = {best['waist_error']*1e6:.6f} μm")
    summary.append(f"Fractional error = {best['waist_error']/best['w_c']:.6e}")

    summary.append(f"\nOutput ROC = {best['R_o']}")
    summary.append("="*60 + "\n")

    ###############################################################################
    # Plot results
    ###############################################################################

    # plt.figure(figsize=(8,5))
    # plt.plot(d1_vals, waist_error_vals)
    # plt.xlabel("d1 (mm)")
    # plt.ylabel("Waist error (μm)")
    # plt.title(f"{wavelen} nm Mode Matching Error vs d1")
    # plt.grid(True)
    # plt.tight_layout()
    # plt.savefig(f"plots/{wavelen}_nm_mode_matching_error_vs_d1.png")


with open("collimate_results.txt", "w") as f:
    f.write("\n".join(summary))