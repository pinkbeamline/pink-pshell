#overnight PShell test

myloop=0
haserror=False

while(haserror==False):
    try:
        msg=time.asctime()+" - Loop: " + '{:d}'.format(myloop+1)
        caput("PINK:GSM:smsmsg", msg)
        caput("PINK:GSM:sendsms.PROC", 1)
        
        mysample = "overnight test (line_vert) - Loop: " + '{:d}'.format(myloop+1)
        #31 sec/pass = 26 min
        pink.ge_SEC_EL_line_vert(1, 0, 10, 10, passes=50, sample=mysample)
        
        mysample = "overnight test (zigzag) - Loop: " + '{:d}'.format(myloop+1)
        #56 sec/pass = 47 min
        pink.ge_SEC_EL_zigzag(1, 0, 10, 4, 0, 10, 5, passes=50, sample=mysample)
        
        mysample = "overnight test (exposure_points) - Loop: " + '{:d}'.format(myloop+1)
        #105 sec/pass = 70 min
        pink.ge_SEC_EL_continous_exposure_points(1, 0, 10, 4, 0, 100, 10, passes=40, sample=mysample)
        
        mysample = "overnight test (exposure_speed) - Loop: " + '{:d}'.format(myloop+1)
        #120 sec/pass = 60 min
        pink.ge_SEC_EL_continous_exposure_speed(1, 0, 10, 4, 0, 100, 4, passes=30, sample=mysample)
        
        mysample = "overnight test (points_speed) - Loop: " + '{:d}'.format(myloop+1)
        #50 sec/pass = 42 min
        pink.ge_SEC_EL_continous_points_speed(0, 10, 4, 0, 100, 5, 10, passes=50, sample=mysample)

        myloop=myloop+1
    except:
        haserror=True
        msg=time.asctime()+" ERROR - Loop: " + '{:d}'.format(myloop+1)
        caput("PINK:GSM:smsmsg", msg)
        caput("PINK:GSM:sendsms.PROC", 1)

