#Energy calibration
print("########## ENERGYCALIBRATION ##########")
caput("PINK:SMA01:m10.VAL", -13500.) #X
caput("PINK:SMA01:m9.VAL", -5500.) #Y

scan.spot(detector.eiger(), exposure=5., images=40, sample='Ni foil')

caput("PINK:SMA01:m9.VAL", -2500.) #Y
scan.spot(detector.eiger(), exposure=2., images=200, sample='Co foil')
#Co(OH)2 commercial, Kb1,3 and V2C
scan.continuous(detector.eiger(), det_exposure=2, sample_exposure=0.5, X0=-14500, X1=-15000, dX=700, Y0=0, Y1=8100, passes=10, sample='Co(OH)2 Kb1,3', linedelay=0)