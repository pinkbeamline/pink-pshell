sample_1='s1 Co(NO3)2 6H2O'
sample_2='s2 Co2FeO4'
sample_3='s3 Co2.5Fe0.5O4'


#Co(OH)2 commercial, Kb1,3 and V2C
scan.continuous(detector.eiger(), det_exposure=2, sample_exposure=0.5, X0=23500, X1=24000, dX=700, Y0=300, Y1=8100, passes=10, sample='Co(OH)2', linedelay=0)

#Measurement
print("########## MEASUREMENT ##########")
#1
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=39200, X1=41600, dX=780, Y0=-7000, Y1=8100, passes=12, sample=sample_1, linedelay=0)
#2
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=1300, X1=4000, dX=780, Y0=-7000, Y1=8100, passes=12, sample=sample_2, linedelay=0)
#3
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=-13300, X1=-10800, dX=780, Y0=-7000, Y1=8100, passes=12, sample=sample_3, linedelay=0)

#Damage scan
print("########## DAMAGE SCAN ##########")

caput("PINK:SMA01:m9.VAL", 0.) #Y
caput("PINK:SMA01:m10.VAL", -12000.) #X
scan.spot(detector.eiger(), exposure=2., images=80, sample=sample_3)
caput("PINK:SMA01:m10.VAL", 2500.) #X
scan.spot(detector.eiger(), exposure=2., images=80, sample=sample_2)
caput("PINK:SMA01:m10.VAL", 39500.) #X
scan.spot(detector.eiger(), exposure=2., images=80, sample=sample_1)
caput("PINK:SMA01:m10.VAL", 0.) #X
print("########## DONE ##########")
pink.shutter_hard_CLOSE()
#caput("PINK:PLCVAC:V11close", 1)
#caput("PINK:PLCVAC:V12close", 1)
pink.gap(8.0)