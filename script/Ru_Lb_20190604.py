pink.ge_SEC_EL_continous_exposure_speed(10, -15000, 750, 4, -8000, 8000, 200, passes=40, sample='Ru_CT 2,2')
pink.ge_SEC_EL_continous_exposure_speed(10, 19200, 750, 4, -8000, 8000, 200, passes=40, sample='Ru(bpy)(FP6)2')
pink.ge_SEC_EL_continous_exposure_speed(10, 37600, 750, 4, -8000, 8000, 200, passes=40, sample='Ru(dmso)4Cl2')
pink.shutter_hard_CLOSE()
caput("PINK:PLCVAC:V11close", 1)
caput("PINK:PLCVAC:V10close", 1)
#caput("PINK:GEYES:cam1:Temperature", 20)1)