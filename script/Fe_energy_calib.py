#Energy calibration
#Cobalt Ka1,2
caput("PINK:SMA01:m10.VAL", -13000.) #X
caput("PINK:SMA01:m9.VAL", 1550.) #Y
scan.spot(detector.eiger(), exposure=1., images=20, sample='Co foil')
#Fe foil, Kb1,3 and V2C
caput("PINK:SMA01:m10.VAL", -13000.) #X
caput("PINK:SMA01:m9.VAL", -3100.) #Y
scan.spot(detector.eiger(), exposure=2., images=100, sample='Fe foil')
#Fe2O3, Kb1,3 and V2C
caput("PINK:SMA01:m10.VAL", 4000.) #X
caput("PINK:SMA01:m9.VAL", 420.) #Y
scan.spot(detector.eiger(), exposure=2., images=100, sample='Fe2O3')

#scan.continuous(detector.eiger(), det_exposure=2, sample_exposure=0.2, X0=21300, X1=23100, dX=600, Y0=-7400, Y1=8000, passes=5, sample='Fe(acac)2_solid', linedelay=0)