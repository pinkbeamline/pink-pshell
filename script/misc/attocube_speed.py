#test

#PINK:ANC01:ACT0:CMD:TARGET
#PINK:ANC01:ACT0:POSITION
#PINK:ANC01:ACT0:CMD:FREQ

MOTOR = create_channel_device("PINK:ANC01:ACT0:CMD:TARGET", type='d')
MOTOR_SPD = create_channel_device("PINK:ANC01:ACT0:CMD:FREQ", type='d')
MOTOR_RBV = create_channel_device("PINK:ANC01:ACT0:POSITION", type='d')
MOTOR_RBV.setMonitored(True)
MOTOR_DMOV = create_channel_device("PINK:ANC01:ACT0:IN_TARGET", type='d')
MOTOR_DMOV.setMonitored(True)

## setup filename
set_exec_pars(open=False, name="atto-test", reset=True)

#freqlist = [50]

#grab data 50 up
pos1 = 12000.0
pos2 = 10000.0
mspeed = 50
##
sensor = []
tnanos = []
print("50 up - Moving to initial position...")
MOTOR_SPD.write(500)
MOTOR.write(pos1)
sleep(1)
MOTOR_DMOV.waitValueInRange(1, 0.5, 60000)
print("moving...")
MOTOR_SPD.write(mspeed)
MOTOR.write(pos2)
while(abs(MOTOR_RBV.take()-pos2)>5.0):
    MOTOR_RBV.waitCacheChange(1000)
    sensor.append(MOTOR_RBV.take())
    tnanos.append(MOTOR_RBV.getTimestampNanos())
print("done")
save_dataset("motor/pos_50_up", sensor)
save_dataset("motor/pos_50_up_ts", tnanos)

#grab data 50 down
pos1 = 10000.0
pos2 = 12000.0
mspeed = 50
##
sensor = []
tnanos = []
print("50 down - Moving to initial position...")
MOTOR_SPD.write(500)
MOTOR.write(pos1)
sleep(1)
MOTOR_DMOV.waitValueInRange(1, 0.5, 60000)
print("moving...")
MOTOR_SPD.write(mspeed)
MOTOR.write(pos2)
while(abs(MOTOR_RBV.take()-pos2)>5.0):
    MOTOR_RBV.waitCacheChange(1000)
    sensor.append(MOTOR_RBV.take())
    tnanos.append(MOTOR_RBV.getTimestampNanos())
print("done")
save_dataset("motor/pos_50_down", sensor)
save_dataset("motor/pos_50_down_ts", tnanos)

#grab data 100 up
pos1 = 12000.0
pos2 = 10000.0
mspeed = 100
##
sensor = []
tnanos = []
print("100 up - Moving to initial position...")
MOTOR_SPD.write(500)
MOTOR.write(pos1)
sleep(1)
MOTOR_DMOV.waitValueInRange(1, 0.5, 60000)
print("moving...")
MOTOR_SPD.write(mspeed)
MOTOR.write(pos2)
while(abs(MOTOR_RBV.take()-pos2)>5.0):
    MOTOR_RBV.waitCacheChange(1000)
    sensor.append(MOTOR_RBV.take())
    tnanos.append(MOTOR_RBV.getTimestampNanos())
print("done")
save_dataset("motor/pos_100_up", sensor)
save_dataset("motor/pos_100_up_ts", tnanos)

#grab data 100 down
pos1 = 10000.0
pos2 = 12000.0
mspeed = 100
##
sensor = []
tnanos = []
print("100 down - Moving to initial position...")
MOTOR_SPD.write(500)
MOTOR.write(pos1)
sleep(1)
MOTOR_DMOV.waitValueInRange(1, 0.5, 60000)
print("moving...")
MOTOR_SPD.write(mspeed)
MOTOR.write(pos2)
while(abs(MOTOR_RBV.take()-pos2)>5.0):
    MOTOR_RBV.waitCacheChange(1000)
    sensor.append(MOTOR_RBV.take())
    tnanos.append(MOTOR_RBV.getTimestampNanos())
print("done")
save_dataset("motor/pos_100_down", sensor)
save_dataset("motor/pos_100_down_ts", tnanos)

#grab data 200 up
pos1 = 12000.0
pos2 = 8000.0
mspeed = 200
##
sensor = []
tnanos = []
print("200 up - Moving to initial position...")
MOTOR_SPD.write(500)
MOTOR.write(pos1)
sleep(1)
MOTOR_DMOV.waitValueInRange(1, 0.5, 60000)
print("moving...")
MOTOR_SPD.write(mspeed)
MOTOR.write(pos2)
while(abs(MOTOR_RBV.take()-pos2)>5.0):
    MOTOR_RBV.waitCacheChange(1000)
    sensor.append(MOTOR_RBV.take())
    tnanos.append(MOTOR_RBV.getTimestampNanos())
print("done")
save_dataset("motor/pos_200_up", sensor)
save_dataset("motor/pos_200_up_ts", tnanos)

#grab data 200 down
pos1 = 8000.0
pos2 = 12000.0
mspeed = 200
##
sensor = []
tnanos = []
print("200 down - Moving to initial position...")
MOTOR_SPD.write(500)
MOTOR.write(pos1)
sleep(1)
MOTOR_DMOV.waitValueInRange(1, 0.5, 60000)
print("moving...")
MOTOR_SPD.write(mspeed)
MOTOR.write(pos2)
while(abs(MOTOR_RBV.take()-pos2)>5.0):
    MOTOR_RBV.waitCacheChange(1000)
    sensor.append(MOTOR_RBV.take())
    tnanos.append(MOTOR_RBV.getTimestampNanos())
print("done")
save_dataset("motor/pos_200_down", sensor)
save_dataset("motor/pos_200_down_ts", tnanos)

#grab data 500 up
pos1 = 12000.0
pos2 = 8000.0
mspeed = 500
##
sensor = []
tnanos = []
print("500 up - Moving to initial position...")
MOTOR_SPD.write(500)
MOTOR.write(pos1)
sleep(1)
MOTOR_DMOV.waitValueInRange(1, 0.5, 60000)
print("moving...")
MOTOR_SPD.write(mspeed)
MOTOR.write(pos2)
while(abs(MOTOR_RBV.take()-pos2)>5.0):
    MOTOR_RBV.waitCacheChange(1000)
    sensor.append(MOTOR_RBV.take())
    tnanos.append(MOTOR_RBV.getTimestampNanos())
print("done")
save_dataset("motor/pos_500_up", sensor)
save_dataset("motor/pos_500_up_ts", tnanos)

#grab data 500 down
pos1 = 8000.0
pos2 = 12000.0
mspeed = 500
##
sensor = []
tnanos = []
print("500 down - Moving to initial position...")
MOTOR_SPD.write(500)
MOTOR.write(pos1)
sleep(1)
MOTOR_DMOV.waitValueInRange(1, 0.5, 60000)
print("moving...")
MOTOR_SPD.write(mspeed)
MOTOR.write(pos2)
while(abs(MOTOR_RBV.take()-pos2)>5.0):
    MOTOR_RBV.waitCacheChange(1000)
    sensor.append(MOTOR_RBV.take())
    tnanos.append(MOTOR_RBV.getTimestampNanos())
print("done")
save_dataset("motor/pos_500_down", sensor)
save_dataset("motor/pos_500_down_ts", tnanos)

MOTOR.close()
MOTOR_SPD.close()
MOTOR_RBV.close()
MOTOR_DMOV.close()

del MOTOR
del MOTOR_SPD
del MOTOR_RBV
del MOTOR_DMOV