#Spot scans
#SEC_el_y.move(-7400.0)
#SEC_el_x.move(38500.0)
#scan.ge_SEC_EL_spot(1, 20, sample='Ti acetylacetate dicloride')
#SEC_el_x.move(20000.0)
#scan.ge_SEC_EL_spot(1, 20, sample='TTitanocene dichloride')
#SEC_el_x.move(4000.0)
#scan.ge_SEC_EL_spot(1, 20, sample='Ti cyclopentadienyl trichloride')
#SEC_el_y.move(100.0)
#SEC_el_x.move(-13000.0)
#scan.ge_SEC_EL_spot(0.5, 20, sample='V powder Ka1,2')
#Measurement
#scan.ge_SEC_EL_continuous_exposure_speed(8, 2900, 720, 4, -7000, 8000, 500, passes=40, sample='Titanyl acetylacetate')
scan.ge_SEC_EL_continuous_exposure_speed(8, 20000, 700, 4, -7000, 8000, 500, passes=40, sample='Titanocene dichloride')
scan.ge_SEC_EL_continuous_exposure_speed(7, 37900, 720, 4, -7000, 1500, 500, passes=40, sample='Ti acetylacetate dicloride')


pink.shutter_hard_CLOSE()
caput("PINK:PLCVAC:V11close", 1)
caput("PINK:PLCVAC:V10close", 1)
caput("PINK:GEYES:cam1:Temperature", 20)