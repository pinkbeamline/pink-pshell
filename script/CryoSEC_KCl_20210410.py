#X motion
#caput("PINK:PHY:AxisJ.VAL", 11300.)
#Y motion
#caput("PINK:ANC01:ACT0:CMD:TARGET", 16000.)
scan.zigzag_absolute(detector.greateyes(), exposure=5, X0=11300, dX=700, Xpoints=1, Y0=4500, dY=50, Ypoints=220, passes=2, sample='s#1 30um kapton', linedelay=0)
scan.zigzag_absolute(detector.greateyes(), exposure=5, X0=23200, dX=700, Xpoints=1, Y0=4500, dY=50, Ypoints=220, passes=2, sample='s#2 8um kapton', linedelay=0)
scan.zigzag_absolute(detector.greateyes(), exposure=5, X0=47800, dX=700, Xpoints=1, Y0=4500, dY=50, Ypoints=220, passes=2, sample='s#4 cell', linedelay=0)
scan.zigzag_absolute(detector.greateyes(), exposure=5, X0=60000, dX=700, Xpoints=1, Y0=4500, dY=50, Ypoints=220, passes=2, sample='s#5 H20, 30um kapton', linedelay=0)
scan.zigzag_absolute(detector.greateyes(), exposure=5, X0=71500, dX=700, Xpoints=1, Y0=4500, dY=50, Ypoints=220, passes=2, sample='s#6 KCl1mM, 30um kapton', linedelay=0)

print("########## DONE ##########")
caput("PINK:GEYES:cam1:Temperature", 20)
pink.shutter_hard_CLOSE()
pink.gap(9.0)