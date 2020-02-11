scan2.eiger_SEC_EL_continuous_exposure_speed(20, 37400, 700, 4, -7100, 8150, 12, passes=1, sample='Co(OH)2', linedelay=0)
scan2.eiger_SEC_EL_continuous_exposure_speed(20, 19900, 700, 4, -7100, 8150, 12.0, passes=1, sample='Boron CoOH2', linedelay=0)
scan2.eiger_SEC_EL_continuous_exposure_speed(20, -20000, 700, 6, -5000, 5000, 12.0, passes=1, sample='Co(OH)2:BN=2:1', linedelay=0)
pink.shutter_hard_CLOSE()
caput("PINK:PLCVAC:V11close", 1)
pink.gap_set(12.0)

caput("HEX2OS12L:hexapod:setPoseY", -4000.0)