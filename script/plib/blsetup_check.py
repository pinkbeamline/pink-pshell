class BLSETUPCHECK():
    def check_gap(self, params):
        #return
        if params.has_key("gap"):
            pos = params["gap"]
            motor_deadband = 0.02
            status="error"
            isworking=True
            try:
                err=abs(caget("U17IT6R:BasePmGap.A")-pos)
                if err<=motor_deadband:
                    isworking=False
                    status="OK"
                while(isworking):
                    sleep(2)
                    newerr=abs(caget("U17IT6R:BasePmGap.A")-pos)
                    if newerr<err:
                        err=newerr
                        log("[BL setup] gap is in motion")
                    else:
                        isworking=False
                err=abs(caget("U17IT6R:BasePmGap.A")-pos)
                if err<=motor_deadband:
                    status="OK"                 
            except:
                log("[BL setup] Error while moving undulator")        
            print("{0:.<17}[{1:^6}]".format("gap",status))

    def check_m1(self, params):
        #return
        status="OK"
        if params.has_key("m1tx") or params.has_key("m1ty") or params.has_key("m1rx") or params.has_key("m1ry") or params.has_key("m1rz"):
            status="OK"
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
                        status="error"
                        log("[BL setup] Error on M1 Tx position")
                except:
                    status="error"
                    log("[BL setup] Error while checking M1 Tx")
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
                        status="error"
                        log("[BL setup] Error on M1 Ty position")
                except:
                    status="error"
                    log("[BL setup] Error while checking M1 Ty")
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
                        status="error"
                        log("[BL setup] Error on M1 Rx position")
                except:
                    status="error"
                    log("[BL setup] Error while checking M1 Rx")
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
                        status="error"
                        log("[BL setup] Error on M1 Ry position")
                except:
                    status="error"
                    log("[BL setup] Error while checking M1 Ry")
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
                        status="error"
                        log("[BL setup] Error on M1 Rz position")
                except:
                    status="error"
                    log("[BL setup] Error while checking M1 Rz")
            # print status
            print("{0:.<17}[{1:^6}]".format("M1",status))

    def check_filter(self, params):
        #return
        # filter pos: {0:--, 1:5, 2:10, 3:20, 4:0:home}
        if params.has_key("foil"):
            posid=None
            status="error"
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
                    return
                rbvposid = caget("u171dcm1:PH_2_GETN", type='i')
                if rbvposid!=posid:
                    log("[BL setup] Error on filter position")
                else:
                    status="OK"
            except:
                log("[BL setup] Error while checking filter position")
            print("{0:.<17}[{1:^6}]".format("filter",status))

    def check_au1(self, params):
        if params.has_key("au1centery") or params.has_key("au1centerx") or params.has_key("au1gapy") or params.has_key("au1gapx"):
            status = "OK"
            dead_band = 0.002
            if params.has_key("au1centery"):
                pos = params["au1centery"]
                try:
                    rbvpos = caget("PINK:AU1:centerY_RBV")
                    err=abs(rbvpos-pos)
                    if err>dead_band:
                        status="error"
                        log("[BL setup] Error on AU1 center Y")
                except:
                    status="error"
                    log("[BL setup] Error while checking AU1 center Y")
            if params.has_key("au1centerx"):
                pos = params["au1centerx"]
                try:
                    rbvpos = caget("PINK:AU1:centerX_RBV")
                    err=abs(rbvpos-pos)
                    if err>dead_band:
                        status="error"
                        log("[BL setup] Error on AU1 center X")
                except:
                    status="error"
                    log("[BL setup] Error while checking AU1 center X")
            if params.has_key("au1gapy"):
                pos = params["au1gapy"]
                try:
                    caput("PINK:AU1:apertureY", pos)
                except:
                    log("[BL setup] Error while moving AU1 aperture Y")
            if params.has_key("au1gapx"):
                pos = params["au1gapx"]
                try:
                    caput("PINK:AU1:apertureX", pos)
                except:
                    log("[BL setup] Error while moving AU1 aperture X")
                    
            print("{0:.<17}[{1:^6}]".format("AU1",status))

    def check_au2(self, params):
        if params.has_key("au2centery") or params.has_key("au2centerx") or params.has_key("au2gapy") or params.has_key("au2gapx"):
            status = "OK"
            dead_band = 0.002
            if params.has_key("au2centery"):
                pos = params["au2centery"]
                try:
                    rbvpos = caget("PINK:AU2:centerY_RBV")
                    err=abs(rbvpos-pos)
                    if err>dead_band:
                        status="error"
                        log("[BL setup] Error on AU2 center Y")
                except:
                    status="error"
                    log("[BL setup] Error while checking AU2 center Y")
            if params.has_key("au2centerx"):
                pos = params["au2centerx"]
                try:
                    rbvpos = caget("PINK:AU2:centerX_RBV")
                    err=abs(rbvpos-pos)
                    if err>dead_band:
                        status="error"
                        log("[BL setup] Error on AU2 center X")
                except:
                    status="error"
                    log("[BL setup] Error while checking AU2 center X")
            if params.has_key("au2gapy"):
                pos = params["au2gapy"]
                try:
                    caput("PINK:AU2:apertureY", pos)
                except:
                    log("[BL setup] Error while moving AU2 aperture Y")
            if params.has_key("au2gapx"):
                pos = params["au2gapx"]
                try:
                    caput("PINK:AU2:apertureX", pos)
                except:
                    log("[BL setup] Error while moving AU2 aperture X")
                    
            print("{0:.<17}[{1:^6}]".format("AU2",status))

    def check_au3(self, params):
        if params.has_key("au3centery") or params.has_key("au3centerx") or params.has_key("au3gapy") or params.has_key("au3gapx"):
            status = "OK"
            dead_band = 0.002
            if params.has_key("au3centery"):
                pos = params["au3centery"]
                try:
                    rbvpos = caget("PINK:AU3:centerY_RBV")
                    err=abs(rbvpos-pos)
                    if err>dead_band:
                        status="error"
                        log("[BL setup] Error on AU3 center Y")
                except:
                    status="error"
                    log("[BL setup] Error while checking AU3 center Y")
            if params.has_key("au3centerx"):
                pos = params["au3centerx"]
                try:
                    rbvpos = caget("PINK:AU3:centerX_RBV")
                    err=abs(rbvpos-pos)
                    if err>dead_band:
                        status="error"
                        log("[BL setup] Error on AU3 center X")
                except:
                    status="error"
                    log("[BL setup] Error while checking AU3 center X")
            if params.has_key("au3gapy"):
                pos = params["au3gapy"]
                try:
                    caput("PINK:AU3:apertureY", pos)
                except:
                    log("[BL setup] Error while moving AU3 aperture Y")
            if params.has_key("au3gapx"):
                pos = params["au3gapx"]
                try:
                    caput("PINK:AU3:apertureX", pos)
                except:
                    log("[BL setup] Error while moving AU3 aperture X")
                    
            print("{0:.<17}[{1:^6}]".format("AU3",status))

    def check_m2(self, params):
        if params.has_key("m2group") or params.has_key("m2poix") or params.has_key("m2poiy") or params.has_key("m2tx") or params.has_key("m2ty") or params.has_key("m2tz") or params.has_key("m2rx") or params.has_key("m2ry") or params.has_key("m2rz")
            status = "OK"
            if params.has_key("m2group"):
                try:
                    groupid = int(params["m2group"])
                    if groupid>=1 and groupid<=3:
                        epicsgroupid_array = [2, 1, 0]
                        pos = epicsgroupid_array[groupid-1]
                        actualpos = caget("HEX2OS12L:hexapod:mbboMirrorChoicerRun", 'i')
                        if actualpos!=pos:
                            status = "error"
                            log("[BL setup] Error on M2 mirror group") 
                        else:
                            self.__move_m2all(params)
                except:
                    log("[BL setup] Error while checking M2 mirror group") 

        ## wait for end of motion
        ## check positions
        
        print("{0:.<17}[{1:^6}]".format("M2",status))

    def check_bpm1(self, params):
        status = "OK"
        print("{0:.<17}[{1:^6}]".format("BPM1",status))

    def check_bpm2(self, params):
        status = "OK"
        print("{0:.<17}[{1:^6}]".format("BPM2",status))

    def check_bpm3(self, params):
        status = "OK"
        print("{0:.<17}[{1:^6}]".format("BPM3",status))


    ## move m2 all
    def __move_m2all(self, params):
        if params.has_key("m2poix") or params.has_key("m2poiy") or params.has_key("m2tx") or params.has_key("m2ty") or params.has_key("m2tz") or params.has_key("m2rx") or params.has_key("m2ry") or params.has_key("m2rz"):
            try:
                ## disable "run after value set" {0:ON, 1:OFF}
                caput("HEX2OS12L:hexapod:mbboRunAfterValue", 1)
            except:
                log("[BL setup] Error while setting run immediatly option OFF")
                 
            if params.has_key("m2poix"):
                pos = params["m2poix"]
                try:
                    caput("HEX2OS12L:multiaxis:setPOIx", pos)
                except:
                    log("[BL setup] Error while setting M2 POI X")
            if params.has_key("m2poiy"):
                pos = params["m2poiy"]
                try:
                    caput("HEX2OS12L:multiaxis:setPOIy", pos)
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
                    if errpos>dpos:
                        caput("HEX2OS12L:hexapod:setPoseX", pos)
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
                    if errpos>dpos:
                        caput("HEX2OS12L:hexapod:setPoseY", pos)
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
                    if errpos>dpos:
                        caput("HEX2OS12L:hexapod:setPoseZ", pos)
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
                    if errpos>dpos:
                        caput("HEX2OS12L:hexapod:setPoseA", pos)
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
                    if errpos>dpos:
                        caput("HEX2OS12L:hexapod:setPoseB", pos)
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
                    if errpos>dpos:
                        caput("HEX2OS12L:hexapod:setPoseC", pos)
                except:
                    log("[BL setup] Error while moving M2 Rz")

            ## execute target pose
            sleep(1)
            try:
                caput("HEX2OS12L:multiaxis:run", 1)
            except:
                log("[BL setup] Error while executing M2 move all")
            sleep(1)
            try:
                ## enable "run after value set" {0:ON, 1:OFF}
                caput("HEX2OS12L:hexapod:mbboRunAfterValue", 0)
            except:
                log("[BL setup] Error while setting M2 run immediatly option ON")          
    