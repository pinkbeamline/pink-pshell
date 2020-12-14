sample_1='s4 CuCl2 100 mM'
sample_2='s5 CuCl2 10 mM'
sample_3='s6 CuCl2 1 mM'


#Measurement
print("########## MEASUREMENT ##########")
#1
scan.zigzag_absolute(detector.eiger(), exposure=10, X0=54600, dX=800, Xpoints=2, Y0=3450, dY=50, Ypoints=239, passes=2, sample=sample_1, linedelay=0)
#3
scan.zigzag_absolute(detector.eiger(), exposure=10, X0=68400, dX=800, Xpoints=2, Y0=3450, dY=50, Ypoints=239, passes=2, sample=sample_2, linedelay=0)
#4
scan.zigzag_absolute(detector.eiger(), exposure=10, X0=80300, dX=800, Xpoints=2, Y0=3450, dY=50, Ypoints=239, passes=2, sample=sample_3, linedelay=0)


print("########## DONE ##########")
pink.shutter_hard_CLOSE()
caput("PINK:PLCVAC:V11close", 1)
#caput("PINK:PLCVAC:V16close", 1)
pink.gap(9.0)