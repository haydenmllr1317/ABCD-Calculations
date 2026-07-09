from pathlib import Path
import re
import math
import numpy as np
import matplotlib.pyplot as plt

from ABCD import flat_q, prop_free, prop_lens


RESULTS_FILE = Path(__file__).with_name("mode_match_results.txt")
BASE_PLOTS_DIR = Path(__file__).with_name("plots")
PLOTS_DIR = BASE_PLOTS_DIR / "beam-profiles"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)


def parse_results(path: Path):
    text = path.read_text(encoding="utf-8")
    blocks = text.split("\n\n\n")
    solutions = []
    for block in blocks:
        if "BEST SOLUTION" not in block:
            continue
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        data = { }
        # wavelength
        # first try to find the wavelength line (may be preceded by separators)
        for ln0 in lines:
            m = re.match(r"(\d+) nm - BEST SOLUTION", ln0)
            if m:
                data['wvlen'] = int(m.group(1))
                break

        def extract_number(key: str, s: str):
            """Extract number after key= pattern"""
            pattern = rf"{key}\s*=\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)"
            m = re.search(pattern, s)
            if m:
                return m.group(1)
            if 'inf' in s.lower():
                return 'inf'
            return None

        # parse key: value lines
        for ln in lines:
            if ln.startswith('f1'):
                v = extract_number('f1', ln)
                if v:
                    data['f1'] = float(v) * 1e-3
            elif ln.startswith('f2'):
                v = extract_number('f2', ln)
                if v:
                    data['f2'] = float(v) * 1e-3
            elif ln.startswith('d1') and 'd12' not in ln:
                v = extract_number('d1', ln)
                if v:
                    data['d1'] = float(v) * 1e-3
            elif ln.startswith('d12'):
                v = extract_number('d12', ln)
                if v:
                    data['d12'] = float(v) * 1e-3
            elif ln.startswith('d2') and 'Ideal' not in ln:
                v = extract_number('d2', ln)
                if v:
                    data['d2'] = float(v) * 1e-3
            elif ln.startswith('Ideal d2'):
                v = extract_number('Ideal d2', ln)
                if v:
                    data['d2_ideal'] = float(v) * 1e-3
            elif ln.startswith('Input waist'):
                v = extract_number('Input waist', ln)
                if v:
                    data['w_i'] = float(v) * 1e-6
            elif ln.startswith('Cavity waist'):
                v = extract_number('Cavity waist', ln)
                if v:
                    data['w_c'] = float(v) * 1e-6
            elif ln.startswith('Output waist'):
                v = extract_number('Output waist', ln)
                if v:
                    data['w_o'] = float(v) * 1e-6
            elif ln.startswith('Waist error'):
                v = extract_number('Waist error', ln)
                if v:
                    data['error'] = float(v) * 1e-6
            elif ln.startswith('Fractional error'):
                v = extract_number('Fractional error', ln)
                if v and v != 'inf':
                    data['frac_error'] = float(v)
            elif ln.startswith('Output ROC'):
                v = extract_number('Output ROC', ln)
                if v == 'inf':
                    data['R_o'] = float('inf')
                elif v:
                    data['R_o'] = float(v)

        if 'wvlen' in data:
            solutions.append(data)

        # fallback: if values missing, try block-wide regex (handles slightly different formatting)
        if 'f1' not in data:
            m = re.search(r"f1\s*=\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)", block)
            if m:
                data['f1'] = float(m.group(1)) * 1e-3
        if 'f2' not in data:
            m = re.search(r"f2\s*=\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)", block)
            if m:
                data['f2'] = float(m.group(1)) * 1e-3
        if 'd1' not in data:
            m = re.search(r"^d1\s*=\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)", block, re.MULTILINE)
            if m:
                data['d1'] = float(m.group(1)) * 1e-3
        if 'd12' not in data:
            m = re.search(r"^d12\s*=\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)", block, re.MULTILINE)
            if m:
                data['d12'] = float(m.group(1)) * 1e-3
        if 'd2' not in data:
            m = re.search(r"^d2\s*=\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)", block, re.MULTILINE)
            if m:
                data['d2'] = float(m.group(1)) * 1e-3
        if 'd2_ideal' not in data:
            m = re.search(r"^Ideal d2\s*=\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)", block, re.MULTILINE)
            if m:
                data['d2_ideal'] = float(m.group(1)) * 1e-3

    return solutions


def sample_profile(wvlen, w_i, d1, f1, d12, f2, d2, n_points=800):
    z_end = d1 + d12 + d2
    zs = np.linspace(0, z_end, n_points)
    q0 = flat_q(wvlen, w_i)
    ws = []

    for z in zs:
        if z <= d1:
            q = prop_free(q0, z)
        elif z <= d1 + d12:
            q1 = prop_free(q0, d1)
            q2 = prop_lens(q1, f1)
            q = prop_free(q2, z - d1)
        else:
            q1 = prop_free(q0, d1)
            q2 = prop_lens(q1, f1)
            q3 = prop_free(q2, d12)
            q4 = prop_lens(q3, f2)
            q = prop_free(q4, z - d1 - d12)

        invq = 1.0 / q
        imag = invq.imag
        if imag == 0:
            w = float('nan')
        else:
            w = math.sqrt(-wvlen * 1e-9 / (math.pi * imag))
        ws.append(w * 1e6)  # convert to um

    return zs * 1e3, np.array(ws)  # mm, um


def plot_solution(sol):
    wvlen = sol['wvlen']
    f1 = sol['f1']
    f2 = sol['f2']
    d1 = sol['d1']
    d12 = sol['d12']
    d2 = sol['d2']
    d2_ideal = sol.get('d2_ideal', None)
    w_i = sol.get('w_i', None)
    w_c = sol.get('w_c', None)
    w_o = sol.get('w_o', None)
    error = sol.get('error', None)
    frac = sol.get('frac_error', None)
    R_o = sol.get('R_o', None)

    zs_mm, ws_um = sample_profile(wvlen, w_i, d1, f1, d12, f2, d2)

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(zs_mm, ws_um, lw=2)
    ax.set_xlabel('Distance (mm)')
    ax.set_ylabel('Beam radius (μm)')
    ax.set_title(f'{wvlen} nm Mode Profile')

    lens1_x = d1 * 1e3
    lens2_x = (d1 + d12) * 1e3
    d2_x = (d1 + d12 + d2) * 1e3
    ideal_d2_x = (d1 + d12 + d2_ideal) * 1e3 if d2_ideal is not None else None
    if ideal_d2_x is not None:
        x_max = max((d1 + d12 + d2) * 1e3, ideal_d2_x)
        ax.set_xlim(0, x_max * 1.02)
    ax.axvline(lens1_x, color='C1', linestyle='--')
    ax.axvline(lens2_x, color='C1', linestyle='--')
    ax.axvline(d2_x, color='red', linestyle='--', linewidth=1.5)
    if ideal_d2_x is not None:
        ax.axvline(ideal_d2_x, color='tab:green', linestyle=':', linewidth=1.8)
    
    ymax = np.nanmax(ws_um)
    if math.isfinite(ymax):
        y_text = ymax * 0.9
    else:
        y_text = 1.0

    ax.text(lens1_x, y_text, f'f1={f1*1e3:.3f} mm', ha='center', va='bottom')
    ax.text(lens2_x, y_text, f'f2={f2*1e3:.3f} mm', ha='center', va='bottom')
    ax.annotate('d2', xy=(d2_x, y_text), xytext=(0, 8), textcoords='offset points', ha='center', va='bottom', color='red', fontweight='bold')
    if ideal_d2_x is not None:
        ax.annotate('Ideal d2', xy=(ideal_d2_x, y_text), xytext=(0, 22), textcoords='offset points', ha='center', va='bottom', color='tab:green', fontweight='bold')
    
    # Label the lenses at the very top
    y_top = ymax * 1.05
    ax.text(lens1_x, y_top, 'Lens 1', ha='center', va='bottom', fontsize=10, fontweight='bold', color='C1')
    ax.text(lens2_x, y_top, 'Lens 2', ha='center', va='bottom', fontsize=10, fontweight='bold', color='C1')
    
    # Add x-axis labels at lens and cavity positions
    ymin_pos = np.nanmin(ws_um) * 0.95
    ax.text(lens1_x, ymin_pos, f'd1={d1*1e3:.2f}mm', ha='center', va='top', fontsize=11, color='black', fontweight='bold')
    ax.text(lens2_x, ymin_pos, f'd1+d12={lens2_x:.2f}mm', ha='center', va='top', fontsize=11, color='black', fontweight='bold')
    ax.annotate(f'd2={d2*1e3:.2f}mm', xy=(d2_x, ymin_pos), xytext=(0, 40), textcoords='offset points', ha='center', va='top', fontsize=11, color='red', fontweight='bold')
    if ideal_d2_x is not None:
        ax.annotate(f'Ideal d2={d2_ideal*1e3:.2f}mm', xy=(ideal_d2_x, ymin_pos), xytext=(0, 60), textcoords='offset points', ha='center', va='top', fontsize=9, color='tab:green', fontweight='bold')

    # compute beam radius at each lens and annotate (in μm)
    # lens 1 (after free propagation d1)
    try:
        q0 = flat_q(wvlen, w_i)
        q_l1 = prop_free(q0, d1)
        invq_l1 = 1.0 / q_l1
        w_l1 = (math.sqrt(-wvlen * 1e-9 / (math.pi * invq_l1.imag)) * 1e6) if invq_l1.imag != 0 else float('nan')
    except Exception:
        w_l1 = float('nan')

    # lens 2 (after lens1 and propagation d12)
    try:
        q1 = prop_free(q0, d1)
        q2 = prop_lens(q1, f1)
        q_l2 = prop_free(q2, d12)
        invq_l2 = 1.0 / q_l2
        w_l2 = (math.sqrt(-wvlen * 1e-9 / (math.pi * invq_l2.imag)) * 1e6) if invq_l2.imag != 0 else float('nan')
    except Exception:
        w_l2 = float('nan')

    # annotate input (fiber) and cavity waists on the plot
    ymin = np.nanmin(ws_um)
    if not math.isfinite(ymin) or ymax == ymin:
        y_pos = ymax * 0.15
    else:
        y_pos = ymin + 0.05 * (ymax - ymin)

    if w_i is not None:
        ax.text(0.0, y_pos, f'Input (fiber) w = {w_i*1e6:.2f} μm', ha='left', va='bottom', color='C3')
    if w_c is not None:
        cavity_text = f'Cavity w = {w_c*1e6:.2f} μm'
        if w_o is not None:
            cavity_text += f' → Output w = {w_o*1e6:.2f} μm'
        ax.text((d1 + d12 + d2) * 1e3, y_pos, cavity_text, ha='right', va='bottom', color='C3')

    # no legend (user requested); make sure plot area has room
    fig.subplots_adjust(bottom=0.12)

    # info box with ROC and accuracy placed in the plot center to avoid overlap
    roc_str = f"R_o: {'inf' if (R_o is None or not math.isfinite(R_o)) else f'{R_o:.3f} m'}"
    err_str = f"Waist error: {error*1e6:.6f} μm" if error is not None else ""
    frac_str = f"Fractional error: {frac:.3e}" if frac is not None else ''
    info = f"{roc_str}\n{err_str}\n{frac_str}"
    ax.text(0.5, 0.5, info, ha='center', va='center', transform=ax.transAxes,
            bbox=dict(facecolor='white', alpha=0.9, edgecolor='gray'))

    out_name = PLOTS_DIR / f"{wvlen}_nm_mode_profile.png"
    fig.tight_layout()
    fig.savefig(out_name)
    plt.close(fig)
    return out_name


def main():
    sols = parse_results(RESULTS_FILE)
    saved = []
    for sol in sols:
        path = plot_solution(sol)
        saved.append(path)
    print(f"Saved {len(saved)} plots into {PLOTS_DIR}")


if __name__ == '__main__':
    main()
