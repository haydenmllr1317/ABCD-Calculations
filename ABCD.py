from constants import map_to_MFR, R, L, map_to_f2
import math

def cavity_waist(wvlen):
    """
    Calculate the beam waist of a Gaussian beam in a cavity.

    Parameters
    ----------
    wvlen : float
        Wavelength of the light (m)

    Returns
    -------
    float
        Beam waist (the radius of the beam at its narrowest point) (m)
    """
    return math.sqrt(math.sqrt(L*(R-L))*(wvlen*1e-9)/(math.pi))

def perfect_distance(wvlen, w, desired_w):
    """
    Given a beam waist w and a desired output waist desired_w, calculate the distance to propagate the beam to achieve the desired waist.

    Parameters
    ----------
    wvlen : float
        Wavelength of the light (m)
    w : float
        The current beam waist (m)
    desired_w : float
        The desired beam waist (m)
    """
    return math.sqrt((desired_w**2)-(w**2))*(math.pi*w/(wvlen*1e-9))

def flat_q(wvlen, w0):
    """
    Calculate the complex beam parameter for a flat wavefront.

    Parameters
    ----------
    w0 : float
        The beam waist (m)

    Returns
    -------
    complex
        The complex beam parameter (m)
    """
    return 1j*(math.pi*(w0**2))/(wvlen*1e-9)

def prop_free(q,d):
    """
    Propagate a Gaussian beam through free space.

    Parameters
    ----------
    q : complex
        The complex beam parameter at the input plane.
    d : float
        The distance to propagate the beam.

    Returns
    -------
    complex
        The complex beam parameter at the output plane.
    """
    return q + d

def prop_lens(q,f):
    """
    Propagate a Gaussian beam through a thin lens.

    Parameters
    ----------
    q : complex
        The complex beam parameter at the input plane.
    f : float
        The focal length of the lens.

    Returns
    -------
    complex
        The complex beam parameter at the output plane.
    """
    return 1/(1/q - 1/f)

def my_prop(q,d1,f1,d12,f2):
    """
    Propagate a Gaussian beam through a system of two lenses separated by free space.

    Parameters
    ----------
    q : complex
        The complex beam parameter at the input plane.
    d1 : float
        The distance from the input plane to the first lens.
    f1 : float
        The focal length of the first lens.
    d12 : float
        The distance between the two lenses.
    f2 : float
        The focal length of the second lens.
    d2 : float
        The distance from the second lens to the output plane.

    Returns
    -------
    complex
        The complex beam parameter at the output plane.
    """
    q1 = prop_free(q,d1)
    q2 = prop_lens(q1,f1)
    q3 = prop_free(q2,d12)
    q4 = prop_lens(q3,f2)
    d2 = abs(q4.real) 
    q5 = prop_free(q4,abs(q4.real)) # this ensure we go directly to the waist. 
    # print(f"q1: {q1}, q2: {q2}, q3: {q3}, q4: {q4}, q5: {q5}")
    return q5, d2

def runner(wvlen, d1, f1, d12):
    f2 = map_to_f2[wvlen] # in m
    w_i = map_to_MFR[wvlen]*1e-6 # waist of the input fiber mode (m)
    w_c = cavity_waist(wvlen)  # Cavity mode waist (m)
    q = flat_q(wvlen, w_i)  # Calculate complex beam parameter (m)
    q_out, d2 = my_prop(q, d1, f1, d12, f2)  # Propagate through the system
    try:
        R_o = 1/((1/q_out).real) # ROC of output beam (m).q
    except ZeroDivisionError:
        R_o = float('inf')  # Handle the case where the real part is zero (flat wavefront)
    w_o = math.sqrt(-wvlen*1e-9/(((1/q_out).imag)*math.pi))  # Calculate output waist (m)
    return w_i, w_c, w_o, R_o, d2

def main():
    wvlen = 556
    ideal_waist = 0.00052 # 0.52 m
    # d1 = 0.0047235
    # f1 = 0.0047235
    d1 = perfect_distance(wvlen, map_to_MFR[wvlen]*1e-6, ideal_waist)
    f1 = d1
    d12 = 0
    # d12 = 0.195
    # f2 = 0.5
    w_i, w_c, w_o, R_o, d2 = runner(wvlen, d1, f1, d12)
    print('Ideal waist: 0.52 mm')
    print(f"Input wavelength: {wvlen} nm")
    print(f"Input distance 1: {d1:.6f} m")
    print(f"Input distance 2: {d2:.6f} m")
    print(f"Input waist: {w_i*1e6} μm")
    print(f"Cavity waist: {w_c*1e6} μm")
    print(f"Output waist: {w_o*1e6} μm")
    print(f"Waist difference: {abs(w_o - w_c)*1e6} μm")
    print(f"As a fraction: {abs(w_o - w_c)/w_c}")
    print(f"Output R: {R_o:.4f}")


if __name__ == "__main__":
    main()