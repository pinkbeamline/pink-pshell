#X motion
caput("PINK:PHY:AxisJ.VAL", 11300.)
#Y motion
caput("PINK:ANC01:ACT0:CMD:TARGET", 16000.)
scan.spot(detector.eiger(), exposure=10, images=10, sample='Cu foil, S01 T=22K')

scan.zigzag_absolute(detector.eiger(), exposure=10, X0=22600, dX=700, Xpoints=3, Y0=14000, dY=100, Ypoints=100, passes=2, sample='s02 CuCl2 Kb13 100 mM', linedelay=0)

caput("PINK:PHY:AxisJ.VAL", 35300.)
caput("PINK:ANC01:ACT0:CMD:TARGET", 16000.)
scan.spot(detector.eiger(), exposure=10, images=10, sample='Cu foil, S03 T=22K')

scan.zigzag_absolute(detector.eiger(), exposure=10, X0=46600, dX=700, Xpoints=3, Y0=14000, dY=100, Ypoints=100, passes=2, sample='s04 CuCl2 Kb13 10 mM', linedelay=0)

caput("PINK:PHY:AxisJ.VAL", 59200.)
caput("PINK:ANC01:ACT0:CMD:TARGET", 16000.)
scan.spot(detector.eiger(), exposure=10, images=10, sample='Cu foil, S05 T=22K')

scan.zigzag_absolute(detector.eiger(), exposure=10, X0=70600, dX=700, Xpoints=3, Y0=14000, dY=100, Ypoints=100, passes=2, sample='s06 CuCl2 Kb13 1 mM', linedelay=0)

caput("PINK:PHY:AxisJ.VAL", 82800.)
caput("PINK:ANC01:ACT0:CMD:TARGET", 16000.)
scan.spot(detector.eiger(), exposure=10, images=10, sample='Cu foil, S07 T=22K')

print("########## DONE ##########")
pink.shutter_hard_CLOSE()
pink.gap(9.0)