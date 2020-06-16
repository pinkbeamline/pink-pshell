## eiger channel test

DEBUG = 1

print("Requesting Eiger parameters...")
Eiger_ROI_X = caget("PINK:EIGER:image3:ArraySize0_RBV")
Eiger_ROI_Y = caget("PINK:EIGER:image3:ArraySize1_RBV")

## create channels
print("Creating channels")
Eiger_acquire = create_channel_device("PINK:EIGER:cam1:Acquire", type='i')
Eiger_status = create_channel_device("PINK:EIGER:cam1:Acquire_RBV", type='i')
Eiger_status.setMonitored(True)
Eiger_frameID = create_channel_device("PINK:EIGER:cam1:ArrayCounter_RBV", type='d')
Eiger_frameID.setMonitored(True)
Eiger_roi_array = create_channel_device("PINK:EIGER:image3:ArrayData", type='[d', size=int(Eiger_ROI_X*Eiger_ROI_Y))
Eiger_roi_array.setMonitored(True)
Eiger_Spectra = create_channel_device("PINK:EIGER:spectrum_RBV", type='[d', size=Eiger_ROI_X)
Eiger_Spectra.setMonitored(True)
Eiger_Spectra_sum = create_channel_device("PINK:EIGER:specsum_RBV", type='[d', size=Eiger_ROI_X)
Eiger_trigger = create_channel_device("PINK:EIGER:cam1:Trigger", type='d')

print("Sleep 1 second...")
sleep(1)

print("Eiger running?")
## Stop eiger
if Eiger_status.read():
    Eiger_acquire.write(0)
    if DEBUG: print("Eiger Stop")
    while(Eiger_status.read()):
        sleep(1)
    if DEBUG: print("Eiger Idle")
print("Eiger is idle.")

## setup eiger
print("Setup eiger... ")
exposure = 1.1
Ypoints = 2
Xpoints = 3
passes = 1
for i in range(100):
    print("##########  {:d}/100  ##########".format(i+1))
    print("Exposure: {:.3f}".format(exposure))
    caput("PINK:EIGER:cam1:AcquireTime", exposure)
    sleep(1)
    caput("PINK:EIGER:cam1:AcquirePeriod", exposure+0.001)
    caput("PINK:EIGER:cam1:NumImages", Ypoints)
    caput("PINK:EIGER:cam1:NumTriggers", Xpoints*passes)
    # manual trigger enable
    caput("PINK:EIGER:cam1:ManualTrigger", 1)
    sleep(0.5)
    sleep(4)
## arm detector
Eiger_acquire.write(1)

initial_frame = Eiger_frameID.read()

for i in range(Xpoints*passes):
    for j in range(Ypoints):
        Eiger_trigger.write(1)
        Eiger_frameID.waitCacheChange(int((exposure*1000)+2000))

final_frame = Eiger_frameID.read()

print("Expected {:d} frames".format(int(Xpoints*passes*Ypoints)))
print("Received {:d} frames".format(int(final_frame-initial_frame)))

caput("PINK:EIGER:cam1:ManualTrigger", 0)

print("Sleep 1 second...")
sleep(1)

print("Removing Channels...")
del Eiger_acquire
del Eiger_status 
del Eiger_frameID
del Eiger_roi_array 
del Eiger_Spectra
del Eiger_Spectra_sum 
del Eiger_trigger

print("OK")