#pink.ge_SEC_EL_continous_exposure_speed(2, 37600, 1100, 3, -3000, 0, 500, passes=2, sample='test1')
#pink.ge_SEC_EL_continous_exposure_speed(2, 37600, 1100, 3, 1000, 4000, 500, passes=2, sample='test1')

#scan.spot(detector.eiger(), exposure=1, images=3, sample='eiger spot t1')
#scan.spot(detector.eiger(), exposure=1.3, images=4, sample='eiger spot t2')

#scan.spot(detector.eiger(), exposure=2, images=4, sample='test 1')
#sleep(5)
#scan.spot(detector.eiger(), exposure=2, images=4, sample='test 2')

samples=[3]
for i in samples:
    cryo.sample_number(i)
    scan.zigzag_relative(detector.eiger(), exposure=1, X0=-1600, dX=800, Xpoints=5, Y0=-6200, dY=1000, Ypoints=4, passes=1, sample='tests', linedelay=0)

