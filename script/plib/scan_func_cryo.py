# ## Scan functions
# class DETEC():
#     def greateyes(self):
#         return "ge"
#     def eiger(self):
#         return "eiger"
#     def mythen(self):
#         return "mythen"
# #    def greateyes_eiger(self):
# #        return "ge+eiger"
# #    def greateyes_mythen(self):
# #        return "ge+mythen"
#
# class FILTERS():
#     def filter_1(self):
#         return "f1"
#     def filter_2(self):
#         return "f2"
#     def filter_3(self):
#         return "f3"
#     def scatter(self):
#         return "sc"
#
# class SOURCES():
#     def IZero(self):
#         return "izero"
#     def direct_diode_SEC(self):
#         return "sec"
#     def direct_diode_diag(self):
#         return "diag"
# #    def BPM3_ROI_Sum(self):
# #        return "bpm3"
#     def TFY(self):
#         return "tfy"
#
# class SAMPLEAXIS():
#     def horizontal(self):
#         return "x"
#     def vertical(self):
#         return "y"

class SCANFUNCRYO():

    def spot(self, detector, exposure=1, images=1, sample=""):
        if isinstance(detector, DETEC):
            print("!! Please use detector[dot] to see list of detectors !!")
            return

        if detector=="eiger":
            run("plib/scan/spot_eiger_cryo.py")
            myscan = SPOTEIGER()
            myscan.scan(exposure, images, sample)
            del myscan
            print("OK")
            return
        # elif detector=="ge":
        #     run("plib/scan/spot_ge.py")
        #     myscan = SPOTGE()
        #     myscan.scan(exposure, images, sample)
        #     del myscan
        #     print("OK")
        #     return
        # elif detector=="mythen":
        #     run("plib/scan/spot_mythen.py")
        #     myscan = SPOTMYTHEN()
        #     myscan.scan(exposure, images, sample)
        #     del myscan
        #     print("OK")
        #     return
        else:
            print("Not yet coded")

    # def line(self, detector, exposure=1, Y0=0, dY=100, Ypoints=1, passes=1, sample=""):
    #     if isinstance(detector, DETEC):
    #         print("!! Please use detector. to see list of detectors !!")
    #         return
    #     if detector=="ge":
    #         run("plib/scan/line_ge.py")
    #         myscan = LINEGE()
    #         myscan.scan(exposure, Y0, dY, Ypoints, passes, sample)
    #         del myscan
    #         print("OK")
    #         return
    #     if detector=="eiger":
    #         run("plib/scan/line_eiger.py")
    #         myscan = LINEEIGER()
    #         myscan.scan(exposure, Y0, dY, Ypoints, passes, sample)
    #         del myscan
    #         print("OK")
    #         return
    #     if detector=="mythen":
    #         run("plib/scan/line_mythen.py")
    #         myscan = LINEMYTHEN()
    #         myscan.scan(exposure, Y0, dY, Ypoints, passes, sample)
    #         del myscan
    #         print("OK")
    #         return
    #     else:
    #         print("Not yet coded")

    def zigzag_absolute(self, detector, exposure=1, X0=0, dX=100, Xpoints=1, Y0=0, dY=100, Ypoints=1, passes=1, sample="", linedelay=0):
        if isinstance(detector, DETEC):
            print("!! Please use detector. to see list of detectors !!")
            return
        if detector=="eiger":
            run("plib/scan/zigzag_eiger_cryo_abs.py")
            myscan = ZIGZAGEIGER()
            myscan.scan(exposure, X0, dX, Xpoints, Y0, dY, Ypoints, passes, sample, linedelay)
            del myscan
            print("OK")
            return
        # if detector=="ge":
        #     run("plib/scan/zigzag_ge.py")
        #     myscan = ZIGZAGGE()
        #     myscan.scan(exposure, X0, dX, Xpoints, Y0, dY, Ypoints, passes, sample, linedelay)
        #     del myscan
        #     print("OK")
        #     return
        # if detector=="eiger":
        #     if(get_setting("chamber")=="cryo"):
        #         run("plib/scan/zigzag_eiger_cryo.py")
        #     else:
        #         run("plib/scan/zigzag_eiger.py")
        #     myscan = ZIGZAGEIGER()
        #     myscan.scan(exposure, X0, dX, Xpoints, Y0, dY, Ypoints, passes, sample, linedelay)
        #     del myscan
        #     print("OK")
        #     return
        # if detector=="mythen":
        #     run("plib/scan/zigzag_mythen.py")
        #     myscan = ZIGZAGMYTHEN()
        #     myscan.scan(exposure, X0, dX, Xpoints, Y0, dY, Ypoints, passes, sample, linedelay)
        #     del myscan
        #     print("OK")
        #     return
        else:
            print("Not yet coded")

    def zigzag_relative(self, detector, exposure=1, X0=0, dX=100, Xpoints=1, Y0=0, dY=100, Ypoints=1, passes=1, sample="", linedelay=0):
        if isinstance(detector, DETEC):
            print("!! Please use detector. to see list of detectors !!")
            return
        if detector=="eiger":
            run("plib/scan/zigzag_eiger_cryo_rel.py")
            myscan = ZIGZAGEIGER()
            myscan.scan(exposure, X0, dX, Xpoints, Y0, dY, Ypoints, passes, sample, linedelay)
            del myscan
            print("OK")
            return
        else:
            print("Not yet coded")

    # def continuous(self, detector, det_exposure=1, sample_exposure=1, X0=0, X1=1000, dX=500, Y0=0, Y1=1000, passes=1, sample="", linedelay=0):
    #     if isinstance(detector, DETEC):
    #         print("!! Please use detector. to see list of detectors !!")
    #         return
    #     if detector=="ge":
    #         run("plib/scan/continuous_ge.py")
    #         myscan = CONTGE()
    #         myscan.scan(det_exposure, sample_exposure, X0, X1, dX, Y0, Y1, passes, sample, linedelay)
    #         del myscan
    #         print("OK")
    #         return
    #     if detector=="eiger":
    #         #if(get_setting("chamber")=="cryo"):
    #         #    run("plib/scan/continuous_eiger_cryo.py")
    #         #else:
    #         run("plib/scan/continuous_eiger.py")
    #         myscan = CONTEIGER()
    #         myscan.scan(det_exposure, sample_exposure, X0, X1, dX, Y0, Y1, passes, sample, linedelay)
    #         del myscan
    #         print("OK")
    #         return
    #     if detector=="mythen":
    #         run("plib/scan/continuous_mythen.py")
    #         myscan = CONTMYTHEN()
    #         myscan.scan(det_exposure, sample_exposure, X0, X1, dX, Y0, Y1, passes, sample, linedelay)
    #         del myscan
    #         print("OK")
    #         return
    #     else:
    #         print("Not yet coded")

    def filter_scan(self, filters, start=0, end=0, step=0, exposure=1):
        if isinstance(filters, FILTERS):
            print("!! Please use filters. to see list of options !!")
            return
        run("plib/scan/filter_scan.py")
        filterscan = FILTERSCAN()
        filterscan.scan(filters,start,end,step,exposure)
        del filterscan

    def gap(self, source, start=0, end=0, step=0, exposure=1):
        if isinstance(source, SOURCES):
            print("!! Please use source. to see list of options !!")
            return
        run("plib/gap_scans.py")
        gapscan = GAPSCAN()
        gapscan.scan(source, start=start, end=end, step=step, exposure=exposure, fit=False)
        del gapscan

    def sample_scan(self, axis, detector, start=0, end=0, step=0, exposure=1):
        if isinstance(axis, SAMPLEAXIS):
            print('!! Please use "axis." to see list of options !!')
            return
        if isinstance(detector, DETEC):
            print('!! Please use "detector." to see list of detectors !!')
            return
    #     if detector=="mythen":
    #         run("plib/scan/sample_scan_mythen.py")
    #         samplescan = SAMPLESCAN()
    #         samplescan.scan(axis=axis, start=start, end=end, step=step, exposure=exposure)
    #         del samplescan
    #         return
        if detector=="eiger":
            run("plib/scan/sample_scan_eiger_cryo.py")
            samplescan = SAMPLESCAN()
            samplescan.scan(axis=axis, start=start, end=end, step=step, exposure=exposure)
            del samplescan
            return
    #     if detector=="ge":
    #         run("plib/scan/sample_scan_ge.py")
    #         samplescan = SAMPLESCAN()
    #         samplescan.scan(axis=axis, start=start, end=end, step=step, exposure=exposure)
    #         del samplescan
    #         return
        else:
            print("Not available")
        return
