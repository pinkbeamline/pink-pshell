sample_1='s3.1 CJ-115-01 [Cu(II)(3a4a)EtOH]OTf2'
sample_2='s3.2 CuCl'
sample_3='s3.3 FO-180-01 Cu(II)CF3CO2)2'
sample_4='s3.4 FO-207 [Cu(II)(tpy)EtOH]OTf2'

print("########## ENERGYCALIBRATION ##########")
caput("PINK:SMA01:m10.VAL", 23000.) #X
caput("PINK:SMA01:m9.VAL", -4600.) #Y
#Cu foil Kb1,3
scan.spot(detector.eiger(), exposure=5., images=240, sample='Cu foil')
#Zn foil Ka1,2
caput("PINK:SMA01:m9.VAL", -1300.) #Y
scan.spot(detector.eiger(), exposure=10., images=50, sample='Zn foil')
#Ho La1,2
caput("PINK:SMA01:m9.VAL", 900.) #Y
scan.spot(detector.eiger(), exposure=10., images=15, sample='Ho foil')
#CuCl Kb1,3
caput("PINK:SMA01:m10.VAL", 22500.) #X
caput("PINK:SMA01:m9.VAL", 2200.) #Y
scan.spot(detector.eiger(), exposure=5., images=60, sample='CuCl')

#CuCl long scan fro the energy calibration
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=21600, X1=24300, dX=800, Y0=2100, Y1=8150, passes=12, sample='CuCl', linedelay=0)
#Measurement
print("########## MEASUREMENT ##########")
#1
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=38800, X1=41500, dX=800, Y0=-6500, Y1=8130, passes=14, sample=sample_1, linedelay=0)
#3
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=4300, X1=6800, dX=800, Y0=-6500, Y1=8130, passes=14, sample=sample_3, linedelay=0)
#4
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=-13500, X1=-11000, dX=750, Y0=-6500, Y1=8130, passes=14  , sample=sample_4, linedelay=0)


#Damage scan
print("########## DAMAGE SCAN ##########")

caput("PINK:SMA01:m9.VAL", 3000.) #Y
caput("PINK:SMA01:m10.VAL", -12500.) #X
scan.spot(detector.eiger(), exposure=10., images=60, sample=sample_4)
caput("PINK:SMA01:m10.VAL", 5500.) #X
scan.spot(detector.eiger(), exposure=10., images=60, sample=sample_3)
caput("PINK:SMA01:m10.VAL", 40000.) #X
scan.spot(detector.eiger(), exposure=10., images=60, sample=sample_1)

print("########## DONE ##########")
pink.shutter_hard_CLOSE()
caput("PINK:PLCVAC:V11close", 1)
caput("PINK:PLCVAC:V12close", 1)
#caput("PINK:PLCVAC:V16close", 1)
caput("PINK:SMA01:m10.VAL", 0.) #X
caput("PINK:SMA01:m9.VAL", 0.) #Y
#pink.gap(9.0)