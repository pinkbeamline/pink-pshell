## blade scan
class BLADESCAN():
        def __init__(self):
            pass

##################################################################

        def run_diag_scan(self, start=0, end=0, steps=0, exposure=0):
            if (exposure == 0):
                print("Abort: exposure = 0 ")
                return

            set_exec_pars(open=False, name="blade", reset=True)

            verbose=True

            if verbose: print("Creating channels")
            ## channels
            SENSOR = create_channel_device("PINK:CAE2:SumAll:MeanValue_RBV")
            SENSOR.setMonitored(True)
            ACQ = create_channel_device("PINK:CAE2:Acquire", type='i')
            ACQ.setMonitored(True)
            MOTOR = create_channel_device("PINK:SMA01:m0")
            MOTOR_RBV = create_channel_device("PINK:SMA01:m0.RBV")
            MOTOR_RBV.setMonitored(True)

            ## simulated channels
            #SENSOR = create_channel_device("PINK:MSIM2:sigmoid")
            #SENSOR.setMonitored(True)
            #MOTOR = create_channel_device("PINK:MSIM2:m5")
            #MOTOR_RBV = create_channel_device("PINK:MSIM2:m5.RBV")
            #bladepos_RBV.setMonitored(True)
            #add_device(ch.psi.pshell.epics.Positioner("BPOS", "PINK:MSIM2:m5", "PINK:MSIM2:m5.RBV", True))
            #MOTOR_RBV.setMonitored(True)

            ## variables
            sensor = []
            motor = []
            prescan_pos = 0

            ## Setup
            #print("Scanning ...")
            set_exec_pars(open=False, name="blade", reset=True)

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
            positionarray = linspace(start, end, steps)

            ## plot setup
            if verbose: print("Setup plot")
            [p1, p2]=plot([None, None], ["Scan","Derivative"], title="Blade Scan")
            p1.getAxis(p1.AxisId.X).setRange(min(start, end),max(start,end))
            p2.getAxis(p1.AxisId.X).setRange(min(start, end),max(start,end))
            #p1.addSeries(LinePlotSeries("Interpolation"))
            p2.addSeries(LinePlotSeries("Fit"))

            if verbose: print("Scanning...")

            prescan_pos = MOTOR_RBV.read()

            ## Main loop
            for pos in positionarray:
                MOTOR.write(pos)
                #BPOS.waitInPosition(pos, 20000)
                MOTOR_RBV.waitValueInRange(pos, 2.0, 30000)
                while(ACQ.take()==1):
                    sleep(0.25)
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

            if verbose: print("Analysing data")
            dt = deriv(sensor, xdata=motor)
            p2.getSeries(1).setData(motor, dt)
            if mean(dt)<0:
                dt = [-i for i in dt]
            #bpos2 = bpos2[:-1]
            #dt = dt[:-1]
            #print(dt)
            p2.getSeries(0).setData(motor, dt)
            (off, amp, com, sigma, gauss, fwhm, xgauss)=self.__gauss_fit(dt, motor)
            p2.getSeries(1).setData(xgauss, gauss)
            p2.setLegendVisible(True)
            self.__print_info(off, amp, com, sigma, fwhm)

            save_dataset("scan/scantype", "Diagnostic chamber blade scan")
            save_dataset("gaussian/offset", off)
            save_dataset("gaussian/amplitude", amp)
            save_dataset("gaussian/mean", com)
            save_dataset("gaussian/sigma", sigma)
            save_dataset("gaussian/FWHM", fwhm)
            save_dataset("plot/gaussY_fit", gauss)
            save_dataset("plot/gaussX_fit", xgauss)
            save_dataset("processed/derivative", dt)
            #save_dataset("diodes/diode1", self.diode1)
            #save_dataset("diodes/diode2", self.diode2)
            #save_dataset("diodes/diode3", self.diode3)
            #save_dataset("diodes/diode4", self.diode4)
            save_dataset("raw/sensor", sensor)
            save_dataset("raw/blade", motor)

            caput("PINK:CAE2:AcquireMode", 0)

            ## Setup CAE2
            #0:free run 1:ext trigger
            caput("PINK:CAE2:TriggerMode", 0)
            #0:continuous 1:multiple 2:single
            caput("PINK:CAE2:AcquireMode", 0)
            caput("PINK:CAE2:ValuesPerRead", 1000)
            caput("PINK:CAE2:AveragingTime", 1)
            caputq("PINK:CAE2:Acquire", 1)

            ## Move motor back to pre scan position
            MOTOR.write(prescan_pos)
            MOTOR_RBV.waitValueInRange(prescan_pos, 1.0, 60000)
            #MOTOR_DMOV.waitValueInRange(1, 0.5, 60000)

            pink_save_bl_snapshot()

            print("OK")

###############################################################3

        def run_sec_scan(self, source, axis, start=0, end=0, steps=0, exposure=0):
            if (source != "bpm3") & (exposure == 0):
                print("Abort: exposure = 0 ")
                return

        if source=="bpm3":
            ## check for bpm3 diode status
            diode_out = int(caget("PINK:PLCGAS:vdiode_FA_LS"))==1
            if diode_out:
                print("[Warning] The diode on BPM3 is not in the beam path. Aborting.")
                return

            ## check for filters attenuation
            filter_att = float(caget("PINK:FILTER:TxNow"))
            if filter_att > 0.5:
                print("[Warning] Please check the attenuation filters to avoid diode damage.")
                print("[Warning] The total attenuation is now approximately: 1/{:.0f}".format(1/filter_att))

            set_exec_pars(open=False, name="blade", reset=True)

            verbose=True

            if verbose: print("Creating channels")
            ## channels
            if source == "tfy":
                ## TFY diode
                SENSOR = create_channel_device("PINK:CAE1:Current2:MeanValue_RBV")
                SENSOR.setMonitored(True)
            elif source == "bpm3":
                SENSOR = create_channel_device("PINK:CAE1:Current3:MeanValue_RBV")
                SENSOR.setMonitored(True)
                SENSOR_ID = create_channel_device("PINK:CAE1:NumAcquired")
                SENSOR_ID.setMonitored(True)
            else:
                print("Blade scan is not not available for this source.")
                return

            ACQ = create_channel_device("PINK:CAE1:Acquire", type='i')
            ACQ.setMonitored(True)

            if axis=="y":
                MOTOR = create_channel_device("PINK:SMA01:m9")
                MOTOR_RBV = create_channel_device("PINK:SMA01:m9.RBV")
                MOTOR_RBV.setMonitored(True)
            elif axis=="x":
                MOTOR = create_channel_device("PINK:SMA01:m10")
                MOTOR_RBV = create_channel_device("PINK:SMA01:m10.RBV")
                MOTOR_RBV.setMonitored(True)
            else:
                print("axis option is invalid.")
                return

            ## simulated channels
            #SENSOR = create_channel_device("PINK:MSIM2:sigmoid")
            #SENSOR.setMonitored(True)
            #MOTOR = create_channel_device("PINK:MSIM2:m5")
            #MOTOR_RBV = create_channel_device("PINK:MSIM2:m5.RBV")
            #bladepos_RBV.setMonitored(True)
            #add_device(ch.psi.pshell.epics.Positioner("BPOS", "PINK:MSIM2:m5", "PINK:MSIM2:m5.RBV", True))
            #MOTOR_RBV.setMonitored(True)

            ## variables
            sensor = []
            motor = []
            prescan_pos = 0

            ## Setup
            #print("Scanning ...")
            set_exec_pars(open=False, name="blade", reset=True)

            if verbose: print("Setup ampmeter")
            ## Configure ampmeter
            exposure=float(exposure)
            ACQ.write(0)
            sleep(1)
            caput("PINK:CAE1:ValuesPerRead", int(1000*exposure))
            caput("PINK:CAE1:AveragingTime", exposure)
            caput("PINK:CAE1:TriggerMode", 0)
            caput("PINK:CAE1:AcquireMode", 2)

           # if source == "tfy":
           #     caput("PINK:CAE1:Range", 1)
           # else:
           #     caput("PINK:CAE1:Range", 0)
            sleep(1)

            ## configure scan positions
            positionarray = linspace(start, end, steps)

            ## plot setup
            if verbose: print("Setup plot")
            [p1, p2]=plot([None, None], ["Scan","Derivative"], title="Blade Scan")
            p1.getAxis(p1.AxisId.X).setRange(min(start, end),max(start,end))
            p2.getAxis(p1.AxisId.X).setRange(min(start, end),max(start,end))
            #p1.addSeries(LinePlotSeries("Interpolation"))
            p2.addSeries(LinePlotSeries("Fit"))

            if verbose: print("Scanning...")

            prescan_pos = MOTOR_RBV.read()

            ## Main loop
            for pos in positionarray:
                MOTOR.write(pos)
                #BPOS.waitInPosition(pos, 20000)
                MOTOR_RBV.waitValueInRange(pos, 2.0, 30000)

                while(ACQ.take()==1):
                    sleep(0.25)
                ACQ.write(1)
                resp = SENSOR.waitCacheChange(1000*int(exposure+2))
                if resp==False:
                    print("Abort: No data from ampmeter")
                    return

                sensor.append(SENSOR.read())
                motor.append(MOTOR_RBV.take())
                p1.getSeries(0).setData(motor, sensor)
                if len(motor)>2:
                    dt = deriv(sensor, xdata=motor)
                    p2.getSeries(0).setData(motor, dt)

            if verbose: print("Analysing data")
            dt = deriv(sensor, xdata=motor)
            p2.getSeries(1).setData(motor, dt)
            if mean(dt)<0:
                dt = [-i for i in dt]
            #bpos2 = bpos2[:-1]
            #dt = dt[:-1]
            p2.getSeries(0).setData(motor, dt)
            (off, amp, com, sigma, gauss, fwhm, xgauss)=self.__gauss_fit(dt, motor)
            p2.getSeries(1).setData(xgauss, gauss)
            p2.setLegendVisible(True)
            self.__print_info(off, amp, com, sigma, fwhm)

            save_dataset("scan/scantype", "Sample chamber blade scan")
            save_dataset("gaussian/offset", off)
            save_dataset("gaussian/amplitude", amp)
            save_dataset("gaussian/mean", com)
            save_dataset("gaussian/sigma", sigma)
            save_dataset("gaussian/FWHM", fwhm)
            save_dataset("plot/gaussY_fit", gauss)
            save_dataset("plot/gaussX_fit", xgauss)
            save_dataset("processed/derivative", dt)
            #save_dataset("diodes/diode1", self.diode1)
            #save_dataset("diodes/diode2", self.diode2)
            #save_dataset("diodes/diode3", self.diode3)
            #save_dataset("diodes/diode4", self.diode4)
            save_dataset("raw/sensor", sensor)
            save_dataset("raw/blade", motor)

            caput("PINK:CAE1:AcquireMode", 0)

            ## Setup CAE2
            #0:free run 1:ext trigger
            caput("PINK:CAE2:TriggerMode", 0)
            #0:continuous 1:multiple 2:single
            caput("PINK:CAE2:AcquireMode", 0)
            caput("PINK:CAE2:ValuesPerRead", 1000)
            caput("PINK:CAE2:AveragingTime", 1)
            caputq("PINK:CAE2:Acquire", 1)

            ## Move motor back to pre scan position
            MOTOR.write(prescan_pos)
            MOTOR_RBV.waitValueInRange(prescan_pos, 1.0, 60000)
            #MOTOR_DMOV.waitValueInRange(1, 0.5, 60000)

            pink_save_bl_snapshot()
            print("OK")

        ######################################
        ### Support Functions
        ######################################

        def __gauss_fit(self, ydata, xdata):
            (off, amp, com, sigma) = fit_gaussian_offset(ydata, xdata)
            f = Gaussian(amp, com, sigma)
            xgauss = linspace(min(xdata), max(xdata), 100)
            gauss = [f.value(i)+off for i in xgauss]
            fwhm = 2.355*sigma
            return (off, amp, com, sigma, gauss, fwhm, xgauss)

        def __print_info(self, off, amp, com, sigma, fwhm):
            print("*** Gaussian fit ***")
            print("--------------------")
            print("   Offset: " + '{:.3e}'.format(off))
            print("Amplitude: " + '{:.3e}'.format(amp))
            print("     Mean: " + '{:.3f}'.format(com))
            print("    Sigma: " + '{:.3f}'.format(sigma))
            print("     FWHM: " + '{:.3f}'.format(fwhm))
            print("--------------------")
