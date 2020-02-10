## continuous scan for eiger
class CONTMYTHEN():

    def scan(self, det_exposure, sample_exposure, X0, X1, dX, Y0, Y1, passes, sample, linedelay):
        print("Continuous scan for mythen...")
        
        ## variables
        DEBUG=0
        initial_frame = 0
        pass_id = 1
        Mythen_X = caget("PINK:MYTHEN:cam1:SizeX_RBV")
        data_compression = {"compression":"True", "shuffle":"True"}
        profile_size = 100
        scan_abort = False
        tnow = 0
        scan_dir=1

        ## parameter calculations
        ## assuming a beam of vertical size = 50um
        sample_speed = 50.0/sample_exposure
        x_positions = linspace(X0, X1, float(dX))
        num_lines = len(x_positions)
        if det_exposure == "auto" or det_exposure=="AUTO":
            images_per_line = 1
            det_exposure = ((abs(Y1-Y0))/sample_speed)-0.1
        else:
            images_per_line = math.floor((abs(Y1-Y0)/sample_speed)/(det_exposure+0.001))
        sample_l = images_per_line*(det_exposure+0.001)*sample_speed
        effic = sample_l/(abs(Y1-Y0))

        Xpoints = num_lines
        Ypoints = images_per_line
        exposure = det_exposure

        print("******************************************* ")
        print("                    Scan:  continuous")
        print("                Detector:  Eiger")
        print("            Sample speed:  " + '{:.1f}'.format(sample_speed) + " um/s")
        print("Number of vertical lines:  " + '{:d}'.format(num_lines))
        print("          Images p/ line:  " + '{:d}'.format(int(images_per_line)))
        print("       Detector exposure:  " + '{:.1f}'.format(det_exposure) + " seconds")
        print("         Sample exposure:  " + '{:.1f}'.format(sample_exposure) + " seconds")
        #print(" Sample usage efficiency:  " + '{:.1f}'.format(effic*100)+" %")
        print("******************************************* ")
        print(" ")

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
        ### positioners
        ## sec el x
        Sec_el_x = create_channel_device("PINK:SMA01:m10.VAL", type='d')
        Sec_el_x_RBV = create_channel_device("PINK:SMA01:m10.RBV", type='d')
        Sec_el_x_RBV.setMonitored(True)
        Sec_el_x_DMOV = create_channel_device("PINK:SMA01:m10.DMOV", type='d')
        Sec_el_x_DMOV.setMonitored(True)
        ## sec el y
        Sec_el_y = create_channel_device("PINK:SMA01:m9.VAL", type='d')
        Sec_el_y_RBV = create_channel_device("PINK:SMA01:m9.RBV", type='d')
        Sec_el_y_RBV.setMonitored(True)
        Sec_el_y_DMOV = create_channel_device("PINK:SMA01:m9.DMOV", type='d')
        Sec_el_y_DMOV.setMonitored(True)
        Sec_el_y_VELO = create_channel_device("PINK:SMA01:m9.VELO", type='d')
        Sec_el_y_STOP = create_channel_device("PINK:SMA01:m9.STOP", type='d')

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
        save_dataset("scan/type", "continuous")
        save_dataset("scan/num_passes", passes)
        save_dataset("scan/num_images_pass", Xpoints*Ypoints)
        save_dataset("scan/sample_speed", sample_speed)
        save_dataset("scan/sample_exposure", sample_exposure)
        save_dataset("scan/vert_lines", Xpoints)
        save_dataset("scan/images_per_line", Ypoints)

        ## Saving detectors settings
        save_dataset("detector/d_mythen/exposure", exposure)
        save_dataset("detector/d_mythen/energy", caget("PINK:MYTHEN:cam1:BeamEnergy_RBV"))
        save_dataset("detector/d_mythen/threshold", caget("PINK:MYTHEN:cam1:ThresholdEnergy_RBV"))

        ## Update status data
        caput("PINK:AUX:ps_filename_RBV", self.get_filename())
        caput("PINK:AUX:ps_sample", sample) # Update sample name
        caput("PINK:AUX:ps_sample2", array('b', str(sample))) # Update long sample name

        ## setup mythen
        caput("PINK:MYTHEN:cam1:AcquireTime", exposure)
        caput("PINK:MYTHEN:cam1:NumFrames", Ypoints)
        # Mythen image mode 0:single 1:multiple
        caput("PINK:MYTHEN:cam1:ImageMode", 1)

        ## setup caenels 1 and 2
        if DEBUG: log("Setup CAE1", data_file = False)
        caput("PINK:CAE1:AcquireMode", 0) ## continuous
        caput("PINK:CAE1:Range", 1) ## 0: mA / 1: uA
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
        self.setup_delaygen(1, [0, ((exposure+0.001)*Ypoints)-0.02], [0, 0], [0, 0], [0, 0])

        ## create dataset for pass spectrum for eiger
        create_dataset("detector/d_mythen/processed/spectrum_sum", 'd', False, (0, Mythen_X))

        try:
            ### Pass loop
            while pass_id <= passes:
                passpath = "pass"+'{:02d}'.format(pass_id)
                scan_dir=1

                caput("PINK:GEYES:Scan:progress", 0) # Reset pass progress
                caput("PINK:AUX:countdown.B", exposure) # setup frame countdown
                caput("PINK:MYTHEN:specsum_enable", 0) # clean spectrum sum
                caput("PINK:MYTHEN:specsum_enable", 1) # enable spectrum sum

                Display_status.write("Continuous scan pass "+ '{:02d}'.format(pass_id) +" / "+ '{:02d}'.format(passes))

                ##   eta_calc(exposure, Ypoints, Xpoints, passes, linedelay)
                self.eta_calc(exposure, Ypoints, Xpoints, (1+passes-pass_id), linedelay)

                initial_frame = Mythen_frameID.read()

                ## create dataset for passes
                create_dataset("passes/"+passpath+"/detector/d_mythen/processed/spectrum", 'd', False, (0, Mythen_X))
                create_dataset("passes/"+passpath+"/detector/d_mythen/raw/frame_id", 'd', False)
                create_dataset("passes/"+passpath+"/station/izero_profile", 'd', False, (0, profile_size))
                create_dataset("passes/"+passpath+"/station/izero", 'd', False)
                create_dataset("passes/"+passpath+"/station/tfy_profile", 'd', False, (0, profile_size))
                create_dataset("passes/"+passpath+"/station/tfy", 'd', False)
                create_dataset("passes/"+passpath+"/station/ring_current", 'd', False)
                create_dataset("passes/"+passpath+"/timestamps", 'd', False)
                create_dataset("passes/"+passpath+"/positioners/sec_el_x", 'd', False)
                create_dataset("passes/"+passpath+"/positioners/sec_el_y", 'd', False)

                ## create pressure dataset
                for pd in pdev:
                    datasetpath = "passes/"+passpath+"/station/pressure/"+pd[0]
                    create_dataset(datasetpath, 'd', False)
                    set_attribute(datasetpath, "DESC", pd[2])

                ## Move Sec_el_y to start position
                Sec_el_y_VELO.write(20000)
                Sec_el_y.write(Y0)
                Sec_el_y_RBV.waitValueInRange(Y0, 1, 60000)
                Sec_el_y_DMOV.waitValueInRange(1, 0.1, 60000)

                ## Line loop
                for xpos in x_positions:
                    Sec_el_x.write(xpos)
                    Sec_el_x_RBV.waitValueInRange(xpos, 1, 60000)
                    Sec_el_x_DMOV.waitValueInRange(1, 0.1, 60000)

                    if(scan_dir):
                        ydest = float(Y1)
                    else:
                        ydest = float(Y0)

                    Sec_el_y_VELO.write(sample_speed)
                    Sec_el_y.write(ydest)
                    Mythen_acquire.write(1)

                    ## spot loop
                    for point_id in range(int(Ypoints)):
                        append_dataset("passes/"+passpath+"/positioners/sec_el_x", Sec_el_x_RBV.take())
                        append_dataset("passes/"+passpath+"/positioners/sec_el_y", Sec_el_y_RBV.take())
                        Frame_countdown.write(100) # Initiate frame countdown
                        Mythen_Spectra.waitCacheChange(int((exposure*1000)+10000))
                        sleep(0.1)
                        ## append to dataset
                        append_dataset("passes/"+passpath+"/detector/d_mythen/processed/spectrum", Mythen_Spectra.take())
                        append_dataset("passes/"+passpath+"/detector/d_mythen/raw/frame_id", Mythen_frameID.take())
                        append_dataset("passes/"+passpath+"/station/izero_profile", IZero_profile.take())
                        append_dataset("passes/"+passpath+"/station/izero", IZero.take())
                        append_dataset("passes/"+passpath+"/station/tfy_profile", TFY_profile.take())
                        append_dataset("passes/"+passpath+"/station/tfy", TFY.take())
                        append_dataset("passes/"+passpath+"/station/ring_current", Ring_current.take())
                        append_dataset("passes/"+passpath+"/timestamps", Mythen_frameID.getTimestampNanos())
                        append_dataset("passes/"+passpath+"/positioners/sec_el_x", Sec_el_x_RBV.take())
                        append_dataset("passes/"+passpath+"/positioners/sec_el_y", Sec_el_y_RBV.take())
                        ## append to pressure devices
                        for pd in pdev:
                            datasetpath = "passes/"+passpath+"/station/pressure/"+pd[0]
                            append_dataset(datasetpath, pd[1].take())

                        Progress.write(self.calc_progress(initial_frame, Mythen_frameID.take(), Xpoints*Ypoints))
                        ## end of spot loop

                    ## Move Sec_el_y to dest position
                    Sec_el_y_STOP.write(1)
                    sleep(0.25)
                    Sec_el_y_VELO.write(20000)
                    sleep(0.25)
                    Sec_el_y.write(ydest)
                    Sec_el_y_RBV.waitValueInRange(ydest, 1, 60000)
                    Sec_el_y_DMOV.waitValueInRange(1, 0.1, 60000)

                    scan_dir = abs(scan_dir-1)
                    sleep(linedelay)
                    ## end of line loop

                ## save after scan data
                save_dataset("passes/"+passpath+"/detector/d_mythen/processed/spectrum_sum", Mythen_Spectra_sum.read())

                ## save after pass data
                append_dataset("detector/d_mythen/processed/spectrum_sum", Mythen_Spectra_sum.take())

                ## save spec filename
                self.save_specfile(pass_id, extrafname="", spectrum=Mythen_Spectra_sum.take())

                ## increment pass counter
                pass_id = pass_id+1

                ## end of pass loop

        except:
            tnow = time.ctime()
            scan_abort = True
            print("scan aborted [ " + tnow + " ]")
            ## save the current spectrum sum
            save_dataset("passes/"+passpath+"/detector/d_mythen/processed/spectrum_sum", Mythen_Spectra_sum.read())
            append_dataset("detector/d_mythen/processed/spectrum_sum", Mythen_Spectra_sum.take())

        ## save beamline/station snapshot
        Display_status.write("Saving beamline snapshot...")
        run("config/bl_snapshot_config.py")
        for spdev in snapshot_pvlist:
            save_dataset(spdev[0], caget(spdev[1]))

        ## setup Sec_el_y
        Sec_el_y_STOP.write(1)
        sleep(0.1)
        Sec_el_y_VELO.write(20000)

        ## Setup delay generator
        ## (trigger mode, shutter, Mythen, Greateyes, Caenels)
        ## [trigger mode] [5:single shot] [1: Ext rising edge]
        self.setup_delaygen(5, [0, 0], [0, 0], [0, 0], [0, 0])

        ## Stop mythen
        if Mythen_status.read():
            Mythen_acquire.write(0)
            if DEBUG: log("Mythen Stop", data_file = False)
            while(Mythen_status.read()):
                sleep(1)
            if DEBUG: log("Mythen Idle", data_file = False)

        ## save final scan time
        save_dataset("scan/end_time", time.ctime())

        if scan_abort:
            Display_status.write("scan aborted - " + tnow)
            save_dataset("scan/status", "aborted")
        else:
            Display_status.write("Continuous scan completed. OK")
            print("Continuous scan completed.")

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
