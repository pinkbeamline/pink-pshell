print("########## DAMAGE SCAN ##########")

sample_1='s10 CoO SF'
sample_2='s11 Co3O4 SF'
sample_3='s12 CoF3'
scan.spot(detector.eiger(), exposure=1., images=2, sample=sample_1)
caput("PINK:SMA01:m10.VAL", 21000.) #X
scan.spot(detector.eiger(), exposure=1., images=2, sample=sample_2)
caput("PINK:SMA01:m10.VAL", 21500.) #X
scan.spot(detector.eiger(), exposure=1., images=2, sample=sample_3)

print("########## DONE ##########")