## Scan functions
class DETEC():
    def greateyes(self):
        return "ge"
    def eiger(self):
        return "eiger"
    def mythen(self):
        return "mythen"
    def greateyes_eiger(self):
        return "ge+eiger"
    def greateyes_mythen(self):
        return "ge+mythen"

class SCANFUNC():

    def spot(self, detector, exposure=1, images=1, sample=""):
        if isinstance(detector, DETEC):
            print("!! Please use detector[dot] to see list of detectors !!")
            return
        if detector=="ge":
            run("plib/scan/spot_ge.py")
            myscan = SPOTGE()
            myscan.scan(exposure, images, sample)
            del myscan
            print("OK")
            return
        elif detector=="mythen":
            run("plib/scan/spot_mythen.py")
            myscan = SPOTMYTHEN()
            myscan.scan(exposure, images, sample)
            del myscan
            print("OK")
            return
        elif detector=="eiger":
            run("plib/scan/spot_eiger.py")
            myscan = SPOTEIGER()
            myscan.scan(exposure, images, sample)
            del myscan
            print("OK")
            return
        else:
            print("Not yet coded")

    def line(self, detector, exposure=1, Y0=0, dY=100, Ypoints=1, passes=1, sample=""):
        if isinstance(detector, DETEC):
            print("!! Please use detector. to see list of detectors !!")
            return
        if detector=="ge":
            run("plib/scan/line_ge.py")
            myscan = LINEGE()
            myscan.scan(exposure, Y0, dY, Ypoints, passes, sample)
            del myscan
            print("OK")
            return
        if detector=="eiger":
            run("plib/scan/line_eiger.py")
            myscan = LINEEIGER()
            myscan.scan(exposure, Y0, dY, Ypoints, passes, sample)
            del myscan
            print("OK")
            return
        if detector=="mythen":
            run("plib/scan/line_mythen.py")
            myscan = LINEMYTHEN()
            myscan.scan(exposure, Y0, dY, Ypoints, passes, sample)
            del myscan
            print("OK")
            return
        else:
            print("Not yet coded")

    def zigzag(self, detector, exposure=1, X0=0, dX=100, Xpoints=1, Y0=0, dY=100, Ypoints=1, passes=1, sample="", linedelay=0):
        if isinstance(detector, DETEC):
            print("!! Please use detector. to see list of detectors !!")
            return
        if detector=="ge":
            run("plib/scan/zigzag_ge.py")
            myscan = ZIGZAGGE()
            myscan.scan(exposure, X0, dX, Xpoints, Y0, dY, Ypoints, passes, sample, linedelay)
            del myscan
            print("OK")
            return
        if detector=="eiger":
            run("plib/scan/zigzag_eiger.py")
            myscan = ZIGZAGEIGER()
            myscan.scan(exposure, X0, dX, Xpoints, Y0, dY, Ypoints, passes, sample, linedelay)
            del myscan
            print("OK")
            return
        else:
            print("Not yet coded")

    def continuous(self, detector, det_exposure=1, sample_exposure=1, X0=0, X1=1000, dX=500, Y0=0, Y1=1000, passes=1, sample="", linedelay=0):
        if isinstance(detector, DETEC):
            print("!! Please use detector. to see list of detectors !!")
            return
        if detector=="ge":
            run("plib/scan/continuous_ge.py")
            myscan = CONTGE()
            myscan.scan(det_exposure, sample_exposure, X0, X1, dX, Y0, Y1, passes, sample, linedelay)
            del myscan
            print("OK")
            return
        if detector=="eiger":
            run("plib/scan/continuous_eiger.py")
            myscan = CONTEIGER()
            myscan.scan(det_exposure, sample_exposure, X0, X1, dX, Y0, Y1, passes, sample, linedelay)
            del myscan
            print("OK")
            return
        else:
            print("Not yet coded")
