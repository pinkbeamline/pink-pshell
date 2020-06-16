## spot scan for eiger
class SPOTMYTHEN():

    def scan(self, exposure, images, sample):
        print("spot scan for mythen...")

        ## variables
        DEBUG=0
        initial_frame = 0
        pass_id = 1
        Mythen_X = caget("PINK:MYTHEN:cam1:SizeX_RBV")
        data_compression = {"compression":"True", "shuffle":"True"}
        profile_size = 100
        scan_abort = False
        tnow = 0

        ## create channels
        Mythen_acquire = create_channel_device("PINK:MYTHEN:cam1:Acquire", type='i')
        Mythen_status = create_channel_device("PINK:MYTHEN:cam1:Acquire_RBV", type='i')
        Mythen_status.setMonitored(True)
        Mythen_frameID = create_channel_device("PINK:MYTHEN:cam1:ArrayCounter_RBV", type='d')
        Mythen_frameID.setMonitored(True)
        Mythen_Spectra = create_channel_device("PINK:MYTHEN:RawInverted", type='[d', size=Mythen_X)
        Mythen_Spectra.setMonitored(True)
        Mythen_Spectra_sum = create_channel_device("PINK:MYTHEN:specsum_RBV", type='[d', size=Mythen_X)

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
        Ring_current = create_channel_device("MDIZ3T5G:current", type='d')
        Ring_current.setMonitored(True)
        Sec_el_x = create_channel_device("PINK:SMA01:m10.RBV", type='d')
        Sec_el_x.setMonitored(True)
        Sec_el_y = create_channel_device("PINK:SMA01:m9.RBV", type='d')
        Sec_el_y.setMonitored(True)

        ## create pressure channels
        run("config/pressure_devices.py")
        pdev = []
        for pd in pressure_pvlist:
            pvdesc = pd[1]+".DESC"
            pdev.append([pd[0], create_channel_device(pd[1], type='d'), caget(pvdesc)])
        for pd in pdev:
            pd[1].setMonitored(True)

        ## Clean status message
        Display_status.write(" ")

        ## Stop mythen
        if Mythen_status.read():
            Mythen_acquire.write(0)
            if DEBUG: log("Mythen Stop", data_file = False)
            while(Mythen_status.read()):
                sleep(1)
            if DEBUG: log("Mythen Idle", data_file = False)

        ## setup filename
        set_exec_pars(open=False, name="mythen", reset=True)

        ## save initial scan data
        save_dataset("scan/sample", sample)
        save_dataset("scan/start_time", time.ctime())
        save_dataset("scan/type", "spot")
        save_dataset("scan/num_passes", 1)
        save_dataset("scan/num_images_pass", images)

        ## save plot data
        save_dataset("plot/title", sample)
        save_dataset("plot/xlabel", "channel")
        save_dataset("plot/ylabel", "counts")
        plotx = linspace(1, Mythen_X, 1.0)
        save_dataset("plot/x", plotx)

        ## create plot dataset
        create_dataset("plot/y", 'd', False, (0, Mythen_X))
        create_dataset("plot/y_desc", 's', False)

        ## Saving detectors settings
        save_dataset("detector/mythen/exposure", exposure)
        save_dataset("detector/mythen/energy", caget("PINK:MYTHEN:cam1:BeamEnergy_RBV"))
        save_dataset("detector/mythen/threshold", caget("PINK:MYTHEN:cam1:ThresholdEnergy_RBV"))

        ## Update status data
        caput("PINK:AUX:ps_filename_RBV", self.get_filename())
        print("Filename: " + self.get_filename())
        caput("PINK:AUX:ps_sample", sample) # Update sample name
        caput("PINK:AUX:ps_sample2", array('b', str(sample))) # Update long sample name

        ## print some info
        print("******************************************************")
        print("    Scan: spot")
        print("Detector: Eiger")
        print("  Sample: " + sample)
        print("Filename: " + self.get_filename())
        print("Exposure: " + '{:.2f}'.format(float(exposure)) + " seconds")
        print("  Images: " + '{:02d}'.format(int(images)))
        print("******************************************************")

        ## setup mythen
        caput("PINK:MYTHEN:cam1:AcquireTime", exposure)
        caput("PINK:MYTHEN:cam1:NumFrames", images)
        # Mythen image mode 0:single 1:multiple
        caput("PINK:MYTHEN:cam1:ImageMode", 1)
        #caput("PINK:MYTHEN:cam1:DelayTime", 0.001)

        ## setup caenels 1 and 2
        if DEBUG: log("Setup CAE1", data_file = False)
        caput("PINK:CAE1:AcquireMode", 0) ## continuous
        caput("PINK:CAE1:Range", 1)
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
        self.setup_delaygen(1, [0, (images*exposure)-0.02], [0, 0], [0, 0], [0, 0])

        ## Setup trigger switch
        ## A=Delaygen Trigger Source [0:OFF, 1:CCD, 2:mythen, 3:eiger]
        ## B=Caenels Trigger Source [0:OFF, 1:Delaygen, 2:Output A]
        caput("PINK:RPISW:select_A", 2)
        caput("PINK:RPISW:select_B", 2)

        caput("PINK:GEYES:Scan:progress", 0) # Reset pass progress
        caput("PINK:AUX:countdown.B", exposure) # setup frame countdown
        caput("PINK:MYTHEN:specsum_enable", 0) # clean spectrum sum
        caput("PINK:MYTHEN:specsum_enable", 1) # enable spectrum sum

        Display_status.write("Spot scan running...")

        ## eta_calc(exposure, Ypoints, Xpoints, passes, linedelay)
        self.eta_calc(exposure, images, 1, 1, 0)

        initial_frame = Mythen_frameID.read()

        ## save pre scan data
        save_dataset("passes/pass01/positioners/sec_el_x", Sec_el_x.take())
        save_dataset("passes/pass01/positioners/sec_el_y", Sec_el_y.take())

        ## create dataset
        create_dataset("passes/pass01/detector/mythen/processed/spectrum", 'd', False, (0, Mythen_X))
        create_dataset("passes/pass01/detector/mythen/raw/frame_id", 'd', False)
        create_dataset("passes/pass01/station/izero_profile", 'd', False, (0, profile_size))
        create_dataset("passes/pass01/station/izero", 'd', False)
        create_dataset("passes/pass01/station/tfy_profile", 'd', False, (0, profile_size))
        create_dataset("passes/pass01/station/tfy", 'd', False)
        create_dataset("passes/pass01/station/ring_current", 'd', False)
        create_dataset("passes/pass01/timestamps", 'd', False)
        create_dataset("passes/pass01/timestamps_ps", 'd', False)
        ##create_dataset("passes/pass01/positioners/sec_el_x", 'd', False)
        ##create_dataset("passes/pass01/positioners/sec_el_y", 'd', False)

        ## create pressure dataset
        for pd in pdev:
            datasetpath = "passes/pass01/station/pressure/"+pd[0]
            create_dataset(datasetpath, 'd', False)
            set_attribute(datasetpath, "DESC", pd[2])

        ## start acquisition
        Mythen_acquire.write(1)
        try:
            for i in range(int(images)):
                Frame_countdown.write(100) # Initiate frame countdown
                Mythen_Spectra.waitCacheChange(int((exposure*1000)+30000))
                sleep(0.2)
                ## append to dataset
                append_dataset("passes/pass01/detector/mythen/processed/spectrum", Mythen_Spectra.take())
                append_dataset("passes/pass01/detector/mythen/raw/frame_id", Mythen_frameID.take())
                append_dataset("passes/pass01/station/izero_profile", IZero_profile.take())
                append_dataset("passes/pass01/station/izero", IZero.take())
                append_dataset("passes/pass01/station/tfy_profile", TFY_profile.take())
                append_dataset("passes/pass01/station/tfy", TFY.take())
                append_dataset("passes/pass01/station/ring_current", Ring_current.take())
                append_dataset("passes/pass01/timestamps", Mythen_frameID.getTimestampNanos())
                append_dataset("passes/pass01/timestamps_ps", time.time()*1e9)
                ##append_dataset("passes/pass01/positioners/sec_el_x", Sec_el_x.take())
                ##append_dataset("passes/pass01/positioners/sec_el_y", Sec_el_y.take())
                ## append to pressure devices
                for pd in pdev:
                    datasetpath = "passes/pass01/station/pressure/"+pd[0]
                    append_dataset(datasetpath, pd[1].take())

                Progress.write(self.calc_progress(initial_frame, Mythen_frameID.take(), images))
        except:
            tnow = time.ctime()
            scan_abort = True
            print("scan aborted [ " + tnow + " ]")

        ## save after scan data
        save_dataset("passes/pass01/detector/mythen/processed/spectrum_sum", Mythen_Spectra_sum.read())
        save_dataset("detector/mythen/processed/spectrum_sum", Mythen_Spectra_sum.read())

        ## save plot data
        append_dataset("plot/y", Mythen_Spectra_sum.read())
        append_dataset("plot/y_desc", "Pass 0")

        ## save spec filename
        self.save_specfile(pass_id, extrafname="", spectrum=Mythen_Spectra_sum.take())

        ## stop detectors
        Mythen_acquire.write(0)

        ## save beamline/station snapshot
        pink_save_bl_snapshot()

        ## save final scan time
        save_dataset("scan/end_time", time.ctime())

        ## Setup delay generator
        ## (trigger mode, shutter, Mythen, Greateyes, Caenels)
        ## [trigger mode] [5:single shot] [1: Ext rising edge]
        self.setup_delaygen(5, [0, 0], [0, 0], [0, 0], [0, 0])

        if scan_abort:
            Display_status.write("scan aborted - " + tnow)
            save_dataset("scan/status", "aborted")
        else:
            Display_status.write("Spot scan completed. OK")
            save_dataset("scan/status", "ok")
            print("Spot scan completed. OK")

    ################################################################################################

    ### progress calculation
    def calc_progress(self, initial_frame, last_frame, images):
        progress = round(((last_frame-initial_frame)/images)*100.0)
        return progress

    ### ETA calculation
    def eta_calc(self, exposure, Ypoints, Xpoints, passes, linedelay):
        bgtime = 0
        linetime = (Ypoints*(exposure+0.001))+1.7+linedelay
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

    def save_specfile(self, passid, extrafname="", spectrum=[]):
        try:
            datafilepath = get_exec_pars().getPath()
            fpath = datafilepath.split("/")
            fpath = datafilepath.split(fpath[-1])
            fpath = fpath[0]+"mca"
            if os.path.isdir(fpath) == False:
                os.mkdir(fpath)
            specfname = datafilepath.split("/")[-1].split(".h5")[0]+extrafname+".mca"
            specfname = fpath+"/"+specfname
            spectext = []
            spectext.append("#S "+'{:d}'.format(int(passid))+" pass"+'{:03d}'.format(int(passid))+'\n')
            spectext.append("#N 1\n")
            spectext.append("#L Counts\n")
            for ct in spectrum:
                spectext.append('{:d}'.format(int(ct))+'\n')
            spectext.append("\n")
            fspec = open(specfname, 'a+')
            for lines in spectext:
                fspec.write(lines)
            fspec.close()
        except:
            print("[Error]: Failed to create mca file")
