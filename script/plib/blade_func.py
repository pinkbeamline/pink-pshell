## blade scan
class BLADEFUNC():

    def Diagnostic_Chamber_Blade_Scan(self, start=0, end=0, step=0, exposure=0.0):
        """Blade scan on diagnostic chamber
        Args:
            start:    start position
              end:    end position
             step:    (int) number of steps or (float) step distance 
          latency:    settling time after position reached
        """
        ## Variables
        
        run("plib/blade_scan.py")
        bladescan = BLADESCAN()
        bladescan.run_diag_scan(start, end, step, exposure)
        print("OK")

    def Sample_Env__Blade_Scan(self, start=0, end=0, step=0, latency=0.0):
        """Blade scan on sample env chamber
        Args:
            start:    start position
              end:    end position
             step:    (int) number of steps or (float) step distance 
          latency:    settling time after position reached
        """
        ## Variables
        
        run("plib/blade_scan.py")
        bladescan = BLADESCAN()
        bladescan.run_sec_scan()
        print("OK")
