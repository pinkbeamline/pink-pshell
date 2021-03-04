class BLSETUPSET():
    def set(self, params, energy):
        print("Set up beamline")
        print("    energy: {} eV".format(energy))

        ## Set filter calculation energy
        self.__setenergy(energy)

        ## Send DCM and PGM home
        self.__dcm_pgm_home()
        
        ## gap
        if params.has_key("gap"):
            print("Undulator U17")
            print("    gap: {} mm".format(params["gap"]))
            # move motors
            self.__move_gap(params)

        ## M1 mirror
        if params.has_key("m1tx") or params.has_key("m1ty") or params.has_key("m1rx") or params.has_key("m1ry") or params.has_key("m1rz"):
            print("M1 mirror")
            if params.has_key("m1tx"):
                if params.has_key("m1deltatx"): 
                    delta = "+- {}".format(params["m1deltatx"]) 
                else: 
                    delta = ""
                print("    Tx: {} um {}".format(params["m1tx"], delta))
            if params.has_key("m1ty"):
                if params.has_key("m1deltaty"): 
                    delta = "+- {}".format(params["m1deltaty"]) 
                else:
                    delta = ""
                print("    Ty: {} um {}".format(params["m1ty"], delta))
            if params.has_key("m1rx"):
                if params.has_key("m1deltarx"): 
                    delta = "+- {}".format(params["m1deltarx"]) 
                else: 
                    delta = ""            
                print("    Rx: {} um {}".format(params["m1rx"], delta))
            if params.has_key("m1ry"):
                if params.has_key("m1deltary"): 
                    delta = "+- {}".format(params["m1deltary"]) 
                else: 
                    delta = ""             
                print("    Ry: {} um {}".format(params["m1ry"], delta))                
            if params.has_key("m1rz"):
                if params.has_key("m1deltarz"): 
                    delta = "+- {}".format(params["m1deltarz"]) 
                else: 
                    delta = ""             
                print("    Rz: {} um {}".format(params["m1rz"], delta))
            ## move motors
            self.__move_m1(params)

        ## filter foil
        if params.has_key("foil"):
            print("Filter foil")
            print("    filter: {} um C".format(params["foil"]))
            ## move motors
            self.__move_filter(params)            

        ## AU1 aperture
        if params.has_key("au1centery") or params.has_key("au1centerx") or params.has_key("au1gapy") or params.has_key("au1gapx"):
            print("AU1 aperture")
            if params.has_key("au1centery"):   
                print("    center Y: {} mm".format(params["au1centery"]))    
            if params.has_key("au1centerx"):   
                print("    center X: {} mm".format(params["au1centerx"]))
            if params.has_key("au1gapy"):   
                print("    gap Y: {} mm".format(params["au1gapy"]))    
            if params.has_key("au1gapx"):   
                print("    gap X: {} mm".format(params["au1gapx"]))
            ## move motors
            self.__move_au1(params)
            
        ## AU2 aperture
        if params.has_key("au2centery") or params.has_key("au2centerx") or params.has_key("au2gapy") or params.has_key("au2gapx"):
            print("AU2 aperture")
            if params.has_key("au2centery"):   
                print("    center Y: {} mm".format(params["au2centery"]))    
            if params.has_key("au2centerx"):   
                print("    center X: {} mm".format(params["au2centerx"]))
            if params.has_key("au2gapy"):   
                print("    gap Y: {} mm".format(params["au2gapy"]))    
            if params.has_key("au2gapx"):   
                print("    gap X: {} mm".format(params["au2gapx"]))
            ## move motors
            self.__move_au2(params)

        ## AU3 aperture
        if params.has_key("au3centery") or params.has_key("au3centerx") or params.has_key("au3gapy") or params.has_key("au3gapx"):
            print("AU3 aperture")
            if params.has_key("au3centery"):   
                print("    center Y: {} mm".format(params["au3centery"]))    
            if params.has_key("au3centerx"):   
                print("    center X: {} mm".format(params["au3centerx"]))
            if params.has_key("au3gapy"):   
                print("    gap Y: {} mm".format(params["au3gapy"]))    
            if params.has_key("au3gapx"):   
                print("    gap X: {} mm".format(params["au3gapx"]))
            ## move motors
            self.__move_au3(params)

        ## M2 mirror
        if params.has_key("m2group") or params.has_key("m2tx") or params.has_key("m2ty") or params.has_key("m2tz") or params.has_key("m2rx") or params.has_key("m2ry") or params.has_key("m2rz") or params.has_key("poix") or params.has_key("poiy"):
            print("M2 mirror")
            if params.has_key("m2group"):
                try:
                    groupid = int(params["m2group"])
                    if groupid>=1 and groupid<=3:
                        print("    group: Optic ID# {}".format(groupid))
                except:
                    pass
            if params.has_key("m2poix"):
                print("    poix: {} um".format(params["m2poix"]))
            if params.has_key("m2poiy"):
                print("    poiy: {} um".format(params["m2poiy"]))
            if params.has_key("m2tx"):
                if params.has_key("m2deltatx"): 
                    delta = "+- {}".format(params["m2deltatx"]) 
                else: 
                    delta = ""
                print("    Tx: {} um {}".format(params["m2tx"], delta))
            if params.has_key("m2ty"):
                if params.has_key("m2deltaty"): 
                    delta = "+- {}".format(params["m2deltaty"]) 
                else: 
                    delta = ""
                print("    Ty: {} um {}".format(params["m2ty"], delta))
            if params.has_key("m2tz"):
                if params.has_key("m2deltatz"): 
                    delta = "+- {}".format(params["m2deltatz"]) 
                else: 
                    delta = ""
                print("    Tz: {} um {}".format(params["m2tz"], delta))            
            if params.has_key("m2rx"):
                if params.has_key("m2deltarx"): 
                    delta = "+- {}".format(params["m2deltarx"]) 
                else: 
                    delta = ""            
                print("    Rx: {} um {}".format(params["m2rx"], delta))
            if params.has_key("m2ry"):
                if params.has_key("m2deltary"): 
                    delta = "+- {}".format(params["m2deltary"]) 
                else: 
                    delta = ""             
                print("    Ry: {} um {}".format(params["m2ry"], delta))                
            if params.has_key("m2rz"):
                if params.has_key("m2deltarz"): 
                    delta = "+- {}".format(params["m2deltarz"]) 
                else: 
                    delta = ""             
                print("    Rz: {} um {}".format(params["m2rz"], delta))
            ## move motors
            self.__move_m2(params)

        ## BPM1 cross position
        if params.has_key("cross1x") or params.has_key("cross1y"):
            print("BPM1 cross position")
            if params.has_key("cross1x"):
                print("    X: {} px".format(params["cross1x"]))
            if params.has_key("cross1y"):
                print("    Y: {} px".format(params["cross1y"]))
            ## move motors
            self.__move_bpm1(params)

        ## BPM2 cross position
        if params.has_key("cross2x") or params.has_key("cross2y"):
            print("BPM2 cross position")
            if params.has_key("cross2x"):
                print("    X: {} px".format(params["cross2x"]))
            if params.has_key("cross2y"):
                print("    Y: {} px".format(params["cross2y"]))
            ## move motors
            self.__move_bpm2(params)

        ## BPM3 cross position
        if params.has_key("cross3x") or params.has_key("cross3y"):
            print("BPM3 cross position")
            if params.has_key("cross3x"):
                print("    X: {} px".format(params["cross3x"]))
            if params.has_key("cross3y"):
                print("    Y: {} px".format(params["cross3y"]))
            ## move motors
            self.__move_bpm3(params)

        print("{0:-<25}".format(""))

        run("plib/blsetup_check")
        blchk = BLSETUPCHECK()

        blchk.check_gap(params)
        blchk.check_m1(params)
        blchk.check_filter(params)
        blchk.check_dcm_pgm(params)
        blchk.check_au1(params)
        blchk.check_au2(params)
        blchk.check_au3(params)
        blchk.check_m2(params)
        blchk.check_bpm1(params)
        blchk.check_bpm2(params)
        blchk.check_bpm2(params)

        print("{0:-<25}".format(""))


    ### -----------------------------------------------------------------------------

    ## Set energy
    def __setenergy(self, energy):
        try:
            caput("PINK:FILTER:BeamEnergy", energy)
        except:
            log("[BL setup] Error while setting filter energy")
    
    ### move gap
    def __move_gap(self, params):
        #log("move gap")
        #return
        if params.has_key("gap"):
            pos = params["gap"]
            try:
                caput("U17IT6R:BaseParGapsel.B", pos)
                sleep(0.2)
                caput("U17IT6R:BaseCmdCalc.PROC", 1)
            except:
                log("[BL setup] Error while moving undulator")

    ### move M1
    def __move_m1(self, params):
        #print("move m1")
        if params.has_key("m1tx"):
            pos = params["m1tx"]
            if params.has_key("m1deltatx"):
                dpos = params["m1deltatx"]
            else:
                dpos = 0
            try:
                rbvpos = caget("U17_M1:rdTx")
                errpos = abs(rbvpos-pos)
                if errpos>dpos:
                    setpos = caget("U17_M1:TxAbs")
                    if setpos==pos:
                        #mirror rbv>set
                        caput("U17_M1:TxAbs", rbvpos)
                        self.__m1wait()
                    #set parameter and wait
                    caput("U17_M1:TxAbs", pos)
                    self.__m1wait()
            except:
                log("[BL setup] Error while moving M1 Tx")
        if params.has_key("m1ty"):
            pos = params["m1ty"]
            if params.has_key("m1deltaty"):
                dpos = params["m1deltaty"]
            else:
                dpos = 0            
            try:
                rbvpos = caget("U17_M1:rdTy")
                errpos = abs(rbvpos-pos)
                if errpos>dpos:            
                    setpos = caget("U17_M1:TyAbs")
                    if setpos==pos:
                        #mirror rbv>set
                        caput("U17_M1:TyAbs", rbvpos)
                        self.__m1wait()
                    #set parameter and wait
                    caput("U17_M1:TyAbs", pos)
                    self.__m1wait()
            except:
                log("[BL setup] Error while moving M1 Ty")
        if params.has_key("m1rx"):
            pos = params["m1rx"]
            if params.has_key("m1deltarx"):
                dpos = params["m1deltarx"]
            else:
                dpos = 0             
            try:
                rbvpos = caget("U17_M1:rdRx")
                errpos = abs(rbvpos-pos)
                if errpos>dpos:              
                    setpos = caget("U17_M1:RxAbs")
                    if setpos==pos:
                        #mirror rbv>set
                        caput("U17_M1:RxAbs", rbvpos)
                        self.__m1wait()
                    #set parameter and wait
                    caput("U17_M1:RxAbs", pos)
                    self.__m1wait()
            except:
                log("[BL setup] Error while moving M1 Rx")
        if params.has_key("m1ry"):
            pos = params["m1ry"]
            if params.has_key("m1deltary"):
                dpos = params["m1deltary"]
            else:
                dpos = 0               
            try:
                rbvpos = caget("U17_M1:rdRy")
                errpos = abs(rbvpos-pos)
                if errpos>dpos:            
                    setpos = caget("U17_M1:RyAbs")
                    if setpos==pos:
                        #mirror rbv>set
                        caput("U17_M1:RyAbs", rbvpos)
                        self.__m1wait()
                    #set parameter and wait
                    caput("U17_M1:RyAbs", pos)
                    self.__m1wait()
            except:
                log("[BL setup] Error while moving M1 Ry")
        if params.has_key("m1rz"):
            pos = params["m1rz"]
            if params.has_key("m1deltarz"):
                dpos = params["m1deltarz"]
            else:
                dpos = 0               
            try:
                rbvpos = caget("U17_M1:rdRz")
                errpos = abs(rbvpos-pos)
                if errpos>dpos:            
                    setpos = caget("U17_M1:RzAbs")
                    if setpos==pos:
                        #mirror rbv>set
                        caput("U17_M1:RzAbs", rbvpos)
                        self.__m1wait()
                    #set parameter and wait
                    caput("U17_M1:RzAbs", pos)
                    self.__m1wait()
            except:
                log("[BL setup] Error while moving M1 Rz")

    ### move filter
    def __move_filter(self, params):
        #print("move filter")
        #return
        # filter pos: {0:--, 1:5, 2:10, 3:20, 4:0:home}
        # 0:--
        # 1: 5um x=1.5, y=
        # 2:10um x=1.5, y=38.0
        # 3:20um x=1.5, y=
        # 4:home x=1.5, y=
        if params.has_key("foil"):
            posid=None
            try:
                pos = int(params["foil"])
                if pos==0:
                    posid=4
                elif pos==5:
                    posid=1
                elif pos==10:
                    posid=2
                elif pos==20:
                    posid=3
                else:
                    log("[BL setup] Undefined foil option")
                    return
                rbvposid = caget("u171dcm1:PH_2_GETN", type='i')
                if rbvposid!=posid:
                    caput("u171dcm1:PH_2_GON", 0)
                    sleep(2)
                    caput("u171dcm1:PH_2_GON", posid)
            except:
                log("[BL setup] Error while moving foil")

    ### move AU1
    def __move_au1(self, params):
        #print("move au1")
        #return
        deadband = 0.002
        if params.has_key("au1centery") and params.has_key("au1gapy"):
            aucenter = params["au1centery"]
            augap = params["au1gapy"]
            aupos = aucenter+abs(augap/2)
            auneg = aucenter-abs(augap/2)
            try:
                err = abs(aupos-caget("WAUY02U012L:rdPosM1"))
                if err>deadband:
                    caput("WAUY02U012L:AbsM1", aupos)
            except:
                log("[BL setup] Error while moving AU1 top")
            try:
                err = abs(auneg-caget("WAUY02U012L:rdPosM2"))
                if err>deadband:
                    caput("WAUY02U012L:AbsM2", auneg)
            except:
                log("[BL setup] Error while moving AU1 bottom")              
        if params.has_key("au1centerx") and params.has_key("au1gapx"):
            aucenter = params["au1centerx"]
            augap = params["au1gapx"]
            aupos = aucenter+abs(augap/2)
            auneg = aucenter-abs(augap/2)
            try:
                err = abs(aupos-caget("WAUY02U012L:rdPosM3"))
                if err>deadband:
                    caput("WAUY02U012L:AbsM3", aupos)
            except:
                log("[BL setup] Error while moving AU1 left")
            try:
                err = abs(auneg-caget("WAUY02U012L:rdPosM4"))
                if err>deadband:
                    caput("WAUY02U012L:AbsM4", auneg)
            except:
                log("[BL setup] Error while moving AU1 right")   
    ### move AU2
    def __move_au2(self, params):
        #print("move au2")
        #return
        deadband = 0.002
        if params.has_key("au2centery") and params.has_key("au2gapy"):
            aucenter = params["au2centery"]
            augap = params["au2gapy"]
            aupos = aucenter+abs(augap/2)
            auneg = aucenter-abs(augap/2)
            try:
                err = abs(aupos-caget("u171pgm1:PH_2_GET"))
                if err>deadband:
                    caput("u171pgm1:PH_2_SET", aupos)
            except:
                log("[BL setup] Error while moving AU2 top")
            try:
                err = abs(auneg-caget("u171pgm1:PH_3_GET"))
                if err>deadband:
                    caput("u171pgm1:PH_3_SET", auneg)
            except:
                log("[BL setup] Error while moving AU2 bottom")              
        if params.has_key("au2centerx") and params.has_key("au2gapx"):
            aucenter = params["au2centerx"]
            augap = params["au2gapx"]
            aupos = aucenter+abs(augap/2)
            auneg = aucenter-abs(augap/2)
            try:
                err = abs(aupos-caget("u171pgm1:PH_5_GET"))
                if err>deadband:
                    caput("u171pgm1:PH_5_SET", aupos)
            except:
                log("[BL setup] Error while moving AU1 right")
            try:
                err = abs(auneg-caget("u171pgm1:PH_4_GET"))
                if err>deadband:
                    caput("u171pgm1:PH_4_SET", auneg)
            except:
                log("[BL setup] Error while moving AU1 left")   

    ### move AU3
    def __move_au3(self, params):
        #print("move au3")
        #return
        deadband = 0.002
        if params.has_key("au3centery") and params.has_key("au3gapy"):
            aucenter = params["au3centery"]
            augap = params["au3gapy"]
            aupos = aucenter+abs(augap/2)
            auneg = aucenter-abs(augap/2)
            try:
                err = abs(aupos-caget("AUY01U112L:rdPosM1"))
                if err>deadband:
                    caput("AUY01U112L:AbsM1", aupos)
            except:
                log("[BL setup] Error while moving AU3 top")
            try:
                err = abs(auneg-caget("AUY01U112L:rdPosM2"))
                if err>deadband:
                    caput("AUY01U112L:AbsM2", auneg)
            except:
                log("[BL setup] Error while moving AU3 bottom")              
        if params.has_key("au3centerx") and params.has_key("au3gapx"):
            aucenter = params["au3centerx"]
            augap = params["au3gapx"]
            aupos = aucenter+abs(augap/2)
            auneg = aucenter-abs(augap/2)
            try:
                err = abs(aupos-caget("AUY01U112L:rdPosM4"))
                if err>deadband:
                    caput("AUY01U112L:AbsM4", aupos)
            except:
                log("[BL setup] Error while moving AU3 right")
            try:
                err = abs(auneg-caget("AUY01U112L:rdPosM3"))
                if err>deadband:
                    caput("AUY01U112L:AbsM3", auneg)
            except:
                log("[BL setup] Error while moving AU3 left")  

   ### move M2 
    def __move_m2(self, params):
        #print("move m2")
        #return
        ## set M2 group
        if params.has_key("m2group"):
            try:
                groupid = int(params["m2group"])
                if groupid>=1 and groupid<=3:
                    epicsgroupid_array = [2, 1, 0]
                    pos = epicsgroupid_array[groupid-1]
                    actualpos = caget("HEX2OS12L:hexapod:mbboMirrorChoicerRun", 'i')
                    if actualpos!=pos:
                        caput("HEX2OS12L:hexapod:mbboMirrorChoicerRun", pos)
                        self.__m2wait()
            except Exception, errmsg:
                log("[BL setup] Error while setting M2 mirror group")
                log(errmsg)
                
        if params.has_key("m2poix") or params.has_key("m2poiy") or params.has_key("m2tx") or params.has_key("m2ty") or params.has_key("m2tz") or params.has_key("m2rx") or params.has_key("m2ry") or params.has_key("m2rz"):
            m2execute = False
            try:
                ## disable "run after value set" {0:ON, 1:OFF}
                caput("HEX2OS12L:hexapod:mbboRunAfterValue", 1)
            except:
                log("[BL setup] Error while setting run immediatly option OFF")
                return

            if params.has_key("m2poix"):
                pos = params["m2poix"]
                try:
                    caput("HEX2OS12L:multiaxis:setPOIx", pos)
                    sleep(0.25)
                except:
                    log("[BL setup] Error while setting M2 POI X")
            if params.has_key("m2poiy"):
                pos = params["m2poiy"]
                try:
                    caput("HEX2OS12L:multiaxis:setPOIy", pos)
                    sleep(0.25)
                except:
                    log("[BL setup] Error while setting M2 POI Y") 
                    
            if params.has_key("m2tx"):
                pos = params["m2tx"]
                if params.has_key("m2deltatx"):
                    dpos = params["m2deltatx"]
                else:
                    dpos = 0
                try:
                    rbvpos = caget("HEX2OS12L:hexapod:getReadPoseX")
                    errpos = abs(rbvpos-pos)
                    caput("HEX2OS12L:hexapod:setPoseX", pos)
                    if errpos>dpos:
                        #caput("HEX2OS12L:hexapod:setPoseX", pos)
                        #sleep(0.5)
                        m2execute = True
                except:
                    log("[BL setup] Error while moving M2 Tx")
            if params.has_key("m2ty"):
                pos = params["m2ty"]
                if params.has_key("m2deltaty"):
                    dpos = params["m2deltaty"]
                else:
                    dpos = 0
                try:
                    rbvpos = caget("HEX2OS12L:hexapod:getReadPoseY")
                    errpos = abs(rbvpos-pos)
                    caput("HEX2OS12L:hexapod:setPoseY", pos)
                    if errpos>dpos:
                        #caput("HEX2OS12L:hexapod:setPoseY", pos)
                        #sleep(0.5)
                        m2execute = True
                except:
                    log("[BL setup] Error while moving M2 Ty") 
            if params.has_key("m2tz"):
                pos = params["m2tz"]
                if params.has_key("m2deltatz"):
                    dpos = params["m2deltatz"]
                else:
                    dpos = 0
                try:
                    rbvpos = caget("HEX2OS12L:hexapod:getReadPoseZ")
                    errpos = abs(rbvpos-pos)
                    caput("HEX2OS12L:hexapod:setPoseZ", pos)
                    if errpos>dpos:
                        #caput("HEX2OS12L:hexapod:setPoseZ", pos)
                        #sleep(0.5)
                        m2execute = True
                except:
                    log("[BL setup] Error while moving M2 Tz")
            if params.has_key("m2rx"):
                pos = params["m2rx"]
                if params.has_key("m2deltarx"):
                    dpos = params["m2deltarx"]
                else:
                    dpos = 0
                try:
                    rbvpos = caget("HEX2OS12L:hexapod:getReadPoseA")
                    errpos = abs(rbvpos-pos)
                    caput("HEX2OS12L:hexapod:setPoseA", pos)
                    if errpos>dpos:
                        #caput("HEX2OS12L:hexapod:setPoseA", pos)
                        #sleep(0.5)
                        m2execute = True
                except:
                    log("[BL setup] Error while moving M2 Rx")                     
            if params.has_key("m2ry"):
                pos = params["m2ry"]
                if params.has_key("m2deltary"):
                    dpos = params["m2deltary"]
                else:
                    dpos = 0
                try:
                    rbvpos = caget("HEX2OS12L:hexapod:getReadPoseB")
                    errpos = abs(rbvpos-pos)
                    caput("HEX2OS12L:hexapod:setPoseB", pos)
                    if errpos>dpos:
                        #caput("HEX2OS12L:hexapod:setPoseB", pos)
                        #sleep(0.5)
                        m2execute = True
                except:
                    log("[BL setup] Error while moving M2 Ry")                    
            if params.has_key("m2rz"):
                pos = params["m2rz"]
                if params.has_key("m2deltarz"):
                    dpos = params["m2deltarz"]
                else:
                    dpos = 0
                try:
                    rbvpos = caget("HEX2OS12L:hexapod:getReadPoseC")
                    errpos = abs(rbvpos-pos)
                    caput("HEX2OS12L:hexapod:setPoseC", pos)
                    if errpos>dpos:
                        #caput("HEX2OS12L:hexapod:setPoseC", pos)
                        #sleep(0.5)
                        m2execute = True
                except:
                    log("[BL setup] Error while moving M2 Rz")

            ## execute target pose
            sleep(1)
            if m2execute:
                try:
                    caput("HEX2OS12L:multiaxis:run", 1)
                    self.__m2wait()
                    sleep(2)
                    caput("HEX2OS12L:multiaxis:run", 1)
                    self.__m2wait()
                except:
                    log("[BL setup] Error while executing M2 move all")
                sleep(1)
            try:
                ## enable "run after value set" {0:ON, 1:OFF}
                caput("HEX2OS12L:hexapod:mbboRunAfterValue", 0)
            except:
                log("[BL setup] Error while setting M2 run immediatly option ON")            
                
    ### move BPM1 cross
    def __move_bpm1(self, params):
        #print("move bpm1")
        #return
        if params.has_key("cross1x"):
            pos = params["cross1x"]
            try:
                caput("PINK:PG01:Over1:5:CenterX", pos)
            except:
                log("[BL setup] Error while setting BPM 1 cross X")
        if params.has_key("cross1y"):
            pos = params["cross1y"]
            try:
                caput("PINK:PG01:Over1:5:CenterY", pos)
            except:
                log("[BL setup] Error while setting BPM 1 cross Y")
        sleep(0.5)
    ### move BPM2 cross
    def __move_bpm2(self, params):
        #print("move bpm2")           
        #return
        if params.has_key("cross2x"):
            pos = params["cross2x"]
            try:
                caput("PINK:PG04:Over1:5:CenterX", pos)
            except:
                log("[BL setup] Error while setting BPM 2 cross X")
        if params.has_key("cross2y"):
            pos = params["cross2y"]
            try:
                caput("PINK:PG04:Over1:5:CenterY", pos)
            except:
                log("[BL setup] Error while setting BPM 2 cross Y")
        sleep(0.5)                
    ### move BPM3 cross
    def __move_bpm3(self, params):
        #print("move bpm3")    
        #return
        if params.has_key("cross3x"):
            pos = params["cross3x"]
            try:
                caput("PINK:PG03:Over1:5:CenterX", pos)
            except:
                log("[BL setup] Error while setting BPM 3 cross X")
        if params.has_key("cross3y"):
            pos = params["cross3y"]
            try:
                caput("PINK:PG03:Over1:5:CenterY", pos)
            except:
                log("[BL setup] Error while setting BPM 3 cross Y")
        sleep(0.5)                

    ### -----------------------------------------------------------------------------

    ## Wait for M1 to stop moving
    def __m1wait(self):
        m1pvlist= [
            "U17_M1:rdCurSpeedM1",
            "U17_M1:rdCurSpeedM2",
            "U17_M1:rdCurSpeedM3",
            "U17_M1:rdCurSpeedM4",
            "U17_M1:rdCurSpeedM5",
            ]
        donecount=0
        while(donecount<=2):
            m1speedsum=0
            for m1pv in m1pvlist:
                m1speedsum+=int(caget(m1pv))
            if(m1speedsum==0):
                donecount+=1
            else:
                donecount=0
            sleep(1)

    def __m2wait(self):
        #log("[BL Setup] Waiting M2...")
        set_status("Waiting for M2 to finish motion...")
        donecount=0
        while(donecount<=2):
            m2running = int(caget("HEX2OS12L:multiaxis:running"))
            if m2running:
                donecount=0
            else:
                donecount+=1
            sleep(1)   
        #log("[BL Setup] Done Waiting M2.")
        set_status("Running...")


    ## Send DCM and PGM home
    def __dcm_pgm_home(self):
        # dcm {0:--, 4:home}
        try:
            caput("u171dcm1:PH_0_GON", 0)
            sleep(2)
            caput("u171dcm1:PH_0_GON", 4)
        except:
            log("[BL Setup] Error settting DCM position")
        # pgm {0:--, 2:home}
        try:
            caput("u171pgm1:PH_0_GON", 0)
            sleep(2)
            caput("u171dcm1:PH_0_GON", 2)
        except:
            log("[BL Setup] Error settting PGM position")            
            
            