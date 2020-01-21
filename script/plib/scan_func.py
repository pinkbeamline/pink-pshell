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

    def spot(self, detector, exposure=1, images=1, sample=''):
        if isinstance(detector, DETEC):
            print("!! Please use detector. to see list of detectors !!")
            return
        if detector=="ge":
            run("plib/scan/spot_ge.py")
            myscan = SPOTGE()
            myscan.scan(exposure, images, sample)
            del myscan
            print("OK")
            return
        if detector=="mythen":
            run("plib/scan/spot_mythen.py")
            myscan = SPOTMYTHEN()
            myscan.scan(exposure, images, sample)
            del myscan
            print("OK")
            return

    def line(self, detector):
        if isinstance(detector, DETEC):
            print("!! Please use detector. to see list of detectors !!")
            return
        print("Line scan " + detector)

    def zigzag(self, detector):
        if isinstance(detector, DETEC):
            print("!! Please use detector. to see list of detectors !!")
            return
        print("zigzag scan " + detector)

    def continuous(self, detector):
        if isinstance(detector, DETEC):
            print("!! Please use detector. to see list of detectors !!")
            return
        print("continuous scan " + detector)
