print("########## ENERGYCALIBRATION ##########")
caput("PINK:SMA01:m10.VAL", 5000.) #X
caput("PINK:SMA01:m9.VAL", -3500) #Y
scan.spot(detector.greateyes(), exposure=5, images=100, sample='Sb La')
caput("PINK:SMA01:m9.VAL", -5800) #Y
scan.spot(detector.greateyes(), exposure=2, images=200, sample='KCl Kb')

scan.continuous(detector.greateyes(), det_exposure=4, sample_exposure=2, X0=3900, X1=6700, dX=800, Y0=-2100, Y1=8100, passes=1, sample='KCl', linedelay=0)
scan.continuous(detector.greateyes(), det_exposure=4, sample_exposure=0.5, X0=-13300, X1=-10200, dX=800, Y0=-7000, Y1=8100, passes=6, sample='KBr', linedelay=0)
scan.continuous(detector.greateyes(), det_exposure=4, sample_exposure=0.5, X0=21900, X1=24800, dX=800, Y0=-7000, Y1=8100, passes=6, sample='KCO3', linedelay=0) 
print("########## DAMAGE SCAN ##########")
caput("PINK:SMA01:m9.VAL", 3000.) #Y
caput("PINK:SMA01:m10.VAL", 40000.) #X
scan.spot(detector.eiger(), exposure=4., images=125, sample='KI')
caput("PINK:SMA01:m10.VAL", -12000.) #X
scan.spot(detector.eiger(), exposure=4., images=125, sample='KBr')
