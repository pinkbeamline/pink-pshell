sample_1='s1.1 FM4'
sample_2='s1.2 CuCl'
sample_3='s1.3 BG1'
#sample_4='s1.4 FM3'

print("########## ENERGYCALIBRATION ##########")
caput("PINK:SMA01:m10.VAL", 22500.) #X
caput("PINK:SMA01:m9.VAL", -4600.) #Y
#Cu foil Kb1,3
scan.spot(detector.eiger(), exposure=5., images=60, sample='Cu foil')
#Zn foil Ka1,2
caput("PINK:SMA01:m9.VAL", -1900.) #Y
scan.spot(detector.eiger(), exposure=10., images=50, sample='Zn foil')
#Ho La1,2
caput("PINK:SMA01:m9.VAL", 700.) #Y
scan.spot(detector.eiger(), exposure=10., images=15, sample='Ho foil')
#CuCl Kb1,3
caput("PINK:SMA01:m9.VAL", 1800.) #Y
scan.spot(detector.eiger(), exposure=10., images=100, sample='CuCl')




#Measurement
print("########## MEASUREMENT ##########")
#1
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=39400, X1=42000, dX=780, Y0=-7000, Y1=8100, passes=15, sample=sample_1, linedelay=0)
#3
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=4300, X1=7000, dX=780, Y0=-7000, Y1=8100, passes=15, sample=sample_3, linedelay=0)
#4
#scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=-13200, X1=-10500, dX=780, Y0=-7000, Y1=8100, passes=12, sample=sample_4, linedelay=0)

#Damage scan
print("########## DAMAGE SCAN ##########")

caput("PINK:SMA01:m9.VAL", 0.) #Y
caput("PINK:SMA01:m10.VAL", -12000.) #X
scan.spot(detector.eiger(), exposure=10., images=80, sample=sample_4)
caput("PINK:SMA01:m10.VAL", 5500.) #X
scan.spot(detector.eiger(), exposure=10., images=80, sample=sample_3)
caput("PINK:SMA01:m10.VAL", 40000.) #X
scan.spot(detector.eiger(), exposure=10., images=80, sample=sample_1)

#CuCl long scan
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=21700, X1=24400, dX=780, Y0=2000, Y1=8100, passes=60, sample='CuCl', linedelay=0)

caput("PINK:SMA01:m10.VAL", 0.) #X
caput("PINK:SMA01:m9.VAL", 0.) #Y

print("########## DONE ##########")
pink.shutter_hard_CLOSE()
caput("PINK:PLCVAC:V11close", 1)
caput("PINK:PLCVAC:V12close", 1)
caput("PINK:PLCVAC:V16close", 1)
pink.gap(8.0)