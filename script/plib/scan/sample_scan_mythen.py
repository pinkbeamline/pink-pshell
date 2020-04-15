class SAMPLESCAN():
    def scan(self, axis, start, end, step, exposure):
        print("Sample scan for mythen")

        ## variables
        sensor = []
        motor = []
        prescan_pos = 0

        ## Mythen channels
        Mythen_acquire = create_channel_device("PINK:MYTHEN:cam1:Acquire", type='i')
        Mythen_status = create_channel_device("PINK:MYTHEN:cam1:Acquire_RBV", type='i')
        Mythen_status.setMonitored(True)
        ##### needs to add PV for mythen CPS
        Sensor = create_channel_device("PINK:MYTHEN:.......", type='d')
        Sensor.setMonitored(True)
#        Mythen_frameID = create_channel_device("PINK:MYTHEN:cam1:ArrayCounter_RBV", type='d')
#        Mythen_frameID.setMonitored(True)
#        Mythen_Spectra = create_channel_device("PINK:MYTHEN:RawInverted", type='[d', size=Mythen_X)
#        Mythen_Spectra.setMonitored(True)
#        Mythen_Spectra_sum = create_channel_device("PINK:MYTHEN:specsum_RBV", type='[d', size=Mythen_X)

        ## sample motor
        if axis=="x":
            MOTOR = create_channel_device("PINK:SMA01:m10.VAL")
            MOTOR_RBV = create_channel_device("PINK:SMA01:m10.RBV")
            MOTOR_RBV.setMonitored(True)
            MOTOR_DMOV = create_channel_device("PINK:SMA01:m10.DMOV")
            MOTOR_DMOV.setMonitored(True)
        if axis=="y":
            MOTOR = create_channel_device("PINK:SMA01:m9.VAL")
            MOTOR_RBV = create_channel_device("PINK:SMA01:m9.RBV")
            MOTOR_RBV.setMonitored(True)
            MOTOR_DMOV = create_channel_device("PINK:SMA01:m9.DMOV")
            MOTOR_DMOV.setMonitored(True)

        ## setup filename
        set_exec_pars(open=False, name="sample_scan_mythen", reset=True)

        ## save initial scan data
        save_dataset("scan/start_time", time.ctime())
        save_dataset("scan/type", "sample scan with mythen")

        ## configure scan positions
        positionarray = linspace(start, end, step)

        ## plot setup
        if axis=='x':
            ypos = '{:.1f}'.format(caget("PINK:SMA01:m9.RBV"))
            xlabel = 'X position'
            plottitle = 'Horizontal Sample Scan (Y='+ypos+')'
        else:
            ypos = '{:.1f}'.format(caget("PINK:SMA01:m10.RBV"))
            xlabel = 'Y position'
            plottitle = 'Vertical Sample Scan (X='+ypos+')'
        p1h=plot([None], [xlabel], title=plottitle)
        p1 = p1h.get(0)
        p1.getAxis(p1.AxisId.X).setRange(min(start, end),max(start,end))

        ## setup mythen
        caput("PINK:MYTHEN:cam1:AcquireTime", exposure)
        caput("PINK:MYTHEN:cam1:NumFrames", 1)
        # Mythen image mode 0:single 1:multiple
        caput("PINK:MYTHEN:cam1:ImageMode", 1)

        print("Scanning...")

        # saving pre scan position
        prescan_pos = MOTOR_RBV.read()

        ## Main loop
        for pos in positionarray:
            MOTOR.write(pos)
            MOTOR_RBV.waitValueInRange(pos, 1.0, 60000)
            MOTOR_DMOV.waitValueInRange(1, 0.5, 60000)
            Mythen_acquire.write(1)
            resp = SENSOR.waitCacheChange(1000*int(exposure+2))
            if resp==False:
                print("Timeout: No data from mythen")
                continue
            sensor.append(SENSOR.take())
            motor.append(MOTOR_RBV.take())
            p1.getSeries(0).setData(motor, sensor)

        ## Save data
        save_dataset("raw/sensor", sensor)
        save_dataset("raw/blade", motor)

        ## Save plot data
        save_dataset("plot/title", plottitle)
        save_dataset("plot/xlabel", "Position")
        save_dataset("plot/ylabel", "Counts per second")
        save_dataset("plot/x", motor)
        create_dataset("plot/y", 'd', False, (0, len(sensor)))
        append_dataset("plot/y", sensor)

        ## save data
        save_dataset("scan/finish_time", time.ctime())

        ## Move back to original position
        MOTOR.write(prescan_pos)
        MOTOR_RBV.waitValueInRange(pos, 1.0, 60000)
        MOTOR_DMOV.waitValueInRange(1, 0.5, 60000)

        print("Scan complete")
