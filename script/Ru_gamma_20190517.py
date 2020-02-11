pink.ge_SEC_EL_continous_points_speed(2510,800, 4, -8000, 8100, 1, 500, passes=5, sample='Ru(NH3)Cl3')
pink.ge_SEC_EL_continous_points_speed(37400, 750, 4, -8000, 8100, 1, 500, passes=10, sample='RuO2')
#pink.ge_SEC_EL_continous_points_speed(-14900, 800, 4, -8000, 8100, 1, 500, passes=5, sample='Ru(NH3)Cl3')
pink.shutter_hard_CLOSE()
caput("PINK:PLCVAC:V11close", 1)
caput("PINK:PLCVAC:V10close", 1)
#caput("PINK:GEYES:cam1:Temperature", 20)


