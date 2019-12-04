## blade scan
class BLADESCAN():
        def __init__(self):
            pass
        
        def run_diag_scan(self, start=0, end=0, steps=0, exposure=0):
            if exposure == 0:
                print("Abort: exposure = 0 ")
                return
                
            ## channels
            DSUM = create_channel_device("PINK:CAE2:SumAll:MeanValue_RBV")
            DSUM.setMonitored(True)
            ACQ = create_channel_device("PINK:CAE2:Acquire", type='i')
            ACQ.setMonitored(True)
            #bladepos = create_channel_device("PINK:MSIM:m2")
            #bladepos_RBV = create_channel_device("PINK:MSIM:m2.RBV")
            #bladepos_RBV.setMonitored(True)

            ## simulated channels
            DSUMS = create_channel_device("PINK:MSIM2:sigmoid")
            DSUMS.setMonitored(True)
            bladepos = create_channel_device("PINK:MSIM2:m5")
            bladepos_RBV = create_channel_device("PINK:MSIM2:m5.RBV")
            bladepos_RBV.setMonitored(True)            
            
            ## variables
            sig2fwmh=2.355
            diode1 = []
            diode2 = []
            diode3 = []
            diode4 = []
            diode_sum = []
            tfy = []
            
            
            ## Setup 
            print("Scanning ...")
            set_exec_pars(open=False, name="blade_diag", reset=True)

            ## Configure ampmeter
            cae_exp_time=float(exposure)
            ACQ.write(0)
            sleep(1)
            caput("PINK:CAE2:ValuesPerRead", int(1000*cae_exp_time))
            caput("PINK:CAE2:AveragingTime", cae_exp_time)
            caput("PINK:CAE2:TriggerMode", 0)
            caput("PINK:CAE2:AcquireMode", 2)
            sleep(1)

            ## Main loop
            for i in range(steps):
                while(ACQ.take()==1):
                    sleep(0.25)
                ACQ.write(1)
                resp = DSUM.waitCacheChange(1000*int(exposure+2))
                if resp==False:
                    print("Abort: No data from ampmeter")
                    return
                diode_sum.append(DSUM.take())
            caput("PINK:CAE2:AcquireMode", 0)
            print("OK")

        def run_sec_scan(self):
            print("Diag scan")   