from constants import wvln_to_f2, wvln_to_f1
import numpy as np
from ABCD import runner


f1_options = [0.0015, 0.002, 0.0028, 0.003, 0.0031, 0.0033, 0.004, 0.0045,
              0.00451, 0.0046, 0.0055, 0.0062, 0.00624, 0.0075, 0.008, 0.0096,
              0.011, 0.0139, 0.0153, 0.0184]  # in meters

################################ USER INPUTS ###################################
total_distance = 0.25  # 250 mm

d1_neg_delta = 0.03      # 5% under f1
d1_pos_delta = 0.03      # 5% over f1
num_points = 10001
###############################################################################

summary = []

for wavelen in wvln_to_f2.keys():
    f1 = wvln_to_f1[wavelen]
    f2 = wvln_to_f2[wavelen]
    d2 = f2
    best = None
    for d1 in np.linspace(f1 * (1 - d1_neg_delta), f1 * (1 + d1_pos_delta), num_points):

        w_i, w_c, w_o, R_o, d2_ideal, max_waist = runner(
            wavelen,
            d1,
            f1,
            total_distance - d1,
            f2,
            d2
        )

        waist_error = abs(w_o - w_c)
        d2_error = abs(d2 - d2_ideal)
        # total_error = np.sqrt(waist_error**2 + d2_error**2)
        total_error = d2_error

        if best is None or total_error < best["d2_error"]:
            best = {
                "d1": d1,
                "f1": f1,
                "d12": total_distance - d1,
                "f2": f2,
                "d2": d2,
                "d2_ideal": d2_ideal,
                "d2_error": d2_error,
                "w_i": w_i,
                "w_c": w_c,
                "w_o": w_o,
                "R_o": R_o,
                "total_error": total_error,
                "waist_error": waist_error,
                "max_waist": max_waist
            }

    summary.append("\n" + "="*60)
    summary.append(f"{wavelen} nm - BEST SOLUTION")
    summary.append("="*60)

    summary.append(f"f1          = {best['f1']*1e3:.3f} mm")
    summary.append(f"f2          = {best['f2']*1e3:.3f} mm")

    summary.append(f"d1          = {best['d1']*1e3:.6f} mm")
    summary.append(f"d12         = {best['d12']*1e3:.3f} mm")
    summary.append(f"d2          = {best['d2']*1e3:.3f} mm")
    summary.append(f"Ideal d2     = {best['d2_ideal']*1e3:.3f} mm")

    summary.append(f"\nInput waist  = {best['w_i']*1e6:.3f} μm")
    summary.append(f"Max waist    = {best['max_waist']*1e6:.3f} μm")
    summary.append(f"Cavity waist = {best['w_c']*1e6:.3f} μm")
    summary.append(f"Output waist = {best['w_o']*1e6:.3f} μm")

    summary.append(f"\nWaist error = {best['waist_error']*1e6:.6f} μm")
    summary.append(f"Fractional error = {100*(best['w_o']-best['w_c'])/best['w_c']:.6f}%")

    summary.append(f"\nOutput ROC = {best['R_o']}")
    summary.append(f"d2 error = {best['d2_error']*1e3:.6f} mm")
    summary.append("="*60 + "\n")


with open("new_mfd_final_results_250.txt", "w") as f:
    f.write("\n".join(summary))