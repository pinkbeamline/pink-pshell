#pink.ge_SEC_EL_continous_exposure_speed(2, 37600, 1100, 3, -3000, 0, 500, passes=2, sample='test1')
#pink.ge_SEC_EL_continous_exposure_speed(2, 37600, 1100, 3, 1000, 4000, 500, passes=2, sample='test1')

#scan.spot(detector.eiger(), exposure=1, images=3, sample='eiger spot t1')
#scan.spot(detector.eiger(), exposure=1.3, images=4, sample='eiger spot t2')

#scan.spot(detector.eiger(), exposure=2, images=4, sample='test 1')
#sleep(5)
#scan.spot(detector.eiger(), exposure=2, images=4, sample='test 2')

cryo.holder_number(2)
scan.zigzag_relative(detector.eiger(), exposure=1, X0=-500, dX=1000, Xpoints=2, Y0=-500, dY=1000, Ypoints=2, passes=1, sample='test1a', linedelay=0)
cryo.holder_number(3)
scan.zigzag_relative(detector.eiger(), exposure=1, X0=-500, dX=1000, Xpoints=2, Y0=-500, dY=1000, Ypoints=2, passes=1, sample='test1b', linedelay=0)

