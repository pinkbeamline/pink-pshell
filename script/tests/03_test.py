#03_test
elab.put(time.asctime())
sim.spot(detector, exposure=1.1, images=10, sample='S01')
sleep(1)
sim.spot(detector.eiger(), exposure=2.2, images=20, sample='S02')
