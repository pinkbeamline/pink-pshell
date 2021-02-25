sample_2='s1.2 CuCl'
sample_3='s2.3 FO-208 Cu(II)(Tmeda)2OTf2'


print("########## ENERGYCALIBRATION ##########")
caput("PINK:SMA01:m10.VAL", 22800.) #X
caput("PINK:SMA01:m9.VAL", -4800.) #Y
#Cu foil Kb1,3
scan.spot(detector.eiger(), exposure=5., images=100, sample='Cu foil')
#Zn foil Ka1,2
caput("PINK:SMA01:m9.VAL", -1600.) #Y
scan.spot(detector.eiger(), exposure=10., images=50, sample='Zn foil')
#Ho La1,2
caput("PINK:SMA01:m9.VAL", 900.) #Y
scan.spot(detector.eiger(), exposure=10., images=15, sample='Ho foil')


#CuCl long scan fro the energy calibration
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=21300, X1=24200, dX=800, Y0=2300, Y1=8150, passes=6, sample='CuCl', linedelay=0)
#Measurement
print("########## MEASUREMENT ##########")

#3
scan.ccontinuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=4200, X1=6500, dX=750, Y0=-5800, Y1=7500, passes=14, sample=sample_3, linedelay=0)

#Damage scan
print("########## DAMAGE SCAN ##########")

caput("PINK:SMA01:m9.VAL", 3000.) #Y
caput("PINK:SMA01:m10.VAL", 5500.) #X
scan.spot(detector.eiger(), exposure=10., images=60, sample=sample_3)
