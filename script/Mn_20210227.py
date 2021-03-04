sample_1='s1 Mn(II) acac'
sample_2='s2 Mn(III) acac'
sample_3='s3 MnO'
sample_4='s4 Mn(II)H3O2TMC2 SJ-066-02'

#print("########## ENERGYCALIBRATION ##########")
caput("PINK:SMA01:m10.VAL", 5000.) #X
caput("PINK:SMA01:m9.VAL", -6000.) #Y
#Fe Ka1,2
scan.spot(detector.eiger(), exposure=1.0, images=20, sample='Fe foil, Ka1,2')
#MnO Kb1,3
#caput("PINK:SMA01:m9.VAL", -4100.) #Y
#scan.spot(detector.eiger(), exposure=2., images=200, sample='MnO Kb')

#MnO long scan for the energy calibration
scan.continuous(detector.eiger(), det_exposure=4, sample_exposure=0.5, X0=21500, X1=24000, dX=800, Y0=-4000, Y1=8130, passes=10, sample=sample_3, linedelay=0)
#Measurement
print("########## MEASUREMENT ##########")
#1
scan.continuous(detector.eiger(), det_exposure=4, sample_exposure=0.5, X0=39200, X1=41600, dX=800, Y0=-6500, Y1=8130, passes=12, sample=sample_1, linedelay=0)
#3
scan.continuous(detector.eiger(), det_exposure=4, sample_exposure=0.5, X0=21400, X1=24000, dX=750, Y0=-6500, Y1=8130, passes=12, sample=sample_2, linedelay=0)
#4
scan.continuous(detector.eiger(), det_exposure=4, sample_exposure=0.5, X0=-12500, X1=-10100, dX=750, Y0=-6500, Y1=8130, passes=12  , sample=sample_4, linedelay=0)

#Damage scan
print("########## DAMAGE SCAN ##########")

caput("PINK:SMA01:m9.VAL", 8150.) #Y
caput("PINK:SMA01:m10.VAL", -11000.) #X
scan.spot(detector.eiger(), exposure=2., images=200, sample=sample_4)
caput("PINK:SMA01:m10.VAL", 22500.) #X
scan.spot(detector.eiger(), exposure=2., images=200, sample=sample_2)
caput("PINK:SMA01:m10.VAL", 40000.) #X
scan.spot(detector.eiger(), exposure=2., images=200, sample=sample_1)

print("########## DONE ##########")
pink.shutter_hard_CLOSE()
caput("PINK:PLCVAC:V11close", 1)
caput("PINK:PLCVAC:V12close", 1)
#caput("PINK:PLCVAC:V16close", 1)
caput("PINK:SMA01:m10.VAL", 0.) #X
caput("PINK:SMA01:m9.VAL", 0.) #Y
pink.gap(9.0)