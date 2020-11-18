cryo_y_DMOV = create_channel_device("PINK:ANC01:ACT0:IN_TARGET", type='d')
cryo_y_DMOV.setMonitored(True)
cryo_y_SPEED = create_channel_device("PINK:ANC01:ACT0:speedavg", type='d')
cryo_y_SPEED.setMonitored(True)

def motionsuccessbyspeed(dmov, speed):
    status = False
    notdone = True
    speedfail=0
    while(notdone):
        if(dmov.read()>0):
            status=True
            notdone=False
        if(abs(speed.read())<100.0):
            speedfail += 1
            print("Motor speed too low... {}".format(speedfail))
        else:
            speedfail = 0
        if(speedfail>=5):
            notdone=False
        sleep(1)       
    return status

caput("PINK:CRYO:sampley", -8000)
print("waiting...")
sleep(1)
motionsuccess = motionsuccessbyspeed(cryo_y_DMOV, cryo_y_SPEED)

print("Motion success: " + str(motionsuccess))


del cryo_y_DMOV
del cryo_y_SPEED