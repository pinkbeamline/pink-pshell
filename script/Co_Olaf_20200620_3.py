print("########## ENERGYCALIBRATION ##########")
caput("PINK:SMA01:m10.VAL", 21000.) #X
caput("PINK:SMA01:m9.VAL", -5000.) #Y

#Ni Ka1,2
scan.spot(detector.eiger(), exposure=5., images=40, sample='Ni foil')
#Co foil, Kb1,3 and V2C
caput("PINK:SMA01:m10.VAL", 21000.) #X
caput("PINK:SMA01:m9.VAL", -3500.) #Y
scan.spot(detector.eiger(), exposure=2., images=200, sample='Co foil')
#Co(OH)2 commercial, Kb1,3 and V2C
scan.continuous(detector.eiger(), det_exposure=2, sample_exposure=0.5, X0=19300, X1=20200, dX=700, Y0=0, Y1=4000, passes=20, sample='Co(OH)2', linedelay=0)

#Measurement
print("########## MEASUREMENT ##########")
#1
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=37300, X1=40000, dX=750, Y0=-7500, Y1=8100, passes=6, sample='s07 SBA32', linedelay=0)
#2
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=2500, X1=4800, dX=750, Y0=-7500, Y1=8100, passes=6, sample='s08 CoFe2O4 (KIT-6 Fe)', linedelay=0)
#3
scan.continuous(detector.eiger(), det_exposure=5, sample_exposure=0.5, X0=-15100, X1=-12400, dX=750, Y0=-7500, Y1=8100, passes=6, sample='s09 CoFe2O4 (TRR247)', linedelay=0)

#Damage scan
print("########## DAMAGE SCAN ##########")

caput("PINK:SMA01:m9.VAL", 0.) #Y
caput("PINK:SMA01:m10.VAL", -13500.) #X
scan.spot(detector.eiger(), exposure=2., images=60, sample='s09 CoFe2O4 (TRR247)')
caput("PINK:SMA01:m10.VAL", 3500.) #X
scan.spot(detector.eiger(), exposure=2., images=60, sample='s08 CoFe2O4 (KIT-6 Fe)')
caput("PINK:SMA01:m10.VAL", 38500.) #X
scan.spot(detector.eiger(), exposure=2., images=60, sample='s07 SBA32')
caput("PINK:SMA01:m10.VAL", 0.) #X
print("########## DONE ##########")
pink.shutter_hard_CLOSE()
caput("PINK:PLCVAC:V11close", 1)
caput("PINK:PLCVAC:V10close", 1)
pink.gap(12.0)