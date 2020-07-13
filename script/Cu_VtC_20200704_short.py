sample_1='s14 Cu(OAc)2H20'
#sample_2 energy calibration sample
sample_3='s15 Cu(OTf)'
sample_4='s16 [NEt4]2[CuCl4]'

print("########## ENERGYCALIBRATION ##########")
caput("PINK:SMA01:m10.VAL", 21000.) #X
caput("PINK:SMA01:m9.VAL", -5000.) #Y
#Cu foil Kb1,3
##scan.spot(detector.eiger(), exposure=5., images=40, sample='Cu foil')
#Zn foil Ka1,2
##caput("PINK:SMA01:m9.VAL", -1500.) #Y
##scan.spot(detector.eiger(), exposure=10., images=30, sample='Zn foil')
#Ho La1,2
##caput("PINK:SMA01:m9.VAL", 1000.) #Y
#scan.spot(detector.eiger(), exposure=10., images=10, sample='Ho foil')
#CuCl Kb1,3
##caput("PINK:SMA01:m9.VAL", 2900.) #Y
##scan.spot(detector.eiger(), exposure=10., images=80, sample='CuCl')

#Measurement
print("########## MEASUREMENT ##########")
#1
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=37300, X1=40000, dX=750, Y0=-7500, Y1=8100, passes=2, sample=sample_1, linedelay=0)
#3
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=2300, X1=4800, dX=750, Y0=-7500, Y1=8100, passes=5, sample=sample_3, linedelay=0)
#4
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=-15200, X1=-12600, dX=750, Y0=-7500, Y1=8100, passes=10, sample=sample_4, linedelay=0)

#Damage scan
print("########## DAMAGE SCAN ##########")

caput("PINK:SMA01:m9.VAL", 0.) #Y
caput("PINK:SMA01:m10.VAL", -13500.) #X
scan.spot(detector.eiger(), exposure=10., images=60, sample=sample_4)
caput("PINK:SMA01:m10.VAL", 3500.) #X
scan.spot(detector.eiger(), exposure=10., images=60, sample=sample_3)
caput("PINK:SMA01:m10.VAL", 38500.) #X
scan.spot(detector.eiger(), exposure=10., images=60, sample=sample_1)

caput("PINK:SMA01:m10.VAL", 0.) #X
caput("PINK:SMA01:m9.VAL", 0.) #Y

print("########## DONE ##########")
#pink.shutter_hard_CLOSE()
#caput("PINK:PLCVAC:V11close", 1)
#caput("PINK:PLCVAC:V12close", 1)
#pink.gap(12.0)