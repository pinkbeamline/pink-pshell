#Energy calibration
#SEC_el_x.move(3000.0)
#SEC_el_y.move(3000.0)
#scan.mythen_SEC_EL_spot(1, 30, sample='Ni Ka1,2')
#Measurement

scan.mythen_SEC_EL_continuous_exposure_speed(20, 37400, 700, 4, -7100, 8150, 15, passes=1, sample='Co(OH)2', linedelay=0)
scan.mythen_SEC_EL_continuous_exposure_speed(20, 19900, 700, 4, -7100, 8150, 15.0, passes=1, sample='Boron CoOH2', linedelay=0)
scan.mythen_SEC_EL_continuous_exposure_speed(20, -20000, 700, 6, -5000, 5000, 15.0, passes=1, sample='Co(OH)2:BN=2:1', linedelay=0)
#pink.shutter_hard_CLOSE()
#caput("PINK:PLCVAC:V11close", 1)
#caput("PINK:PLCVAC:V10close", 1)
#pink.gap_set(12.0)