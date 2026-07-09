"""
THIS FILE CONTAINS A SET OF CONSTANTS USED THROUGHOUT THE CODE
"""

'''FIBER MODE CONSTANTS'''

# For 460 - 700 nm, MFD = 3.3 ± 0.5 µm @ 515 nm
# For 970 - 1550nm, MFD = 6.6 ± 0.5 µm @ 980 nm
# For 1270 - 1625 nm, MFD = 9.3 ± 0.5 µm @ 1300 nm
# For 1440 - 1625 nm, MFD = 10.1 ± 0.4 µm @ 1550 nm
wvln_to_MFR = {1112: 3.3, 556: 1.65, 604: 1.65, 978: 3.3, 1034: 3.3, 1389: 4.65, 1580: 5.05} # in µm



'''CAVITY CONSTANTS'''
R = 0.5  # Characteristic radius of second lens (m)
L = 0.1  # Characteristic length between lenses (m)

'''f CONSTANTS'''
wvln_to_f1= {1112: 0.0045, 556: 0.0045, 604: 0.0055, 978: 0.0096, 1034: 0.0075, 1389: 0.008, 1580: 0.0055} # in m (THESE MINIMIZE BEAM WAIST RADIUS ERROR)
# wvln_to_f1_250 = {1112: 0.0045, 556: 0.0045, 604: 0.0055, 978: 0.0096, 1034: 0.0075, 1389: 0.008, 1580: 0.0055} # in m (THESE MINIMIZE BEAM WAIST RADIUS ERROR)
# wvln_to_f2 = {1112: 0.3, 556: 0.45, 604: 0.45, 978: 0.3, 1034: 0.45, 1389: 0.5, 1580: 0.25} # in m
wvln_to_f2 = {1112: 0.35, 556: 0.5, 604: 0.6, 978: 0.75, 1034: 0.6, 1389: 0.5, 1580: 0.35} # in m

'''IDEAL d2 CONSTANTS'''
wvln_to_ideal_d2 = {1112: 0.376, 556: 0.515, 604: 0.535, 978: 0.6855, 1034: 0.5315, 1389: 0.5115, 1580: 0.3725} # in m
wvln_to_d2_min = {1112: 0.365, 556: 0.504, 604: 0.535, 978: 0.6855, 1034: 0.5315, 1389: 0.5005, 1580: 0.3615} # in m
wvln_to_d2_max = {1112: 0.376, 556: 0.515, 604: 0.605, 978: 0.755, 1034: 0.605, 1389: 0.5115, 1580: 0.3725} # in m