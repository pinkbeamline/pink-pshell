#dcm_scans.py

class DCMSCAN():
    def __init__(self):
        pass

########################################
### scan
########################################

    def scan(self, source, start=0, end=0, step=0, exposure=0.0, fit=False):
        #print(source)
        print("* DCM scan *")
        return
        
        if exposure==0:
            print("abort: exposure = 0")
            return

        #set_exec_pars(open=False, name="dcm", reset=True)

        verbose=True
        DEBUG=False

        if verbose: print("Creating channels")
        ## channels
        if source=="izero":
            SENSOR = create_channel_device("PINK:CAE2:SumAll:MeanValue_RBV")
            SENSOR.setMonitored(True)
            ACQ = create_channel_device("PINK:CAE2:Acquire", type='i')
            ACQ.setMonitored(True)
        elif source=="bpm3":
            SENSOR = create_channel_device("PINK:CAE1:Current3:MeanValue_RBV")
            SENSOR.setMonitored(True)
            ACQ = create_channel_device("PINK:CAE1:Acquire", type='i')
            ACQ.setMonitored(True)
        else:
            print("DCM scan is not available for this source.")
            return

        #MOTOR = create_channel_device("U17IT6R:BaseParGapsel.B")
        #MOTOR_SET = create_channel_device("U17IT6R:BaseCmdCalc.PROC")
        #MOTOR_RBV = create_channel_device("U17IT6R:BasePmGap.A")
        #MOTOR_RBV.setMonitored(True)
        #motor_deadband = 0.02

        #MOTOR = create_channel_device("u171dcm1:monoSetEnergy")
        #MOTOR_RBV = create_channel_device("u171dcm1:monoGetEnergy")
        #MOTOR_RBV.setMonitored(True)
        #MOTOR_DMOV = create_channel_device("u171dcm1:axis6:running", type='i')
        #MOTOR_DMOV.setMonitored(True)

        ## variables
        sensor = []
        motor = []

        ## Setup
        #print("Scanning ...")
        set_exec_pars(open=False, name="dcm", reset=True)
        save_dataset("scan/scantype", "DCM scan")

        ## setup DCM
        # Set IdOn {0:off, 1:on}
        #caput("u171dcm1:SetIdOn", 1)

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
        [p1] = plot(None, "Scan", title="DCM Scan")
        p1.getAxis(p1.AxisId.X).setRange(min(start, end),max(start,end))
        p1.addSeries(LinePlotSeries("Fit"))

        if verbose: print("Moving DCM to start position")
        initpos = MOTOR_RBV.take()
        pos = positionarray[0]
        MOTOR.write(pos)
        sleep(0.2)
        self.__waitdcm()

        if verbose: print("Scanning...")
        set_status("Scanning...")
        try:
            ## Main loop
            for pos in positionarray:
                set_status("Energy: {} eV".format(pos))

                ## move and wait for dcm
                MOTOR.write(pos)
                sleep(0.2)
                self.__waitdcm()

                ## read sensor
                trycount = 0
                waitsensor = True
                # try 3 times to read ampmeter
                pos_skip=False
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
            print("DCM scan aborted.")

        set_status("End of scan...")

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
            #save_dataset("scan/scantype", "DCM scan with linear bg gaussian fitting")
            save_dataset("gaussian/inclination", a)
            save_dataset("gaussian/offset", b)
            save_dataset("gaussian/amplitude", amp)
            save_dataset("gaussian/mean", com)
            save_dataset("gaussian/sigma", sigma)
            save_dataset("gaussian/fwhm", fwhm)
            save_dataset("plot/x", xgauss)
            save_dataset("plot/y", gauss)
            save_dataset("raw/izero", sensor)
            save_dataset("raw/dcm", motor)

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
            save_dataset("scan/scantype", "DCM scan with exponential bg gaussian fitting")
            save_dataset("gaussian/exp_amplitude", eamp)
            save_dataset("gaussian/exp_decay", decay)
            save_dataset("gaussian/amplitude", amp)
            save_dataset("gaussian/mean", com)
            save_dataset("gaussian/sigma", sigma)
            save_dataset("gaussian/fwhm", fwhm)
            save_dataset("plot/x", xgauss)
            save_dataset("plot/y", gauss)
            save_dataset("raw/izero", sensor)
            save_dataset("raw/dcm", motor)

        else:
            save_dataset("plot/x", motor)
            create_dataset("plot/y", 'd', False, (0, len(sensor)))
            append_dataset("plot/y", sensor)
            save_dataset("plot/title", "DCM Scan")
            save_dataset("plot/xlabel", "DCM")
            save_dataset("plot/ylabel", "Current")
            save_dataset("plot/y_desc", "scan 0")
            #save_dataset("scan/scantype", "DCM scan without fitting")
            save_dataset("raw/izero", sensor)
            save_dataset("raw/dcm", motor)

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

        ## Return DCM to initial position
        MOTOR.write(initpos)
        sleep(0.2)
        self.__waitdcm()

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

    def __waitdcm(self):
        #set_status("Waiting for dcm...")
        while(MOTOR_DMOV.take()==0):
            sleep(0.25)
        