"""
THIS FILE CONTAINS A SET OF CONSTANTS USED THROUGHOUT THE CODE
"""

'''FIBER MODE CONSTANTS'''

# For 460 - 700 nm, MFD = 3.3 ± 0.5 µm @ 515 nm
# For 970 - 1550nm, MFD = 6.6 ± 0.5 µm @ 980 nm
# For 1270 - 1625 nm, MFD = 9.3 ± 0.5 µm @ 1300 nm
# For 1440 - 1625 nm, MFD = 10.1 ± 0.4 µm @ 1550 nm
map_to_MFR = {1112: 3.3, 556: 1.65, 604: 1.65, 978: 3.3, 1034: 3.3, 1389: 4.65, 1580: 5.05} # in µm



'''CAVITY CONSTANTS'''
R = 0.5  # Characteristic radius of second lens (m)
L = 0.1  # Characteristic length between lenses (m)

'''f2 CONSTANTS'''

map_to_f2 = {1112: 0.3, 556: 0.45, 604: 0.45, 978: 0.3, 1034: 0.45, 1389: 0.5, 1580: 0.25} # in m