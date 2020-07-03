
print("########## ENERGYCALIBRATION ##########")
caput("PINK:SMA01:m10.VAL", 21000.) #X
caput("PINK:SMA01:m9.VAL", -5200.) #Y

#Ni Ka1,2
scan.spot(detector.eiger(), exposure=5., images=40, sample='Ni foil')
#Co foil, Kb1,3 and V2C
caput("PINK:SMA01:m10.VAL", 21000.) #X
caput("PINK:SMA01:m9.VAL", -3300.) #Y
scan.spot(detector.eiger(), exposure=2., images=200, sample='Co foil')
#Co(OH)2 commercial, Kb1,3 and V2C
scan.continuous(detector.eiger(), det_exposure=2, sample_exposure=0.5, X0=21200, X1=22000, dX=700, Y0=4050, Y1=8100, passes=20, sample='Co(OH)2', linedelay=0)

#caput("PINK:SMA01:m10.VAL", 3000.) #X
#caput("PINK:SMA01:m9.VAL", 6500.) #Y
#scan.spot(detector.eiger(), exposure=2., images=200, sample='Co foil #1 KMC-2')
#caput("PINK:SMA01:m9.VAL", 0.) #Y
#scan.spot(detector.eiger(), exposure=2., images=200, sample='Co foil #2 ')
#caput("PINK:SMA01:m9.VAL", -3000.) #Y
#scan.spot(detector.eiger(), exposure=2., images=200, sample='Co foil #3 under kapton')