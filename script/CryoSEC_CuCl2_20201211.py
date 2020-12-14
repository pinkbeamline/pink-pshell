sample_1='s4 CuCl2 100 mM'
sample_2='s5 CuCl2 10 mM'
sample_3='s6 CuCl2 1 mM'

print("########## ENERGY CALIBRATION ##########")
scan.zigzag_absolute(detector.eiger(), exposure=10, X0=19400, dX=0, Xpoints=1, Y0=6700, dY=10, Ypoints=50, passes=1, sample='s1 Zn foil', linedelay=0)
scan.zigzag_absolute(detector.eiger(), exposure=5, X0=19400, dX=0, Xpoints=1, Y0=13000, dY=10, Ypoints=60, passes=1, sample='s1 Cu foil', linedelay=0)
scan.zigzag_absolute(detector.eiger(), exposure=5, X0=31400, dX=0, Xpoints=1, Y0=13000, dY=10, Ypoints=60, passes=1, sample='s2 Cu foil', linedelay=0)
scan.zigzag_absolute(detector.eiger(), exposure=5, X0=43400, dX=0, Xpoints=1, Y0=13000, dY=10, Ypoints=60, passes=1, sample='s3 Cu foil', linedelay=0)
scan.zigzag_absolute(detector.eiger(), exposure=5, X0=91000, dX=0, Xpoints=1, Y0=13000, dY=10, Ypoints=60, passes=1, sample='s7 Cu foil', linedelay=0)

x1_center=19400
#Measurement
print("########## MEASUREMENT ##########")
#s#4
x4_center=x1_center+36000
scan.zigzag_absolute(detector.eiger(), exposure=10, X0=x4_center-1500, dX=0, Xpoints=1, Y0=4050, dY=45, Ypoints=270, passes=1, sample=sample_1, linedelay=0)
scan.zigzag_absolute(detector.eiger(), exposure=10, X0=x4_center-750, dX=0, Xpoints=1, Y0=4050, dY=45, Ypoints=270, passes=1, sample=sample_1, linedelay=0)
scan.zigzag_absolute(detector.eiger(), exposure=10, X0=x4_center, dX=0, Xpoints=1, Y0=4050, dY=45, Ypoints=270, passes=1, sample=sample_1, linedelay=0)
scan.zigzag_absolute(detector.eiger(), exposure=10, X0=x4_center+750, dX=0, Xpoints=1, Y0=4050, dY=45, Ypoints=270, passes=1, sample=sample_1, linedelay=0)
scan.zigzag_absolute(detector.eiger(), exposure=10, X0=x4_center+1500, dX=0, Xpoints=1, Y0=4050, dY=45, Ypoints=270, passes=1, sample=sample_1, linedelay=0)
#s#4
x5_center=x1_center+48000
scan.zigzag_absolute(detector.eiger(), exposure=10, X0=x5_center-1500, dX=0, Xpoints=1, Y0=4050, dY=45, Ypoints=270, passes=1, sample=sample_2, linedelay=0)
scan.zigzag_absolute(detector.eiger(), exposure=10, X0=x5_center-750, dX=0, Xpoints=1, Y0=4050, dY=45, Ypoints=270, passes=1, sample=sample_2, linedelay=0)
scan.zigzag_absolute(detector.eiger(), exposure=10, X0=x5_center, dX=0, Xpoints=1, Y0=4050, dY=45, Ypoints=270, passes=1, sample=sample_2, linedelay=0)
scan.zigzag_absolute(detector.eiger(), exposure=10, X0=x5_center+750, dX=0, Xpoints=1, Y0=4050, dY=45, Ypoints=270, passes=1, sample=sample_2, linedelay=0)
scan.zigzag_absolute(detector.eiger(), exposure=10, X0=x5_center+1500, dX=0, Xpoints=1, Y0=4050, dY=45, Ypoints=270, passes=1, sample=sample_2, linedelay=0)
#s#4
x6_center=x1_center+60000
scan.zigzag_absolute(detector.eiger(), exposure=10, X0=x6_center-1500, dX=0, Xpoints=1, Y0=4050, dY=45, Ypoints=270, passes=1, sample=sample_3, linedelay=0)
scan.zigzag_absolute(detector.eiger(), exposure=10, X0=x6_center-750, dX=0, Xpoints=1, Y0=4050, dY=45, Ypoints=270, passes=1, sample=sample_3, linedelay=0)
scan.zigzag_absolute(detector.eiger(), exposure=10, X0=x6_center, dX=0, Xpoints=1, Y0=4050, dY=45, Ypoints=270, passes=1, sample=sample_3, linedelay=0)
scan.zigzag_absolute(detector.eiger(), exposure=10, X0=x6_center+750, dX=0, Xpoints=1, Y0=4050, dY=45, Ypoints=270, passes=1, sample=sample_3, linedelay=0)
scan.zigzag_absolute(detector.eiger(), exposure=10, X0=x6_center+1500, dX=0, Xpoints=1, Y0=4050, dY=45, Ypoints=270, passes=1, sample=sample_3, linedelay=0)


print("########## DONE ##########")
pink.shutter_hard_CLOSE()
caput("PINK:PLCVAC:V11close", 1)
#caput("PINK:PLCVAC:V16close", 1)
pink.gap(8.0) 

