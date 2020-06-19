## blade scan
class BLADEFUNC():

    def Diagnostic_Chamber_Blade_Scan(self, start=0, end=0, step=0, exposure=0.0):
        """Blade scan on diagnostic chamber
        Args:
            start:    start position
              end:    end position
             step:    (int) number of steps or (float) step distance
         exposure:    settling time after position reached
        """
        ## Variables

        run("plib/blade_scan.py")
        bladescan = BLADESCAN()
        bladescan.run_diag_scan(start, end, step, exposure)
        print("OK")

    def Sample_Env_Blade_Scan(self, source, axis, start=0, end=0, step=0, exposure=0.0):
        if isinstance(source, SOURCES):
            print("!! Please use sensor[dot] to see list of available sensors !!")
            return
        if isinstance(axis, SAMPLEAXIS):
            print("!! Please use axis[dot] to see list of available axis !!")
            return
        """Blade scan on sample env chamber
        Args:
            start:    start position
              end:    end position
             step:    (int) number of steps or (float) step distance
         exposure:    settling time after position reached
        """
        ## Variables

        run("plib/blade_scan.py")
        bladescan = BLADESCAN()
        bladescan.run_sec_scan(source, axis, start, end, step, exposure)
        print("OK")

    def Slit_Scan(self, slit, start=0, end=0, step=0, exposure=0.0):
        if isinstance(slit, SLITS):
            print("!! Please use slit[dot] to see list of available slits !!")
            return
        run("plib/scan/slit_scan.py")
        slitscan = SLITSCAN()
        slitscan.scan(slit,start,end,step,exposure)


class SLITS():
    def bottom(self):
        return "bottom"
    def top(self):
        return "top"
    def left(self):
        return "left"
    def right(self):
        return "right"
