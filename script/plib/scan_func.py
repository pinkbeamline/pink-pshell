class SCANFUNC():
    def __init__(self):
        pass

############################################
### Blade scan
############################################

    def Blade__Diagnostic_Chamber(self, start=0, end=0, step=0, exposure=0.0):
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

    def Blade__Sample_Chamber(self, start=0, end=0, step=0, exposure=0.0):
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
        bladescan.run_sec_scan(start, end, step, exposure)
        print("OK")

############################################
### Gap scan
############################################

    def gap____without_fitting(self, start=0, end=0, step=0, exposure=0.0):
        run("plib/gap_scans.py")
        gap = GAPSCAN()
        gap.scan(start, end, step, exposure, fit=None)
        print("OK")
        
    def gap____linear_background(self, start=0, end=0, step=0, exposure=0.0):
        run("plib/gap_scans.py")
        gap = GAPSCAN()
        gap.scan(start, end, step, exposure, fit="linear")
        print("OK")

    def gap____exponential_background(self, start=0, end=0, step=0, exposure=0.0):
        run("plib/gap_scans.py")
        gap = GAPSCAN()
        gap.scan(start, end, step, exposure, fit="exp")
        print("OK")        