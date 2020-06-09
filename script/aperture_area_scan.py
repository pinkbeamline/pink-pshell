# Settings
aperture_gap_x = 0.2
c_start_x = -1.4
c_end_x = 0.6
c_step_x = 0.2

aperture_gap_y = 0.2
c_start_y = -0.7
c_end_y = 1.3
c_step_y = 0.2

exposure = 1.0

# center pos calc
cposx = linspace(c_start_x, c_end_x, c_step_x)
cposy = linspace(c_start_y, c_end_y, c_step_y)
print("Center positions x")
print(cposx)
print("\nCenter positions y")
print(cposy)
print("\n")

# create matrix
xsize = len(cposx)
ysize = len(cposy)

imap = [0]*ysize
for i in range(ysize):
    imap[i]=[0]*xsize

## setup caenels CAE2
log("Setup CAE2", data_file = False)
#0:continuous 1:multiple 2:single
caput("PINK:CAE2:AcquireMode", 2) ## single
caput("PINK:CAE2:AveragingTime", exposure)
caput("PINK:CAE2:ValuesPerRead", exposure*1000)
#0:free run 1:ext trigger
caput("PINK:CAE2:TriggerMode", 0) ## free run
caputq("PINK:CAE2:Acquire", 0)    

## channels
SENSOR = create_channel_device("PINK:CAE2:SumAll:MeanValue_RBV")
SENSOR.setMonitored(True)
ACQ = create_channel_device("PINK:CAE2:Acquire", type='i')
ACQ.setMonitored(True)

##set file name
set_exec_pars(open=False, name="au_area_scan", reset=True)

## save some pre data
save_dataset("position/centerx", cposx)
save_dataset("position/centery", cposy)
save_dataset("position/aperture_gap_x", aperture_gap_x)
save_dataset("position/aperture_gap_y", aperture_gap_y)

print("CenterX"+'\t'+"CenterY"+'\t'+"top"+'\t'+"bottom"+'\t'+"wall"+'\t'+"ring")
# main loop
for n in range(len(cposy)):
    posy = cposy[n]
    linetemp = [0]*xsize
    try:
        for m in range(len(cposx)):
            posx = cposx[m]
            #pvec = [posx, posy]
            #print(pvec)
            top=posy+(aperture_gap_y/2)
            bottom=posy-(aperture_gap_y/2)
            wall=posx+(aperture_gap_x/2)
            ring=posx-(aperture_gap_x/2)
            print('{:.3f}'.format(posx)+'\t'+'{:.3f}'.format(posy)+'\t'+'{:.3f}'.format(top)+'\t'+'{:.3f}'.format(bottom)+'\t'+'{:.3f}'.format(wall)+'\t'+'{:.3f}'.format(ring)+'\t')
            pink.AU1(top=top, bottom=bottom, wall=wall, ring=ring)
            #ACQ.write(1)
            #resp = SENSOR.waitCacheChange(1000*int(exposure+2))
            linetemp[m]=SENSOR.read()
            imap[n]=linetemp
            plot(imap)      
    except:
        print("abort")
        imap[n]=linetemp

# save matrix data
save_dataset("data/intesity_map", imap)

print("Done")