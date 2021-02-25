print("########## ENERGYCALIBRATION ##########")
caput("PINK:SMA01:m10.VAL", 5000.) #X
caput("PINK:SMA01:m9.VAL", -5500) #Y
scan.spot(detector.greateyes(), exposure=5, images=100, sample='Sb La')
caput("PINK:SMA01:m9.VAL", -2200) #Y
scan.spot(detector.greateyes(), exposure=2, images=200, sample='KCl Kb')

scan.continuous(detector.greateyes(), det_exposure=4, sample_exposure=2, X0=4000, X1=6700, dX=800, Y0=-2000, Y1=8000, passes=1, sample='KCl', linedelay=0)
scan.continuous(detector.greateyes(), det_exposure=4, sample_exposure=0.5, X0=-13300, X1=-10200, dX=800, Y0=-6900, Y1=8000, passes=8, sample='KBr', linedelay=0)
scan.continuous(detector.greateyes(), det_exposure=4, sample_exposure=0.5, X0=39600, X1=42200, dX=800, Y0=-6900, Y1=8000, passes=8, sample='KI', linedelay=0) 
print("########## DAMAGE SCAN ##########")
caput("PINK:SMA01:m9.VAL", 0.) #Y
caput("PINK:SMA01:m10.VAL", 40500.) #X
scan.spot(detector.greateyes(), exposure=4., images=125, sample='KI')
caput("PINK:SMA01:m10.VAL", -12000.) #X
scan.spot(detector.greateyes(), exposure=4., images=125, sample='KBr')

 