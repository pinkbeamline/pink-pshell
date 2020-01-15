## spot scan for greateyes
class SPOTGE():

    def scan(self, exposure, images, sample):
        print("spot scan for greateyes")

        ## variables
        DEBUG=0
        initial_frame = 0
        pass_id = 1
        GE_ROI_X = caget("PINK:GEYES:image3:ArraySize0_RBV")
        GE_ROI_Y = caget("PINK:GEYES:image3:ArraySize1_RBV")
        GE_X = caget("PINK:GEYES:image4:ArraySize0_RBV")
        GE_Y = caget("PINK:GEYES:image4:ArraySize1_RBV")
        data_compression = {"compression":"True", "shuffle":"True"}
        profile_size = 100

        ## create channels
        GE_acquire = create_channel_device("PINK:GEYES:cam1:Acquire", type='i')
        GE_status = create_channel_device("PINK:GEYES:cam1:DetectorState_RBV", type='i')
        GE_status.setMonitored(True)
        GE_frameID = create_channel_device("PINK:GEYES:cam1:ArrayCounter_RBV", type='d')
        GE_frameID.setMonitored(True)
        GE_raw_array = create_channel_device("PINK:GEYES:image1:ArrayData", type='[d', size=int(GE_X*GE_Y))
        GE_raw_array.setMonitored(True)
        GE_roi_array = create_channel_device("PINK:GEYES:image3:ArrayData", type='[d', size=int(GE_ROI_X*GE_ROI_Y))
        GE_roi_array.setMonitored(True)
        GE_Spectra = create_channel_device("PINK:GEYES:spectrum_RBV", type='[d', size=GE_X)
        GE_Spectra.setMonitored(True)
        GE_temperature = create_channel_device("PINK:GEYES:cam1:TemperatureActual", type='d')
        GE_temperature.setMonitored(True)
        TFY = create_channel_device("PINK:CAE1:Current2:MeanValue_RBV", type='d')
        TFY.setMonitored(True)
        TFY_profile = create_channel_device("PINK:CAE1:image2:ArrayData", type='[d', size=100)
        TFY_profile.setMonitored(True)
        IZero = create_channel_device("PINK:CAE2:SumAll:MeanValue_RBV", type='d')
        IZero.setMonitored(True)
        IZero_profile = create_channel_device("PINK:CAE2:image1:ArrayData", type='[d', size=100)
        IZero_profile.setMonitored(True)
        Frame_countdown = create_channel_device("PINK:AUX:countdown.VAL")
        Display_status = create_channel_device("PINK:AUX:ps_status")
        Progress = create_channel_device("PINK:GEYES:Scan:progress")
        
        ## Stop greateyes
        if GE_status.read():
            GE_acquire.write(0)
            if DEBUG: log("GE Stop", data_file = False)
            while(GE_status.read()):
                sleep(1)
            if DEBUG: log("GE Idle", data_file = False)

        ## setup filename
        set_exec_pars(open=False, name="ge", reset=True)

        ## save initial scan data
        save_dataset("scan/sample", sample)
        save_dataset("scan/start_time", time.ctime())
        save_dataset("scan/type", "spot")

        ## Update status data
        caput("PINK:AUX:ps_filename_RBV", self.get_filename())
        caput("PINK:AUX:ps_sample", sample) # Update sample name

        ## setup greateyes
        caput("PINK:GEYES:cam1:AcquireTime", exposure)
        caput("PINK:GEYES:cam1:ImageMode", 0) # single image

        ## setup caenels 1 and 2
        if DEBUG: log("Setup CAE1", data_file = False)
        caput("PINK:CAE1:AcquireMode", 0) ## continuous
        caput("PINK:CAE1:AveragingTime", exposure)
        caput("PINK:CAE1:ValuesPerRead", exposure*1000)
        caput("PINK:CAE1:TriggerMode", 1) ## ext trigger
        caputq("PINK:CAE1:Acquire", 1)

        if DEBUG: log("Setup CAE2", data_file = False)
        caput("PINK:CAE2:AcquireMode", 0) ## continuous
        caput("PINK:CAE2:AveragingTime", exposure)
        caput("PINK:CAE2:ValuesPerRead", exposure*1000)
        caput("PINK:CAE2:TriggerMode", 1) ## ext trigger
        caputq("PINK:CAE2:Acquire", 1)

        ## Setup delay generator
        ## (trigger mode, shutter, Mythen, Greateyes, Caenels)
        ## [trigger mode] [5:single shot] [1: Ext rising edge]
        self.setup_delaygen(5, [0, exposure-0.02], [0, 0], [0, 0], [0, 0.001])
        
        caput("PINK:GEYES:Scan:progress", 0) # Reset pass progress

        ## take GE background image
        self.save_GE_BG(exposure)

        ## Setup delay generator
        ## (trigger mode, shutter, Mythen, Greateyes, Caenels)
        ## [trigger mode] [5:single shot] [1: Ext rising edge]
        self.setup_delaygen(1, [0, exposure-0.02], [0, 0], [0, 0], [0, 0.001])

        caput("PINK:AUX:countdown.B", exposure) # setup frame countdown
        caput("PINK:GEYES:specsum_reset", 0) # clean spectrum sum
        caput("PINK:GEYES:specsum_reset", 1) # enable spectrum sum

        ## eta_calc(exposure, Ypoints, Xpoints, passes, linedelay)
        self.eta_calc(exposure, images, 1, 1, 0)

        initial_frame = GE_frameID.read()

        ## save pre scan data
        save_dataset("passes/pass01/d_ccd/raw/bg_image", Convert.reshape(GE_raw_array.read(), GE_Y, GE_X))
        save_dataset("passes/pass01/d_ccd/processed/bg_spectrum", GE_Spectra.read())

        ## create dataset 
        create_dataset("passes/pass01/d_ccd/raw/image", 'd', False, (0, GE_Y, GE_X), features=data_compression)
        create_dataset("passes/pass01/d_ccd/processed/image", 'd', False, (0, GE_ROI_Y, GE_ROI_X), features=data_compression)
        create_dataset("passes/pass01/d_ccd/processed/spectrum", 'd', False, (0, GE_ROI_X))
        create_dataset("passes/pass01/d_ccd/raw/temperature", 'd', False)
        create_dataset("passes/pass01/d_ccd/raw/frame_id", 'd', False)
        create_dataset("passes/pass01/station/izero_profile", 'd', False, (0, profile_size))
        create_dataset("passes/pass01/station/izero", 'd', False)
        create_dataset("passes/pass01/station/tfy_profile", 'd', False, (0, profile_size))
        create_dataset("passes/pass01/station/tfy", 'd', False)
        create_dataset("passes/pass01/timestamps", 'd', False)

        ## pressure dataset
        
        for i in range(int(images)):
            msgstr = "Frame " + str(i)
            Display_status.write(msgstr)
            Frame_countdown.write(100) # Initiate frame countdown
            GE_acquire.write(1)
            GE_raw_array.waitCacheChange(int((exposure*1000)+10000))
            sleep(0.01)
            ## append to dataset
            append_dataset("passes/pass01/d_ccd/raw/image", Convert.reshape(GE_raw_array.take(), GE_Y, GE_X))
            append_dataset("passes/pass01/d_ccd/processed/image", Convert.reshape(GE_roi_array.take(), GE_ROI_Y, GE_ROI_X))
            append_dataset("passes/pass01/d_ccd/processed/spectrum", GE_Spectra.take())
            append_dataset("passes/pass01/d_ccd/raw/temperature", GE_temperature.take())
            append_dataset("passes/pass01/d_ccd/raw/frame_id", GE_frameID.take())
            append_dataset("passes/pass01/station/izero_profile", IZero_profile.take())
            append_dataset("passes/pass01/station/izero", IZero.take())
            append_dataset("passes/pass01/station/tfy_profile", TFY_profile.take())
            append_dataset("passes/pass01/station/tfy", TFY.take())
            append_dataset("passes/pass01/timestamps", GE_frameID.getTimestampNanos())
            Progress.write(self.calc_progress(initial_frame, GE_frameID.take(), images))

        ## save after scan data
        save_dataset("scan/end_time", time.ctime())

    ################################################################################################
    ### GE save background image function
    def save_GE_BG(self, exposure):
        DEBUG=0
        if DEBUG: log("Saving GE background", data_file = False)
        caput("PINK:AUX:ps_status", "Acquiring background image")
        
        ## Stop GE acquisition
        if caget("PINK:GEYES:cam1:DetectorState_RBV", type='i'):
            caputq("PINK:GEYES:cam1:Acquire", 0)
            if DEBUG: log("GE Stop", data_file = False)
            while(caget("PINK:GEYES:cam1:DetectorState_RBV", type='i')):
                sleep(1)
            if DEBUG: log("GE Idle", data_file = False)

        caput("PINK:PLCGAS:ei_B01", 0) # Close fast shutter
        caput("PINK:GEYES:cam1:ImageMode", 0) # GE single image
        caput("PINK:AUX:countdown.B", exposure) # setup frame countdown
        caput("PINK:GEYES:Proc1:EnableBackground",0) #Disable GE BG Processing
        sleep(1)
        caput("PINK:AUX:countdown.VAL", 100) # Initiate frame countdown
        caput("PINK:GEYES:cam1:Acquire", 1) # acquire 1 image
        caput("PINK:GEYES:savebg", 1) # copy bg image to record
        caput("PINK:GEYES:Proc1:SaveBackground", 1) # save BG image into process record
        caput("PINK:GEYES:Proc1:EnableBackground",1) # Enable GE BG Processing
        caput("PINK:AUX:ps_status", "Background image OK")
        if DEBUG: log("Saving GE background OK", data_file = False)

    ### progress calculation
    def calc_progress(self, initial_frame, last_frame, images):
        progress = round(((last_frame-initial_frame)/images)*100.0)
        return progress

    ### ETA calculation
    def eta_calc(self, exposure, Ypoints, Xpoints, passes, linedelay):
        bgtime = 2.881 + exposure*1.087
        linetime = (Ypoints*(exposure+0.35))+1.7+linedelay
        passtime = (Xpoints * linetime) + bgtime
        scantime = passes*passtime
        tnow = time.time()
        passETA = time.ctime(tnow + passtime)
        scanETA = time.ctime(tnow + scantime)
        caput("PINK:AUX:pass_eta", passETA)
        caput("PINK:AUX:scan_eta", scanETA)

    def get_filename(self):
        execinfo=get_exec_pars()
        filenameinfo=execinfo.path
        filenameinfo=filenameinfo.split("/")
        fname=filenameinfo[-1]
        return fname

    ## (trigger mode, shutter, Mythen, Greateyes, Caenels)
    ## trigger [5:single shot] [1: Ext rising edge]
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
        