sample_1='s18 CoFe2O4'
sample_2='s19 Co0.5Fe2.5O4'
sample_3='s20 Co1.5Fe1.5O4'

print("########## ENERGYCALIBRATION ##########")
caput("PINK:SMA01:m10.VAL", 21000.) #X
caput("PINK:SMA01:m9.VAL", -5500.) #Y
#Ni Kb1,3
scan.spot(detector.eiger(), exposure=5., images=40, sample='Ni foil')
#Co foil, Kb1,3 and V2C
caput("PINK:SMA01:m9.VAL", -2500.) #Y
scan.spot(detector.eiger(), exposure=2., images=200, sample='Co foil')
#Co(OH)2 commercial, Kb1,3 and V2C
scan.continuous(detector.eiger(), det_exposure=2, sample_exposure=0.5, X0=19500, X1=20000, dX=700, Y0=0, Y1=8100, passes=10, sample='Co(OH)2', linedelay=0)

#Measurement
print("########## MEASUREMENT ##########")
#1
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=36700, X1=39000, dX=750, Y0=-7500, Y1=8100, passes=6, sample=sample_1, linedelay=0)
#2
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=2600, X1=5000, dX=750, Y0=-7500, Y1=8100, passes=12, sample=sample_2, linedelay=0)
#3
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=-15200, X1=-12500, dX=750, Y0=-7500, Y1=8100, passes=6, sample='sample_3', linedelay=0)

#Damage scan
print("########## DAMAGE SCAN ##########")

caput("PINK:SMA01:m9.VAL", 0.) #Y
caput("PINK:SMA01:m10.VAL", -13500.) #X
scan.spot(detector.eiger(), exposure=2., images=60, sample=sample_3)
caput("PINK:SMA01:m10.VAL", 3500.) #X
scan.spot(detector.eiger(), exposure=2., images=60, sample=sample_2)
caput("PINK:SMA01:m10.VAL", 38000.) #X
scan.spot(detector.eiger(), exposure=2., images=60, sample=sample_1)
caput("PINK:SMA01:m10.VAL", 0.) #X
print("########## DONE ##########")
#pink.shutter_hard_CLOSE()
#caput("PINK:PLCVAC:V11close", 1)
#caput("PINK:PLCVAC:V12close", 1)
#pink.gap(12.0)