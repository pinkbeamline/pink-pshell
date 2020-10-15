class SIMFUNC():
    def spot(self, detector, exposure=1, images=1, sample=''):
        if isinstance(detector, DETEC):
            #print("Warning: detector not defined.")
            simdetector="not defined"
        else:
            simdetector=detector

        scantimestr = self.__scantime_calc(exposure=exposure, Ypoints=images, Xpoints=1, passes=1, linedelay=0)

        elab_det = ""
        if simdetector=="eiger":
            elab_det = ".eiger()"
        elif simdetector=="ge":
            elab_det = ".greateyes()"
        elif simdetector=="mythen":
            elab_det = ".mythen()"
        else:
            elab_det = ""
        #elab.put("[Cmd] sim.spot(detector{}, exposure={}, images={}, sample='{}')".format(elab_det, exposure, images, sample))

        ## print some info
        print("******************************************************")
        print("              Filename: Simulation ")
        print("                Sample: " + sample)
        print("             Scan type: spot")
        print("              Detector: " + simdetector)
        print("              Exposure: " + '{:.2f}'.format(float(exposure)) + " seconds")
        print("                Images: " + '{:02d}'.format(int(images)))
        print(" Total sample exposure: " + '{:.2f}'.format(exposure*images) + " seconds")
        print("       Total scan time: " + scantimestr)
        print("******************************************************")

    def continuous(self, detector, det_exposure=1, sample_exposure=1, X0=0, X1=1000, dX=500, Y0=0, Y1=1000, passes=1, sample='', linedelay=0):
        if isinstance(detector, DETEC):
            #print("Warning: detector not defined.")
            simdetector="not defined"
        else:
            simdetector=detector

        elab_det = ""
        if simdetector=="eiger":
            elab_det = ".eiger()"
        elif simdetector=="ge":
            elab_det = ".greateyes()"
        elif simdetector=="mythen":
            elab_det = ".mythen()"
        else:
            elab_det = ""
        #elab.put("[Cmd] sim.continuous(detector{}, det_exposure={}, sample_exposure={}, X0={}, X1={}, dX={}, Y0={}, Y1={}, passes={}, sample='{}', linedelay={})".format(elab_det, det_exposure, sample_exposure, X0, X1, dX, Y0, Y1, passes, sample, linedelay))

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

        scantimestr = self.__scantime_calc(exposure=exposure, Ypoints=Ypoints, Xpoints=Xpoints, passes=passes, linedelay=linedelay)

        print("******************************************* ")
        print("                  Filename:  Simulation")
        print("                    Sample:  " + sample)
        print("                 Scan type:  continuous")
        print("                  Detector:  " + simdetector)
        print("              Sample speed:  " + '{:.1f}'.format(sample_speed) + " um/s")
        print("  Number of vertical lines:  " + '{:d}'.format(num_lines))
        print("Position of vertical lines:  " + str(x_positions))
        print("            Images p/ line:  " + '{:d}'.format(int(images_per_line)))
        print("          Number of passes:  " + '{:d}'.format(int(passes)))
        print("         Detector exposure:  " + '{:.1f}'.format(det_exposure) + " seconds")
        print("  Sample exposure per pass:  " + '{:.2f}'.format(sample_exposure) + " seconds")
        print("     Total sample exposure:  " + '{:.2f}'.format(sample_exposure*passes) + " seconds")
        print("           Total scan time:  " + scantimestr)
        #print(" Sample usage efficiency:  " + '{:.1f}'.format(effic*100)+" %")
        print("******************************************* ")
        return

    def __scantime_calc(self, exposure=0, Ypoints=0, Xpoints=0, passes=0, linedelay=0):
        ## eiger
        bgtime = 0
        linetime = (Ypoints*(exposure+0.001))+1.7+linedelay
        passtime = (Xpoints * linetime) + bgtime
        scantime = round(passes*passtime)
        sh = int(scantime/3600.0)
        sm = int(scantime/60)%60
        ss = int(scantime%60)
        if sh>0:
            SH = "{:02d}h ".format(sh)
        else:
            SH = ""
        if sm>0:
            SM = "{:02d}m ".format(sm)
        else:
            SM = ""
        if ss>0:
            SS = "{:02d}s ".format(ss)
        else:
            SS = ""
        msg = SH + SM + SS
        return msg
