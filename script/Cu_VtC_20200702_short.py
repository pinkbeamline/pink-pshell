sample_1='s01 (creatinine)2[CuCl4]'
sample_3='s02 Cu(im)4Br2'
sample_4='s03 Cu(im)6Cl2'


#CuCl long scan
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=19000, X1=19900, dX=700, Y0=2500, Y1=8100, passes=50, sample='CuCl', linedelay=0)

#Measurement
print("########## MEASUREMENT ##########")
#1
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=37200, X1=40000, dX=750, Y0=-7500, Y1=8100, passes=15, sample=sample_1, linedelay=0)
#3
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=2100, X1=4800, dX=750, Y0=-7500, Y1=8100, passes=15, sample=sample_3, linedelay=0)
#4
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=-15400, X1=-12600, dX=750, Y0=-7500, Y1=8100, passes=15, sample=sample_4, linedelay=0)

#Damage scan
print("########## DAMAGE SCAN ##########")

caput("PINK:SMA01:m9.VAL", 0.) #Y
caput("PINK:SMA01:m10.VAL", -13500.) #X
scan.spot(detector.eiger(), exposure=5., images=60, sample=sample_4)
caput("PINK:SMA01:m10.VAL", 3500.) #X
scan.spot(detector.eiger(), exposure=5., images=60, sample=sample_3)
caput("PINK:SMA01:m10.VAL", 38500.) #X
scan.spot(detector.eiger(), exposure=5., images=60, sample=sample_1)

caput("PINK:SMA01:m9.VAL", 4000.) #Y
caput("PINK:SMA01:m10.VAL", 21000.) #X
scan.spot(detector.eiger(), exposure=5., images=60, sample='CuCl')

caput("PINK:SMA01:m10.VAL", 0.) #X
caput("PINK:SMA01:m9.VAL", 0.) #Y

print("########## DONE ##########")
pink.shutter_hard_CLOSE()
caput("PINK:PLCVAC:V11close", 1)
caput("PINK:PLCVAC:V12close", 1)
pink.gap(12.0)