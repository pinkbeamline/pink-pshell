#X motion
caput("PINK:PHY:AxisJ.VAL", 23200.)
#Y motion
caput("PINK:ANC01:ACT0:CMD:TARGET", 15000.)
scan.spot(detector.eiger(), exposure=10, images=10, sample='Cu foil, S02 T=22K')

scan.zigzag_absolute(detector.eiger(), exposure=10, X0=33800, dX=700, Xpoints=5, Y0=4000, dY=100, Ypoints=100, passes=1, sample='s03 CuCl2 Kb13 100 mM', linedelay=0)

scan.zigzag_absolute(detector.eiger(), exposure=10, X0=45400, dX=700, Xpoints=5, Y0=4000, dY=100, Ypoints=100, passes=1, sample='s05 CuCl2 Kb13 10 mM', linedelay=0)

scan.zigzag_absolute(detector.eiger(), exposure=10, X0=57600, dX=700, Xpoints=5, Y0=4000, dY=100, Ypoints=100, passes=1, sample='s06 CuCl2 Kb13 1 mM', linedelay=0)

caput("PINK:PHY:AxisJ.VAL", 83000.)
caput("PINK:ANC01:ACT0:CMD:TARGET", 15000.)
scan.spot(detector.eiger(), exposure=10, images=10, sample='Cu foil, S07 T=22K')

print("########## DONE ##########")
