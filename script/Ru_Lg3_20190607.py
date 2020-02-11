#Energy calibration
SEC_el_x.move(3000.0)
SEC_el_y.move(0.0)
pink.ge_SEC_EL_spot(2, 20, sample='Pd Lb2')
#Measurement
pink.ge_SEC_EL_continous_exposure_speed(15, -15800, 780, 5, -8000, 8000, 200, passes=20, sample='Ru(dmap)6Cl2')
pink.ge_SEC_EL_continous_exposure_speed(15, 19300, 780, 5, -8000, 8000, 200, passes=20, sample='Ru(bpy)3(PF6)2')
pink.ge_SEC_EL_continous_exposure_speed(15, 37000, 780, 5, -8000, 8000, 200, passes=20, sample='Ru(CN)6K4')
pink.ge_SEC_EL_continous_exposure_speed(15, -15800, 780, 5, -8000, 8000, 200, passes=20, sample='Ru(dmap)6Cl2')
pink.ge_SEC_EL_continous_exposure_speed(15, 19300, 780, 5, -8000, 8000, 200, passes=20, sample='Ru(bpy)3(PF6)2')
pink.ge_SEC_EL_continous_exposure_speed(15, 37000, 780, 5, -8000, 8000, 200, passes=20, sample='Ru(CN)6K4')
#Energy calibration
SEC_el_x.move(3000.0)
SEC_el_y.move(0.0)
pink.ge_SEC_EL_spot(2, 20, sample='Pd Lb2')
#Energy calibration
SEC_el_x.move(3500.0)
SEC_el_y.move(-1000.0)
pink.ge_SEC_EL_spot(2, 20, sample='Pd Lb2')
pink.shutter_hard_CLOSE()
caput("PINK:PLCVAC:V11close", 1)
caput("PINK:PLCVAC:V10close", 1)
caput("PINK:GEYES:cam1:Temperature", 20)