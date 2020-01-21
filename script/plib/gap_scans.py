#gap_scans.py

class GAPSCAN():
    def __init__(self):
        pass

########################################
### scan
########################################

    def scan(self, start=0, end=0, step=0, exposure=0.0, fit=None):
        if exposure==0:
            print("abort: exposure = 0")
            return
            
        set_exec_pars(open=False, name="gap", reset=True)
        
        verbose=True

        if verbose: print("Creating channels")
        ## channels
        SENSOR2 = create_channel_device("PINK:CAE2:SumAll:MeanValue_RBV")
        SENSOR2.setMonitored(True)
        ACQ = create_channel_device("PINK:CAE2:Acquire", type='i')
        ACQ.setMonitored(True)
        #MOTOR = create_channel_device("U17IT6R:BaseParGapsel.B")
        #MOTOR_SET = create_channel_device("U17IT6R:BaseCmdCalc.PROC")
        #MOTOR_RBV = create_channel_device("U17IT6R::BasePmGap.A")
        #MOTOR_RBV.setMonitored(True)   
        #motor_deadband = 2.0

        ## simulated channels
        SENSOR = create_channel_device("PINK:GAPSIM:izero")
        SENSOR.setMonitored(True)
        MOTOR = create_channel_device("PINK:GAPSIM:gapset")
        MOTOR_SET = create_channel_device("PINK:GAPSIM:gapexec.PROC")
        MOTOR_RBV = create_channel_device("PINK:GAPSIM:m1.RBV")
        MOTOR_RBV.setMonitored(True)   
        motor_deadband = 0.1

        ## variables
        sensor = []
        motor = []
                    
        ## Setup 
        #print("Scanning ...")
        set_exec_pars(open=False, name="gap", reset=True)

        if verbose: print("Setup ampmeter")
        ## Configure ampmeter
        exposure=float(exposure)
        ACQ.write(0)
        sleep(1)
        caput("PINK:CAE2:ValuesPerRead", int(1000*exposure))
        caput("PINK:CAE2:AveragingTime", exposure)
        caput("PINK:CAE2:TriggerMode", 0)
        caput("PINK:CAE2:AcquireMode", 2)
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
        while(abs(pos-MOTOR_RBV.take()) > motor_deadband):
            mystat = "Gap: " + str(MOTOR_RBV.take())
            set_status(mystat)
            sleep(0.5)
        #MOTOR_RBV.waitValueInRange(positionarray[0], motor_deadband, 60000)
        
        if verbose: print("Scanning...")
        ## Main loop
        for pos in positionarray:
            MOTOR.write(pos)
            MOTOR_SET.write(1)
            MOTOR_RBV.waitValueInRange(pos, motor_deadband, 10000)
            
            while(ACQ.take()==1):
                sleep(0.25)
            ACQ.write(1)
            resp = SENSOR2.waitCacheChange(1000*int(exposure+2))
            if resp==False:
                print("Abort: No data from ampmeter")
                return
            
            sensor.append(SENSOR.take())
            motor.append(MOTOR_RBV.take())
            p1.getSeries(0).setData(motor, sensor)

    
        ## Fitting options
        if fit=="linear":
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
            save_dataset("scan/scantype", "Gap scan with linear bg gaussian fitting")
            save_dataset("gaussian/inclination", a)
            save_dataset("gaussian/offset", b)
            save_dataset("gaussian/amplitude", amp)
            save_dataset("gaussian/mean", com)
            save_dataset("gaussian/sigma", sigma)
            save_dataset("gaussian/fwhm", fwhm)
            save_dataset("plot/x", xgauss)
            save_dataset("plot/y", gauss)
            save_dataset("raw/sensor", sensor)
            save_dataset("raw/gap", motor)
            
        elif fit == "exp":
            if verbose: print("analysing")
            (eamp, decay, amp, com, sigma, gauss, fwhm, xgauss)=self.__gauss_exp_fit(sensor,motor)
            p1.getSeries(1).setData(xgauss, gauss)
            p1.setLegendVisible(True)
            print(" ")
            print("Gaussian fit -- expontial background")
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
            save_dataset("raw/sensor", sensor)
            save_dataset("raw/gap", motor)
            
        else:    
            save_dataset("scan/scantype", "Gap scan without fitting")
            save_dataset("raw/sensor", sensor)
            save_dataset("raw/blade", motor)

        # end routine
        caput("PINK:CAE2:AcquireMode", 0)
        print(".")

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