## slit scan

class SLITSCAN():
    def scan(self,slit,start,end,step,exposure):
        print("Slit scan..." + slit)

        ## variables
        DEBUG=0
        sensor = []
        motor = []

        ## channels
        SENSOR = create_channel_device("PINK:CAE2:SumAll:MeanValue_RBV")
        SENSOR.setMonitored(True)
        ACQ = create_channel_device("PINK:CAE2:Acquire", type='i')
        ACQ.setMonitored(True)

        ## slit motor
        if slit=="bottom":
            MOTOR = create_channel_device("PINK:PHY:AxisI.VAL")
            MOTOR_RBV = create_channel_device("PINK:PHY:AxisI.RBV")
            MOTOR_RBV.setMonitored(True)
            MOTOR_DMOV = create_channel_device("PINK:PHY:AxisI.DMOV")
            MOTOR_DMOV.setMonitored(True)
        elif slit=="top":
            MOTOR = create_channel_device("PINK:PHY:AxisH.VAL")
            MOTOR_RBV = create_channel_device("PINK:PHY:AxisH.RBV")
            MOTOR_RBV.setMonitored(True)
            MOTOR_DMOV = create_channel_device("PINK:PHY:AxisH.DMOV")
            MOTOR_DMOV.setMonitored(True)
        elif slit=="left":
            MOTOR = create_channel_device("PINK:PHY:AxisF.VAL")
            MOTOR_RBV = create_channel_device("PINK:PHY:AxisF.RBV")
            MOTOR_RBV.setMonitored(True)
            MOTOR_DMOV = create_channel_device("PINK:PHY:AxisF.DMOV")
            MOTOR_DMOV.setMonitored(True)
        elif slit=="right":
            MOTOR = create_channel_device("PINK:PHY:AxisG.VAL")
            MOTOR_RBV = create_channel_device("PINK:PHY:AxisG.RBV")
            MOTOR_RBV.setMonitored(True)
            MOTOR_DMOV = create_channel_device("PINK:PHY:AxisG.DMOV")
            MOTOR_DMOV.setMonitored(True)
        else:
            print("Invalid slit. Aborting")
            return

        ## setup caenels CAE2
        if DEBUG: log("Setup CAE2", data_file = False)
        #0:continuous 1:multiple 2:single
        caput("PINK:CAE2:AcquireMode", 2) ## single
        caput("PINK:CAE2:AveragingTime", exposure)
        caput("PINK:CAE2:ValuesPerRead", exposure*1000)
        #0:free run 1:ext trigger
        caput("PINK:CAE2:TriggerMode", 0) ## free run
        caputq("PINK:CAE2:Acquire", 0)

        ##set file name
        set_exec_pars(open=False, name="slit", reset=True)

        ## configure scan positions
        positionarray = linspace(start, end, step)

        ## plot setup
        if DEBUG: print("Setup plot")
        [p1, p2]=plot([None, None], [slit+" slit","Derivative"], title="Slit Scan")
        p1.getAxis(p1.AxisId.X).setRange(min(start, end),max(start,end))
        p2.getAxis(p1.AxisId.X).setRange(min(start, end),max(start,end))
        #p1.addSeries(LinePlotSeries("Interpolation"))
        p2.addSeries(LinePlotSeries("Fit"))

        print("Scanning...")

        ## Main loop
        for pos in positionarray:
            MOTOR.write(pos)
            #BPOS.waitInPosition(pos, 20000)
            MOTOR_RBV.waitValueInRange(pos, 1.0, 60000)
            MOTOR_DMOV.waitValueInRange(1, 0.5, 60000)
            ACQ.write(1)
            resp = SENSOR.waitCacheChange(1000*int(exposure+2))
            if resp==False:
                print("Abort: No data from ampmeter")
                return
            sensor.append(SENSOR.take())
            motor.append(MOTOR_RBV.take())
            p1.getSeries(0).setData(motor, sensor)
            if len(motor)>2:
                dt = deriv(sensor, xdata=motor)
                p2.getSeries(0).setData(motor, dt)

        print("Analysing data...")
        dt = deriv(sensor, xdata=motor)
        #p2.getSeries(1).setData(motor, dt)
        if mean(dt)<0:
            dt = [-i for i in dt]
        p2.getSeries(0).setData(motor, dt)

        ## gauss fitting
        try:
            (off, amp, com, sigma) = fit_gaussian_offset(dt, motor)
            f = Gaussian(amp, com, sigma)
            xgauss = linspace(min(motor), max(motor), 100)
            gauss = [f.value(i)+off for i in xgauss]
            fwhm = 2.355*sigma
            p2.getSeries(1).setData(xgauss, gauss)
            p2.setLegendVisible(True)
            print("*** Gaussian fit ***")
            print("--------------------")
            print("   Offset: " + '{:.3e}'.format(off))
            print("Amplitude: " + '{:.3e}'.format(amp))
            print("     Mean: " + '{:.3f}'.format(com))
            print("    Sigma: " + '{:.3f}'.format(sigma))
            print("     FWHM: " + '{:.3f}'.format(fwhm))
            print("--------------------")
        except:
            print("Failed to fit gaussian")
            off = 0
            amp = 0
            com = 0
            sigma = 0
            xgauss = 0
            gauss = 0
            fwhm = 0

        save_dataset("scan/scantype", "slit scan")
        save_dataset("scan/slit", slit)
        save_dataset("gaussian/offset", off)
        save_dataset("gaussian/amplitude", amp)
        save_dataset("gaussian/mean", com)
        save_dataset("gaussian/sigma", sigma)
        save_dataset("gaussian/FWHM", fwhm)
        save_dataset("plot/gaussY_fit", gauss)
        save_dataset("plot/gaussX_fit", xgauss)
        save_dataset("processed/derivative", dt)
        save_dataset("raw/sensor", sensor)
        save_dataset("raw/blade", motor)

        ## Setup CAE2
        #0:continuous 1:multiple 2:single
        caput("PINK:CAE2:AcquireMode", 0) ## continuous
