#gap_scans.py

class GAPSCAN():
    def __init__(self):
        pass

########################################
### scan
########################################

    def scan(self, source, start=0, end=0, step=0, exposure=0.0, fit=False):
        #print(source)
        if exposure==0:
            print("abort: exposure = 0")
            return

        set_exec_pars(open=False, name="gap", reset=True)

        verbose=True
        DEBUG=False

        if verbose: print("Creating channels")
        ## channels
        if source=="izero":
            SENSOR = create_channel_device("PINK:CAE2:SumAll:MeanValue_RBV")
            SENSOR.setMonitored(True)
            ACQ = create_channel_device("PINK:CAE2:Acquire", type='i')
            ACQ.setMonitored(True)
        elif source=="sec":
            SENSOR = create_channel_device("PINK:CAE1:Current3:MeanValue_RBV")
            SENSOR.setMonitored(True)
            ACQ = create_channel_device("PINK:CAE1:Acquire", type='i')
            ACQ.setMonitored(True)
        else:
            print("gap scan is not available for this source.")
            return

        MOTOR = create_channel_device("U17IT6R:BaseParGapsel.B")
        MOTOR_SET = create_channel_device("U17IT6R:BaseCmdCalc.PROC")
        MOTOR_RBV = create_channel_device("U17IT6R:BasePmGap.A")
        MOTOR_RBV.setMonitored(True)
        motor_deadband = 0.02

        ## simulated channels
        #SENSOR = create_channel_device("PINK:GAPSIM:izero")
        #SENSOR.setMonitored(True)
        #MOTOR = create_channel_device("PINK:GAPSIM:gapset")
        #MOTOR_SET = create_channel_device("PINK:GAPSIM:gapexec.PROC")
        #MOTOR_RBV = create_channel_device("PINK:GAPSIM:m1.RBV")
        #MOTOR_RBV.setMonitored(True)
        #motor_deadband = 0.1

        ## variables
        sensor = []
        motor = []

        ## Setup
        #print("Scanning ...")
        set_exec_pars(open=False, name="gap", reset=True)
        save_dataset("scan/scantype", "Gap scan")

        if verbose: print("Setup ampmeter")
        ## Configure ampmeter
        exposure=float(exposure)
        ACQ.write(0)
        sleep(1)
        if source=="izero":
            caput("PINK:CAE2:ValuesPerRead", int(1000*exposure))
            caput("PINK:CAE2:AveragingTime", exposure)
            caput("PINK:CAE2:TriggerMode", 0)
            caput("PINK:CAE2:AcquireMode", 2)
        else:
            caput("PINK:CAE1:ValuesPerRead", int(1000*exposure))
            caput("PINK:CAE1:AveragingTime", exposure)
            caput("PINK:CAE1:TriggerMode", 0)
            caput("PINK:CAE1:AcquireMode", 2)
            caput("PINK:CAE1:Range", 0)
        sleep(1)

        ## configure scan positions
        positionarray = linspace(start, end, step)

        ## plot setup
        if verbose: print("Setup plot")
        [p1] = plot(None, "Scan", title="Gap Scan")
        p1.getAxis(p1.AxisId.X).setRange(min(start, end),max(start,end))
        p1.addSeries(LinePlotSeries("Fit"))

        if verbose: print("Moving gap to start position")
        pos = positionarray[0]
        MOTOR.write(pos)
        MOTOR_SET.write(1)
        while(abs(pos-MOTOR_RBV.read()) > motor_deadband):
            mystat = "Gap: " + str(MOTOR_RBV.take())
            set_status(mystat)
            sleep(0.5)
        #MOTOR_RBV.waitValueInRange(positionarray[0], motor_deadband, 60000)
        mystat = "Gap: " + str(MOTOR_RBV.take())
        set_status(mystat)

        if verbose: print("Scanning...")
        try:
            ## Main loop
            for pos in positionarray:
                moveattempt = 0
                posok = False
                while(moveattempt < 3 and posok==False):
                    if DEBUG: print("Pos: " + str(pos))
                    MOTOR.write(pos)
                    sleep(0.2)
                    MOTOR_SET.write(1)

                    gaperr = abs(pos - MOTOR_RBV.read())
                    if DEBUG: print("Gap dx: " + str(gaperr))
                    time_init = time.clock()

                    ## wait for gap to reach position
                    pos_skip = False
                    waitpos = True
                    while(gaperr>=motor_deadband and pos_skip==False and waitpos==True):
                        gaperr = abs(pos - MOTOR_RBV.read())
                        time_elapse = time.clock()-time_init
                        if time_elapse>3.0:
                            moveattempt = moveattempt + 1
                            logmsg="Gap have not reached position in 3 seconds. Position: " + str(pos) + " ,Attempt: " + str(moveattempt)
                            print(logmsg)
                            log(logmsg, data_file = True)
                            waitpos=False
                        sleep(0.25)

                    if moveattempt >= 3:
                        logmsg = "Warning: Failed to reach gap position after 3 attempts. Skipping position"
                        print(logmsg)
                        log(logmsg, data_file = True)
                        pos_skip = True

                    if gaperr<=motor_deadband:
                        posok=True


                # junk = MOTOR_RBV.read()
                # try:
                #     MOTOR_RBV.waitValueInRange(pos, motor_deadband, 5000)
                # except:
                #     continue


                if(pos_skip==False):
                    trycount = 0
                    waitsensor = True
                    # try 3 times to read ampmeter
                    while(waitsensor):

                        while(ACQ.take()==1):
                            ACQ.write(0)
                            sleep(1)

                        ACQ.write(1)
                        resp = SENSOR.waitCacheChange(int(1000*(exposure+2)))

                        if resp==False:
                            if trycount < 3:
                                trycount = trycount + 1
                                logmsg = "Warning: No data from ampmeter. Attempt " + '{:d}'.format(int(trycount)) + " of 3."
                                print(logmsg)
                                log(logmsg, data_file = True)
                            else:
                                pos_skip=True
                                waitsensor = False
                                logmsg = "Failed to read ampmeter after 3 attempts. Skipping position"
                                print(logmsg)
                                log(logmsg, data_file = True)
                        else:
                            waitsensor=False

                if(pos_skip==False):
                    sensor.append(SENSOR.take())
                    motor.append(MOTOR_RBV.take())
                    p1.getSeries(0).setData(motor, sensor)
        except:
            print("Gap scan aborted.")

        if fit == True:
            fittype = "exp"
        else:
            fittype = None

        ## Fitting options
        if fittype=="linear":
            if verbose: print("analysing")
            (a, b, amp, com, sigma, gauss, fwhm, xgauss)=self.__gauss_fit(sensor, motor)
            p1.getSeries(1).setData(xgauss, gauss)
            p1.setLegendVisible(True)
            print(" ")
            print("Gaussian fit -- linear background")
            print("-----------------------------------------")
            print("inclination: " + '{:.3e}'.format(a))
            print("     offset: " + '{:.3e}'.format(b))
            print("  Amplitude: " + '{:.3e}'.format(amp))
            print("       Mean: " + '{:.3f}'.format(com))
            print("      Sigma: " + '{:.3f}'.format(sigma))
            print("       FWHM: " + '{:.3f}'.format(fwhm))
            print("-----------------------------------------")

            if verbose: print("Saving data")
            #save_dataset("scan/scantype", "Gap scan with linear bg gaussian fitting")
            save_dataset("gaussian/inclination", a)
            save_dataset("gaussian/offset", b)
            save_dataset("gaussian/amplitude", amp)
            save_dataset("gaussian/mean", com)
            save_dataset("gaussian/sigma", sigma)
            save_dataset("gaussian/fwhm", fwhm)
            save_dataset("plot/x", xgauss)
            save_dataset("plot/y", gauss)
            save_dataset("raw/izero", sensor)
            save_dataset("raw/gap", motor)

        elif fittype == "exp":
            if verbose: print("analysing")
            (eamp, decay, amp, com, sigma, gauss, fwhm, xgauss)=self.__gauss_exp_fit(sensor,motor)
            p1.getSeries(1).setData(xgauss, gauss)
            p1.setLegendVisible(True)
            print(" ")
            print("Gaussian fit -- exponetial background")
            print("-----------------------------------------")
            print("Exp. amplitude: " + '{:.3e}'.format(eamp))
            print("Exp.     decay: " + '{:.3e}'.format(decay))
            print("     Amplitude: " + '{:.3e}'.format(amp))
            print("          Mean: " + '{:.3f}'.format(com))
            print("         Sigma: " + '{:.3f}'.format(sigma))
            print("          FWHM: " + '{:.3f}'.format(fwhm))
            print("-----------------------------------------")

            if verbose: print("Saving data")
            save_dataset("scan/scantype", "Gap scan with exponential bg gaussian fitting")
            save_dataset("gaussian/exp_amplitude", eamp)
            save_dataset("gaussian/exp_decay", decay)
            save_dataset("gaussian/amplitude", amp)
            save_dataset("gaussian/mean", com)
            save_dataset("gaussian/sigma", sigma)
            save_dataset("gaussian/fwhm", fwhm)
            save_dataset("plot/x", xgauss)
            save_dataset("plot/y", gauss)
            save_dataset("raw/izero", sensor)
            save_dataset("raw/gap", motor)

        else:
            save_dataset("plot/x", motor)
            create_dataset("plot/y", 'd', False, (0, len(sensor)))
            append_dataset("plot/y", sensor)
            save_dataset("plot/title", "Gap Scan")
            save_dataset("plot/xlabel", "Gap")
            save_dataset("plot/ylabel", "Current")
            save_dataset("plot/y_desc", "scan 0")
            #save_dataset("scan/scantype", "Gap scan without fitting")
            save_dataset("raw/izero", sensor)
            save_dataset("raw/gap", motor)

        ## save beamline/station snapshot
        pink_save_bl_snapshot()

        # end routine
        if source=="izero":
            caput("PINK:CAE2:AcquireMode", 0)
        else:
            caput("PINK:CAE1:AcquireMode", 0)
            caput("PINK:CAE1:Range", 1)

        ## Setup CAE2
        #0:free run 1:ext trigger
        caput("PINK:CAE2:TriggerMode", 0)
        #0:continuous 1:multiple 2:single
        caput("PINK:CAE2:AcquireMode", 0)
        caput("PINK:CAE2:ValuesPerRead", 1000)
        caput("PINK:CAE2:AveragingTime", 1)
        caputq("PINK:CAE2:Acquire", 1)
            
        print("Scan finished. OK")

###########################################
### Support functions
###########################################

    def __gauss_fit(self, ydata, xdata):
        (a, b, amp, com, sigma) = fit_gaussian_linear(ydata, xdata)
        f = Gaussian(amp, com, sigma)
        xgauss = linspace(min(xdata), max(xdata), 400)
        gauss = [f.value(i)+(a*i)+b for i in xgauss]
        fwhm = 2.355*sigma
        return (a, b, amp, com, sigma, gauss, fwhm, xgauss)

    def __gauss_exp_fit(self, ydata, xdata):
        (incl, off, amp, com, sigma) = fit_gaussian_linear(ydata, xdata)
        start_point=[1, 1, amp, com, sigma]
        (eamp, decay, amp, com, sigma) = fit_gaussian_exp_bkg(ydata, xdata, start_point=start_point)
        f = Gaussian(amp, com, sigma)
        xgauss = linspace(min(xdata), max(xdata), 400)
        gauss = [f.value(i) + eamp*math.exp(-i/decay) for i in xgauss]
        fwhm = 2.355*sigma
        return (eamp, decay, amp, com, sigma, gauss, fwhm, xgauss)
