print("########## ENERGYCALIBRATION ##########")
caput("PINK:SMA01:m10.VAL", 5000.) #X
caput("PINK:SMA01:m9.VAL", -4200) #Y
scan.spot(detector.greateyes(), exposure=1, images=300, sample='Sb La')
caput("PINK:SMA01:m9.VAL", -6100) #Y
scan.spot(detector.greateyes(), exposure=1, images=300, sample='KCl Kb')

#scan.continuous(detector.greateyes(), det_exposure=1, sample_exposure=2, X0=4000, X1=6600, dX=750, Y0=-2500, Y1=8050, passes=4, sample='KCl', linedelay=0) 
scan.continuous(detector.greateyes(), det_exposure=1, sample_exposure=2, X0=-13000, X1=-10500, dX=750, Y0=-7100, Y1=8050, passes=4, sample='KI', linedelay=0) 
scan.continuous(detector.greateyes(), det_exposure=1, sample_exposure=2, X0=39000, X1=41600, dX=750, Y0=-7100, Y1=8050, passes=4, sample='KBr', linedelay=0) 
caput("PINK:SMA01:m10.VAL", 22500.) #X
pink.shutter_hard_CLOSE()
#caput("PINK:PLCVAC:V11close", 1)
#caput("PINK:PLCVAC:V10close", 1)
caput("PINK:GEYES:cam1:Temperature", 20)