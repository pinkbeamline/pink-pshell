sample_1='s1.1 Cu(I)(MeCN)4'
sample_2='s1.2 CuCl'
sample_3='s1.3 Cu(I) IG-5'
sample_4='s1.4 Cu(I) IG-1 batch 159'

print("########## ENERGYCALIBRATION ##########")
caput("PINK:SMA01:m10.VAL", 22500.) #X
caput("PINK:SMA01:m9.VAL", -4600.) #Y
#Cu foil Kb1,3
scan.spot(detector.eiger(), exposure=5., images=60, sample='Cu foil')
#Zn foil Ka1,2
caput("PINK:SMA01:m9.VAL", -1300.) #Y
scan.spot(detector.eiger(), exposure=10., images=50, sample='Zn foil')
#Ho La1,2
caput("PINK:SMA01:m9.VAL", 900.) #Y
scan.spot(detector.eiger(), exposure=10., images=15, sample='Ho foil')
#CuCl Kb1,3
caput("PINK:SMA01:m10.VAL", 22500.) #X
caput("PINK:SMA01:m9.VAL", 2500.) #Y
scan.spot(detector.eiger(), exposure=5., images=60, sample='CuCl')

#CuCl long scan fro the energy calibration
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=21700, X1=24400, dX=800, Y0=2400, Y1=8150, passes=20, sample='CuCl', linedelay=0)
#Measurement
print("########## MEASUREMENT ##########")
#1
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=39000, X1=42000, dX=800, Y0=-6500, Y1=8130, passes=20, sample=sample_1, linedelay=0)
#3
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=3800, X1=6500, dX=800, Y0=-6500, Y1=8130, passes=20, sample=sample_3, linedelay=0)
#4
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=-13500, X1=-10500, dX=800, Y0=-6500, Y1=8130, passes=20 , sample=sample_4, linedelay=0)


#Damage scan
print("########## DAMAGE SCAN ##########")

caput("PINK:SMA01:m9.VAL", 3000.) #Y
caput("PINK:SMA01:m10.VAL", -12000.) #X
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
pink.gap(9.0)