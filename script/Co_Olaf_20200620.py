#Energy calibration
#Ni Ka1,2
print("########## ENERGYCALIBRATION ##########")
caput("PINK:SMA01:m10.VAL", 21000.) #X
caput("PINK:SMA01:m9.VAL", -5000.) #Y
scan.spot(detector.eiger(), exposure=5., images=40, sample='Ni foil')
#Co foil, Kb1,3 and V2C
caput("PINK:SMA01:m10.VAL", 21000.) #X
caput("PINK:SMA01:m9.VAL", -3500.) #Y
scan.spot(detector.eiger(), exposure=2., images=200, sample='Co foil')
#Co(OH)2 commercial, Kb1,3 and V2C
scan.continuous(detector.eiger(), det_exposure=2, sample_exposure=0.5, X0=19300, X1=19500, dX=700, Y0=4050, Y1=8100, passes=20, sample='Co(OH)2', linedelay=0)

#Measurement
print("########## MEASUREMENT ##########")
#S1
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=37300, X1=40000, dX=750, Y0=-7500, Y1=8100, passes=6, sample='s04 KIT-32', linedelay=0)
#S2
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=2500, X1=4800, dX=750, Y0=-7500, Y1=8100, passes=6, sample='s05 KIT-3', linedelay=0)
#S3
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=-15100, X1=-12400, dX=750, Y0=-7500, Y1=8100, passes=6, sample='s6 Co3O4 SBA', linedelay=0)

#Damage scan
print("########## DAMAGE SCAN ##########")

caput("PINK:SMA01:m9.VAL", 0.) #Y
caput("PINK:SMA01:m10.VAL", -13500.) #X
scan.spot(detector.eiger(), exposure=2., images=60, sample='s04 KIT-32')
caput("PINK:SMA01:m10.VAL", 3500.) #X
scan.spot(detector.eiger(), exposure=2., images=60, sample='s05 KIT-3')
caput("PINK:SMA01:m10.VAL", 38500.) #X
scan.spot(detector.eiger(), exposure=2., images=60, sample='s04 KIT-32')
caput("PINK:SMA01:m10.VAL", 0.) #X
print("########## DONE ##########")