## filter scan

class FILTERSCAN():
    def scan(self,filters,start,end,step,exposure):
        #print("Filter scan..." + filters)

        ## variables
        DEBUG=0
        sensor = []
        motor = []
        prescan_pos = 0

        ## channels
        SENSOR = create_channel_device("PINK:CAE2:SumAll:MeanValue_RBV")
        SENSOR.setMonitored(True)
        ACQ = create_channel_device("PINK:CAE2:Acquire", type='i')
        ACQ.setMonitored(True)

        ## filter motor
        if filters=="f1":
            filter_desc = "Filter 1"
            MOTOR = create_channel_device("PINK:SMA01:m0.VAL")
            MOTOR_RBV = create_channel_device("PINK:SMA01:m0.RBV")
            MOTOR_RBV.setMonitored(True)
            MOTOR_DMOV = create_channel_device("PINK:SMA01:m0.DMOV")
            MOTOR_DMOV.setMonitored(True)
        elif filters=="f2":
            filter_desc = "Filter 2"
            MOTOR = create_channel_device("PINK:SMA01:m1.VAL")
            MOTOR_RBV = create_channel_device("PINK:SMA01:m1.RBV")
            MOTOR_RBV.setMonitored(True)
            MOTOR_DMOV = create_channel_device("PINK:SMA01:m1.DMOV")
            MOTOR_DMOV.setMonitored(True)
        elif filters=="f3":
            filter_desc = "Filter 3"
            MOTOR = create_channel_device("PINK:SMA01:m2.VAL")
            MOTOR_RBV = create_channel_device("PINK:SMA01:m2.RBV")
            MOTOR_RBV.setMonitored(True)
            MOTOR_DMOV = create_channel_device("PINK:SMA01:m2.DMOV")
            MOTOR_DMOV.setMonitored(True)
        elif filters=="sc":
            filter_desc = "Scatter"
            MOTOR = create_channel_device("PINK:SMA01:m5.VAL")
            MOTOR_RBV = create_channel_device("PINK:SMA01:m5.RBV")
            MOTOR_RBV.setMonitored(True)
            MOTOR_DMOV = create_channel_device("PINK:SMA01:m5.DMOV")
            MOTOR_DMOV.setMonitored(True)
        else:
            print("Invalid filter. Aborting!")
            return

        print("Scannig " + filter_desc)

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
        if filters=="sc":
            set_exec_pars(open=False, name="scatter", reset=True)
        else:
            set_exec_pars(open=False, name="filter", reset=True)

        save_dataset("scan/start_time", time.ctime())

        ## configure scan positions
        positionarray = linspace(start, end, step)

        ## plot setup
        if DEBUG: print("Setup plot")
        if filters=="sc":
            plottitle = "Scatter Scan"
        else:
            plottitle = "Filter Scan"

        ##[p1, p2]=plot([None, None], [filtes_desc,"Derivative"], title=plottitle)
        p1h=plot([None], [filter_desc], title=plottitle)
        p1 = p1h.get(0)
        p1.getAxis(p1.AxisId.X).setRange(min(start, end),max(start,end))
        ##p2.getAxis(p1.AxisId.X).setRange(min(start, end),max(start,end))
        #p1.addSeries(LinePlotSeries("Interpolation"))
        #p2.addSeries(LinePlotSeries("Fit"))

        print("Scanning...")

        # saving pre scan position
        prescan_pos = MOTOR_RBV.read()

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
            # if len(motor)>2:
            #     dt = deriv(sensor, xdata=motor)
            #     p2.getSeries(0).setData(motor, dt)


        save_dataset("scan/scantype", plottitle)
        save_dataset("scan/motor", filter_desc)
        save_dataset("raw/sensor", sensor)
        save_dataset("raw/blade", motor)

        ## Save plot data
        save_dataset("plot/title", plottitle)
        save_dataset("plot/xlabel", "position")
        save_dataset("plot/ylabel", "intensity")
        save_dataset("plot/x", motor)
        ## create plot dataset
        create_dataset("plot/y", 'd', False, (0, len(sensor)))
        create_dataset("plot/y_desc", 's', False)
        append_dataset("plot/y", sensor)
        append_dataset("plot/y_desc", filter_desc)

        save_dataset("scan/finish_time", time.ctime())

        ## Setup CAE2
        #0:continuous 1:multiple 2:single
        caput("PINK:CAE2:AcquireMode", 0) ## continuous

        ## Move back to original position
        MOTOR.write(prescan_pos)
        MOTOR_RBV.waitValueInRange(pos, 1.0, 60000)
        MOTOR_DMOV.waitValueInRange(1, 0.5, 60000)

        print("Scan complete")
