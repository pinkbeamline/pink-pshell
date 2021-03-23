class SAMPLESCAN():
    def scan(self, axis, start, end, step, exposure, moveback):
        print("Sample scan for ge")

        ## variables
        sensor = []
        motor = []
        prescan_pos = 0

        ## GE channels
        GE_acquire = create_channel_device("PINK:GEYES:cam1:Acquire", type='i')
        GE_status = create_channel_device("PINK:GEYES:cam1:DetectorState_RBV", type='i')
        GE_status.setMonitored(True)
        GE_FrameID = create_channel_device("PINK:GEYES:cam1:ArrayCounter_RBV", type='i')
        GE_FrameID.setMonitored(True)
        SENSOR = create_channel_device("PINK:GEYES:spectra_avg", type='d')
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
        set_exec_pars(open=False, name="sample_scan_ge", reset=True)

        ## save initial scan data
        save_dataset("scan/start_time", time.ctime())
        save_dataset("scan/type", "sample scan with ge")

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

        ## Setup delay generator
        ## (trigger mode, shutter, Mythen, Greateyes, Caenels)
        ## [trigger mode] [5:single shot] [1: Ext rising edge]
        self.setup_delaygen(1, [0, exposure-0.02], [0, 0], [0, exposure+0.15], [0, 0.001])

        ## Setup trigger switch
        ## A=Delaygen Trigger Source [0:OFF, 1:CCD, 2:mythen, 3:eiger]
        ## B=Caenels Trigger Source [0:OFF, 1:Delaygen, 2:Output A]
        caput("PINK:RPISW:select_A", 1)
        caput("PINK:RPISW:select_B", 1)

        ## Stop greateyes
        if GE_status.read():
            GE_acquire.write(0)
            if DEBUG: log("GE Stop", data_file = False)
            while(GE_status.read()):
                sleep(1)
            if DEBUG: log("GE Idle", data_file = False)

        ## setup greateyes
        caput("PINK:GEYES:cam1:AcquireTime", exposure)
        caput("PINK:GEYES:cam1:ImageMode", 0) # single image

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
            sleep(0.25)
            #MOTOR_RBV.waitValueInRange(pos, 1.0, 60000)
            MOTOR_DMOV.waitValueInRange(1, 0.5, 60000)
            GE_acquire.write(1)
            #resp = SENSOR.waitCacheChange(1000*int(exposure+2))
            resp = GE_FrameID.waitCacheChange(1000*int(exposure+2))
            sleep(0.1)
            if resp==False:
                print("Timeout: No data from ge")
                continue
            sensor.append(SENSOR.take())
            motor.append(MOTOR_RBV.take())
            p1.getSeries(0).setData(motor, sensor)

        # close fast shutter
        caput("PINK:PLCGAS:ei_B01", 0)            

        ## Save data
        save_dataset("raw/sensor", sensor)
        save_dataset("raw/position", motor)

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

        ## Setup delay generator
        ## (trigger mode, shutter, Mythen, Greateyes, Caenels)
        ## [trigger mode] [5:single shot] [1: Ext rising edge]
        self.setup_delaygen(5, [0, exposure-0.02], [0, 0], [0, exposure+0.15], [0, 0.001])

        ## Move back to original position
        if (moveback!=0):
            MOTOR.write(prescan_pos)
            #MOTOR_RBV.waitValueInRange(pos, 1.0, 60000)
            MOTOR_DMOV.waitValueInRange(1, 0.5, 60000)

        ## save beamline/station snapshot
        pink_save_bl_snapshot()

        print("Scan complete")


    def setup_delaygen(self, mode, ch1, ch2, ch3, ch4):
        ## Trigger mode
        caput("PINK:DG01:TriggerSourceMO", mode)
        ## shutter delay
        caput("PINK:DG01:ADelayAO", ch1[0])
        ## shutter exposure
        caput("PINK:DG01:BDelayAO", ch1[1])
        ## mythen delay
        caput("PINK:DG01:CDelayAO", ch2[0])
        ## mythen exposure
        caput("PINK:DG01:DDelayAO", ch2[1])
        ## greateyes delay
        caput("PINK:DG01:EDelayAO", ch3[0])
        ## greateyes exposure
        caput("PINK:DG01:FDelayAO", ch3[1])
        ## extra channel delay
        caput("PINK:DG01:GDelayAO", ch4[0])
        ## extra channel exposure
        caput("PINK:DG01:HDelayAO", ch4[1])

