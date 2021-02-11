print("########## ENERGYCALIBRATION ##########")
caput("PINK:SMA01:m10.VAL", 5000.) #X
caput("PINK:SMA01:m9.VAL", -3500) #Y
scan.spot(detector.greateyes(), exposure=5, images=100, sample='Sb La')
caput("PINK:SMA01:m9.VAL", -5800) #Y
scan.spot(detector.greateyes(), exposure=2, images=200, sample='KCl Kb')
caput("PINK:SMA01:m9.VAL", 0) #Y
scan.spot(detector.greateyes(), exposure=4, images=100, sample='KCl Kb')
caput("PINK:SMA01:m10.VAL", -12000.) #X
scan.spot(detector.greateyes(), exposure=4, images=100, sample='KCO3 Kb')
caput("PINK:SMA01:m10.VAL", 40800.) #X
scan.spot(detector.greateyes(), exposure=4, images=100, sample='KNO3 Kb')