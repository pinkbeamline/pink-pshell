sample_1='s1.1 PB1'
sample_2='s1.2 CuCl'
sample_3='s1.3 PB2'
sample_4='s1.4 PB3'

print("########## ENERGYCALIBRATION ##########")
caput("PINK:SMA01:m10.VAL", 23500.) #X
caput("PINK:SMA01:m9.VAL", -4600.) #Y
#Cu foil Kb1,3
scan.spot(detector.eiger(), exposure=5., images=60, sample='Cu foil')
#Zn foil Ka1,2
caput("PINK:SMA01:m9.VAL", -1580.) #Y
scan.spot(detector.eiger(), exposure=10., images=50, sample='Zn foil')
#Ho La1,2
caput("PINK:SMA01:m9.VAL", 1280.) #Y
scan.spot(detector.eiger(), exposure=10., images=15, sample='Ho foil')
#CuCl Kb1,3
caput("PINK:SMA01:m10.VAL", 22600.) #X
caput("PINK:SMA01:m9.VAL", 2350.) #Y
scan.spot(detector.eiger(), exposure=10., images=100, sample='CuCl')


#Measurement
print("########## MEASUREMENT ##########")
#1
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=39480, X1=42000, dX=780, Y0=-6000, Y1=8130, passes=20, sample=sample_1, linedelay=0)
#3
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=4700, X1=7200, dX=780, Y0=-6000, Y1=8130, passes=20, sample=sample_3, linedelay=0)
#4
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=-13060, X1=-10300, dX=780, Y0=-6000, Y1=8130, passes=20 , sample=sample_4, linedelay=0)

#CuCl long scan fro the energy calibration
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=22080, X1=24700, dX=780, Y0=2500, Y1=8150, passes=30, sample='CuCl', linedelay=0)
#Damage scan
print("########## DAMAGE SCAN ##########")

caput("PINK:SMA01:m9.VAL", 3000.) #Y
caput("PINK:SMA01:m10.VAL", -12000.) #X
scan.spot(detector.eiger(), exposure=10., images=360, sample=sample_4)
caput("PINK:SMA01:m10.VAL", 5500.) #X
scan.spot(detector.eiger(), exposure=10., images=360, sample=sample_3)
caput("PINK:SMA01:m10.VAL", 40000.) #X
scan.spot(detector.eiger(), exposure=10., images=360, sample=sample_1)



print("########## DONE ##########")
pink.shutter_hard_CLOSE()
caput("PINK:PLCVAC:V11close", 1)
caput("PINK:PLCVAC:V12close", 1)
#caput("PINK:PLCVAC:V16close", 1)
caput("PINK:SMA01:m10.VAL", 0.) #X
caput("PINK:SMA01:m9.VAL", 0.) #Y
pink.gap(9.0)