pink.ge_SEC_EL_continous_exposure_speed(10, 2400, 800, 4, -8000, 8100, 200, passes=40, sample='Ru(NH3)Cl3')
pink.ge_SEC_EL_continous_exposure_speed(10, -15000, 800, 4, -8000, 8100, 200, passes=40, sample='Ru(CN6)K4')
pink.shutter_hard_CLOSE()
caput("PINK:PLCVAC:V11close", 1)
caput("PINK:PLCVAC:V10close", 1)
caput("PINK:GEYES:cam1:Temperature", 20)