class BLSETUPCHECK():
    def check_gap(self, params):
        if params.has_key("gap"):
            pos = params["gap"]
            motor_deadband = 0.01
            status="error"
            isworking=True
            try:
                log("[BL Check] waiting for Undulator" )
                while(caget("U17IT6R:BaseStatISLbl", type='i')!=1):
                    sleep(1)
                #err=abs(caget("U17IT6R:BasePmGap.A")-pos)
                #if err<=motor_deadband:
                #    isworking=False
                #    status="OK"
                #while(isworking):
                #    sleep(2)
                #    newerr=abs(caget("U17IT6R:BasePmGap.A")-pos)
                #    if newerr<err:
                #        err=newerr
                #        log("[BL setup] gap is in motion")
                #    else:
                #        isworking=False
                err=abs(caget("U17IT6R:BasePmGap.A")-pos)
                if err<=motor_deadband:
                    status="OK"
            except:
                log("[BL setup] Error while moving undulator")
            print("{0:.<17}[{1:^6}]".format("gap",status))

    def check_dcm_pgm(self, params):
        # DCM
        if caget("u171dcm1:axis6:running", type='i'):
            set_status("Waiting for DCM to finish motion...")
            while(caget("u171dcm1:axis6:running", type='i')):
                sleep(1)
            set_status("Running...")
            sleep(5)
        #posid = caget("u171dcm1:PH_0_GETN", type='i')
        #if posid==4:
        #    status="OK"
        #else:
        #    status="error"
        pos = caget("u171dcm1:PH_0_GET")
        err=abs(0-pos)
        if err < 5.0:
            status="OK"
        else:
            status="error"

        print("{0:.<17}[{1:^6}]".format("DCM",status))
        # PGM mirror
        if caget("u171pgm1:axis3:running", type='i'):
            set_status("Waiting for PGM to finish motion...")
            while(caget("u171pgm1:axis3:running", type='i')):
                sleep(1)
            set_status("Running...")
            sleep(5)
        #posid = caget("u171pgm1:PH_0_GETN", type='i')
        #if posid==2:
        #    status="OK"
        #else:
        #    status="error"
        pos = caget("u171pgm1:PH_0_GET")
        err=abs(770-pos)
        if err < 5.0:
            status="OK"
        else:
            status="error"

        print("{0:.<17}[{1:^6}]".format("PGM",status))

    def check_m1(self, params):
        #return
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
                set_status("Waiting for filter foil to finish motion...")
                while(caget("u171dcm1:axis8:running", type='i')):
                    sleep(1)
                set_status("Running...")
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
                    rbvpos = caget("PINK:AU1:apertureY_RBV")
                    err=abs(rbvpos-pos)
                    if err>dead_band:
                        status="error"
                        log("[BL setup] Error on AU1 gap Y")
                except:
                    status="error"
                    log("[BL setup] Error while checking AU1 gap Y")
            if params.has_key("au1gapx"):
                pos = params["au1gapx"]
                try:
                    rbvpos = caget("PINK:AU1:apertureX_RBV")
                    err=abs(rbvpos-pos)
                    if err>dead_band:
                        status="error"
                        log("[BL setup] Error on AU1 gap X")
                except:
                    status="error"
                    log("[BL setup] Error while checking AU1 gap X")

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
                    rbvpos = caget("PINK:AU2:apertureY_RBV")
                    err=abs(rbvpos-pos)
                    if err>dead_band:
                        status="error"
                        log("[BL setup] Error on AU2 gap Y")
                except:
                    status="error"
                    log("[BL setup] Error while checking AU2 gap Y")
            if params.has_key("au2gapx"):
                pos = params["au2gapx"]
                try:
                    rbvpos = caget("PINK:AU2:apertureX_RBV")
                    err=abs(rbvpos-pos)
                    if err>dead_band:
                        status="error"
                        log("[BL setup] Error on AU2 gap X")
                except:
                    status="error"
                    log("[BL setup] Error while checking AU2 gap X")

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
                    rbvpos = caget("PINK:AU3:apertureY_RBV")
                    err=abs(rbvpos-pos)
                    if err>dead_band:
                        status="error"
                        log("[BL setup] Error on AU3 gap Y")
                except:
                    status="error"
                    log("[BL setup] Error while checking AU3 gap Y")
            if params.has_key("au3gapx"):
                pos = params["au3gapx"]
                try:
                    rbvpos = caget("PINK:AU3:apertureX_RBV")
                    err=abs(rbvpos-pos)
                    if err>dead_band:
                        status="error"
                        log("[BL setup] Error on AU3 gap X")
                except:
                    status="error"
                    log("[BL setup] Error while checking AU3 gap X")

            print("{0:.<17}[{1:^6}]".format("AU3",status))

    def check_m2(self, params):
        if params.has_key("m2group") or params.has_key("m2poix") or params.has_key("m2poiy") or params.has_key("m2tx") or params.has_key("m2ty") or params.has_key("m2tz") or params.has_key("m2rx") or params.has_key("m2ry") or params.has_key("m2rz"):
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
                except:
                    log("[BL setup] Error while checking M2 mirror group") 

            if params.has_key("m2poix"):
                pos = params["m2poix"]
                try:
                    rbvpos = caget("HEX2OS12L:multiaxis:getPOIx")
                    if rbvpos!=pos:
                        status = "error"
                        log("[BL setup] M2 POI X does not match")
                except:
                    log("[BL setup] Error while checking M2 POI X")
            if params.has_key("m2poiy"):
                pos = params["m2poiy"]
                try:
                    rbvpos = caget("HEX2OS12L:multiaxis:getPOIy")
                    if rbvpos!=pos:
                        status = "error"
                        log("[BL setup] M2 POI Y does not match")
                except:
                    log("[BL setup] Error while checking M2 POI Y")
                    
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
                        status = "error"
                        log("[BL setup] M2 Tx does not match")
                except:
                    log("[BL setup] Error checking moving M2 Tx")                    
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
                        status = "error"
                        log("[BL setup] M2 Ty does not match")
                except:
                    log("[BL setup] Error checking moving M2 Ty")
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
                        status = "error"
                        log("[BL setup] M2 Tz does not match")
                except:
                    log("[BL setup] Error checking moving M2 Tz")
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
                        status = "error"
                        log("[BL setup] M2 Rx does not match")
                except:
                    log("[BL setup] Error checking moving M2 Rx")                      
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
                        status = "error"
                        log("[BL setup] M2 Ry does not match")
                except:
                    log("[BL setup] Error checking moving M2 Ry")
            if params.has_key("m2rx"):
                pos = params["m2rz"]
                if params.has_key("m2deltarz"):
                    dpos = params["m2deltarz"]
                else:
                    dpos = 0
                try:
                    rbvpos = caget("HEX2OS12L:hexapod:getReadPoseC")
                    errpos = abs(rbvpos-pos)
                    if errpos>dpos:
                        status = "error"
                        log("[BL setup] M2 Rz does not match")
                except:
                    log("[BL setup] Error checking moving M2 Rz")     
                    
            print("{0:.<17}[{1:^6}]".format("M2",status))

    def check_bpm1(self, params):
        if params.has_key("cross1x") or params.has_key("cross1y"):
            status = "OK"
            if params.has_key("cross1x"):
                pos = params["cross1x"]
                try:
                    rbvpos = caget("PINK:PG01:Over1:5:CenterX_RBV")
                    if rbvpos!=pos:
                        status = "error"
                        log("[BL setup] BPM1 cross X does not match")
                except:
                    log("[BL setup] Error while checking BPM 1 cross X")
            if params.has_key("cross1y"):
                pos = params["cross1y"]
                try:
                    rbvpos = caget("PINK:PG01:Over1:5:CenterY_RBV")
                    if rbvpos!=pos:
                        status = "error"
                        log("[BL setup] BPM1 cross Y does not match")
                except:
                    log("[BL setup] Error while checking BPM 1 cross Y")
            print("{0:.<17}[{1:^6}]".format("BPM1",status))

    def check_bpm2(self, params):
        if params.has_key("cross2x") or params.has_key("cross2y"):
            status = "OK"
            if params.has_key("cross2x"):
                pos = params["cross2x"]
                try:
                    rbvpos = caget("PINK:PG04:Over1:5:CenterX_RBV")
                    if rbvpos!=pos:
                        status = "error"
                        log("[BL setup] BPM2 cross X does not match")
                except:
                    log("[BL setup] Error while checking BPM 2 cross X")
            if params.has_key("cross2y"):
                pos = params["cross2y"]
                try:
                    rbvpos = caget("PINK:PG04:Over1:5:CenterY_RBV")
                    if rbvpos!=pos:
                        status = "error"
                        log("[BL setup] BPM2 cross Y does not match")
                except:
                    log("[BL setup] Error while checking BPM 2 cross Y")        
            print("{0:.<17}[{1:^6}]".format("BPM2",status))

    def check_bpm3(self, params):
        if params.has_key("cross3x") or params.has_key("cross3y"):
            status = "OK"
            if params.has_key("cross3x"):
                pos = params["cross3x"]
                try:
                    rbvpos = caget("PINK:PG03:Over1:5:CenterX_RBV")
                    if rbvpos!=pos:
                        status = "error"
                        log("[BL setup] BPM3 cross X does not match")
                except:
                    log("[BL setup] Error while checking BPM 3 cross X")
            if params.has_key("cross3y"):
                pos = params["cross3y"]
                try:
                    rbvpos = caget("PINK:PG03:Over1:5:CenterY_RBV")
                    if rbvpos!=pos:
                        status = "error"
                        log("[BL setup] BPM3 cross Y does not match")
                except:
                    log("[BL setup] Error while checking BPM 3 cross Y")          
            print("{0:.<17}[{1:^6}]".format("BPM3",status))

    
