#X motion
#caput("PINK:PHY:AxisJ.VAL", 11300.)
#Y motion
#caput("PINK:ANC01:ACT0:CMD:TARGET", 16000.)
scan.spot(detector.greateyes(), exposure=5, images=60, sample='S#7 Sb La1,2')

scan.zigzag_absolute(detector.greateyes(), exposure=5, X0=72500, dX=700, Xpoints=1, Y0=4000, dY=50, Ypoints=220, passes=2, sample='s#6 KCl 10mM, 8um kapton', linedelay=0)
scan.zigzag_absolute(detector.greateyes(), exposure=5, X0=60000, dX=700, Xpoints=1, Y0=4000, dY=50, Ypoints=220, passes=2, sample='s#5 KCl 1mM, 8um kapton', linedelay=0)
scan.zigzag_absolute(detector.greateyes(), exposure=5, X0=48300, dX=700, Xpoints=1, Y0=4000, dY=50, Ypoints=220, passes=2, sample='s#4 KCl 1mM, 8um kapton', linedelay=0)
scan.zigzag_absolute(detector.greateyes(), exposure=5, X0=36500, dX=700, Xpoints=1, Y0=4000, dY=50, Ypoints=220, passes=2, sample='s#3 KCl 1mM, 30um kapton', linedelay=0)


caput("PINK:PHY:AxisJ.VAL", 24400.)
caput("PINK:ANC01:ACT0:CMD:TARGET", 15000.)
scan.spot(detector.greateyes(), exposure=5, images=60, sample='S#2 Kapton 8um')
caput("PINK:ANC01:ACT0:CMD:TARGET", 5000.)
scan.spot(detector.greateyes(), exposure=5, images=60, sample='S#2 Sb La1,2')

scan.zigzag_absolute(detector.greateyes(), exposure=3, X0=12500, dX=700, Xpoints=1, Y0=4000, dY=50, Ypoints=220, passes=2, sample='s#1 KCl powder, 30um kapton', linedelay=0)


print("########## DONE ##########")
pink.shutter_hard_CLOSE()
pink.gap(9.0)