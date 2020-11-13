# dark current measurements for all diodes

# create channels

# diode 1
    qd1 = create_channel_device("PINK:CAE2:Current1:MeanValue_RBV", type='d')
    qd1.setMonitored(True)
    qd2 = create_channel_device("PINK:CAE2:Current2:MeanValue_RBV", type='d')
    qd2.setMonitored(True)
    qd3 = create_channel_device("PINK:CAE2:Current3:MeanValue_RBV", type='d')
    qd3.setMonitored(True)
    qd3 = create_channel_device("PINK:CAE2:Current4:MeanValue_RBV", type='d')
    qd3.setMonitored(True)

    direct = create_channel_device("PINK:CAE2:Current1:MeanValue_RBV", type='d')
    direct.setMonitored(True)
    tfy = create_channel_device("PINK:CAE2:Current2:MeanValue_RBV", type='d')
    tfy.setMonitored(True)


    N = 0
    qd1avg = []
    qd2avg = []
    qd3avg = []
    qd4avg = []
    diravg = []
    tfyavg = []


    
    