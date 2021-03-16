class SAMPLESCAN():
    def scan(self, axis, start, end, step, exposure, moveback):
        print("Sample scan for eiger")

        ## variables 
        sensor = []
        motor = []
        prescan_pos = 0
        DEBUG=0

        ## Eiger channels
        Eiger_acquire = create_channel_device("PINK:EIGER:cam1:Acquire", type='i')
        Eiger_status = create_channel_device("PINK:EIGER:cam1:Acquire_RBV", type='i')
        Eiger_status.setMonitored(True)
        Eiger_frameID = create_channel_device("PINK:EIGER:cam1:ArrayCounter_RBV", type='d')
        Eiger_frameID.setMonitored(True)
#        Eiger_roi_array = create_channel_device("PINK:EIGER:image3:ArrayData", type='[d', size=int(Eiger_ROI_X*Eiger_ROI_Y))
#        Eiger_roi_array.setMonitored(True)
#        Eiger_Spectra = create_channel_device("PINK:EIGER:spectrum_RBV", type='[d', size=Eiger_ROI_X)
#        Eiger_Spectra.setMonitored(True)
#        Eiger_Spectra_sum = create_channel_device("PINK:EIGER:specsum_RBV", type='[d', size=Eiger_ROI_X)
        Eiger_trigger = create_channel_device("PINK:EIGER:cam1:Trigger", type='d')
        SENSOR = create_channel_device("PINK:EIGER:spectra_avg", type='d')
        SENSOR.setMonitored(True)

        ## sample motor
        if axis=="x":
            MOTOR = create_channel_device("PINK:PHY:AxisJ.VAL", type='d')
            MOTOR_RBV = create_channel_device("PINK:PHY:AxisJ.RBV", type='d')
            MOTOR_RBV.setMonitored(True)
            MOTOR_DMOV = create_channel_device("PINK:PHY:AxisJ.DMOV", type='d')
            MOTOR_DMOV.setMonitored(True)
            
        if axis=="y":
            MOTOR = create_channel_device("PINK:ANC01:ACT0:CMD:TARGET", type='d')
            MOTOR_RBV = create_channel_device("PINK:ANC01:ACT0:POSITION", type='d')
            MOTOR_RBV.setMonitored(True)
            MOTOR_DMOV = create_channel_device("PINK:ANC01:ACT0:IN_TARGET", type='d')
            MOTOR_DMOV.setMonitored(True)

        ## setup filename
        set_exec_pars(open=False, name="sample_scan_eiger", reset=True)

        ## save initial scan data
        save_dataset("scan/start_time", time.ctime())
        save_dataset("scan/type", "sample scan with eiger")

        ## configure scan positions
        positionarray = linspace(start, end, step)

        ## plot setup
        if axis=='x':
            ypos = '{:.1f}'.format(caget("PINK:ANC01:ACT0:POSITION"))
            xlabel = 'X position'
            plottitle = 'Horizontal Sample Scan (Y='+ypos+')'
        else:
            ypos = '{:.1f}'.format(caget("PINK:PHY:AxisJ.RBV"))
            xlabel = 'Y position'
            plottitle = 'Vertical Sample Scan (X='+ypos+')'
        p1h=plot([None], [xlabel], title=plottitle)
        p1 = p1h.get(0)
        p1.getAxis(p1.AxisId.X).setRange(min(start, end),max(start,end))

        ## Stop eiger
        if Eiger_status.read():
            Eiger_acquire.write(0)
            if DEBUG: log("Eiger Stop", data_file = False)
            while(Eiger_status.read()):
                sleep(1)
            if DEBUG: log("Eiger Idle", data_file = False)

        ## setup eiger
        caput("PINK:EIGER:cam1:AcquireTime", exposure)
        sleep(1)
        caput("PINK:EIGER:cam1:AcquirePeriod", exposure+0.001)
        caput("PINK:EIGER:cam1:NumImages", 1)
        caput("PINK:EIGER:cam1:NumTriggers", len(positionarray))
        # manual trigger enable
        caput("PINK:EIGER:cam1:ManualTrigger", 1)
        sleep(0.5)
        ## arm detector
        Eiger_acquire.write(1)

        print("Scanning...")

        # saving pre scan position
        prescan_pos = MOTOR_RBV.read()

        # Move to first position
        MOTOR.write(positionarray[0])
        # wait up to 3 minutes to reach first position
        sleep(0.25)
        MOTOR_DMOV.waitValueInRange(1, 0.5, 180000)

        # Open fast shutter
        caput("PINK:PLCGAS:ei_B01", 1)

        ## Main loop
        for pos in positionarray:
            MOTOR.write(pos)
            #MOTOR_RBV.waitValueInRange(pos, 5.0, 60000)
            sleep(0.25)
            MOTOR_DMOV.waitValueInRange(1, 0.5, 60000)
            Eiger_trigger.write(1)
            #resp = SENSOR.waitCacheChange(1000*int(exposure+2))
            resp = Eiger_frameID.waitCacheChange(1000*int(exposure+2))
            sleep(0.1)
            if resp==False:
                print("Timeout: No data from eiger")
                continue
            sensor.append(SENSOR.take())
            motor.append(MOTOR_RBV.take())
            p1.getSeries(0).setData(motor, sensor)

        # close fast shutter
        caput("PINK:PLCGAS:ei_B01", 0)

        ## Stop eiger
        if Eiger_status.read():
            Eiger_acquire.write(0)
            if DEBUG: log("Eiger Stop", data_file = False)
            while(Eiger_status.read()):
                sleep(1)
            if DEBUG: log("Eiger Idle", data_file = False)

        ## setup eiger
        caput("PINK:EIGER:cam1:AcquireTime", 1)
        sleep(1)
        caput("PINK:EIGER:cam1:AcquirePeriod", 1.001)
        caput("PINK:EIGER:cam1:NumImages", 1)
        caput("PINK:EIGER:cam1:NumTriggers", 1)
        # manual trigger enable
        caput("PINK:EIGER:cam1:ManualTrigger", 0)

        ## Save data
        save_dataset("raw/sensor", sensor)
        save_dataset("raw/motor", motor)

        ## Save plot data
        save_dataset("plot/title", plottitle)
        save_dataset("plot/xlabel", "Position")
        save_dataset("plot/ylabel", "Counts per second")
        save_dataset("plot/y_desc", "Pass 0")
        save_dataset("plot/x", motor)
        create_dataset("plot/y", 'd', False, (0, len(sensor)))
        append_dataset("plot/y", sensor)

        ## save data
        save_dataset("scan/finish_time", time.ctime())

        ## Move back to original position
        if (moveback!=0):
            MOTOR.write(prescan_pos)
            sleep(0.25)
            #MOTOR_RBV.waitValueInRange(pos, 1.0, 60000)
            MOTOR_DMOV.waitValueInRange(1, 0.5, 180000)

        ## save beamline/station snapshot
        pink_save_bl_snapshot()

        print("Scan complete")
