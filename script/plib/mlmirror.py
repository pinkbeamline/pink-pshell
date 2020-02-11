class MLMIRROR():

    ###   set function     ######################################
    def set(self, energy=0):
        log("{mlmirror.py} function: set")
        #check input
        try:
            energy = int(energy)
        except:
            print("Invalid energy input")
            return

        ## load lines from file
        try:
            fp = open("pink-pshell/script/config/mirror.py")
            lines = fp.readlines()
            fp.close()
        except:
            print("error reading configuration file: {pink-pshell/script/config/mirror.py}")
            return

        ## set variables
        matched = False
        params = {}

        ## look for energy settings and parse settings
        for line in lines:
            lpars = [x.split() for x in line.split('=')]
            if matched:
                if lpars[0]==['energy']:
                    break
                else:
                    if len(lpars)>1:
                        if len(lpars[0])>0 and len(lpars[1])>0:
                            pkey = lpars[0][0]
                            pvalue = lpars[1][0]
                            try:
                                pvalue = float(pvalue)
                                params[pkey]=pvalue
                            except:
                                pass
            else:
                if lpars[0]==['energy']:
                    if len(lpars)>1:
                        nrgstr = lpars[1]
                        if len(nrgstr)>0:
                            nrgstr = nrgstr[0]
                            if int(nrgstr)==energy:
                                matched = True

        if matched:
            self.__movemirror(params)
        else:
            print("No configuration found")

    ###   movemirror function     ######################################
    def __movemirror(self, params):
        log("{mlmirror.py} function: __movemirror")
        #print(params)

        ## first move to the target mirror group
        if params.has_key("group"):
            print("\n*** Mirror Group ***")
            self.__movegroup(params["group"])

        ## disable start immedialely and set values
        print("\n*** Mirror Pose ***")
        print("Setting mirror position. This may take a few seconds...")
        caput("HEX2OS12L:hexapod:mbboRunAfterValue", 1)
        sleep(1)

        if params.has_key("tx"):
            val = params["tx"]
            print("Tx: " + str(val))
            caput("HEX2OS12L:hexapod:setPoseX", val)
        if params.has_key("ty"):
            val = params["ty"]
            print("Ty: " + str(val))
            caput("HEX2OS12L:hexapod:setPoseY", val)
        if params.has_key("tz"):
            val = params["tz"]
            print("Tz: " + str(val))
            caput("HEX2OS12L:hexapod:setPoseZ", val)
        if params.has_key("rx"):
            val = params["rx"]
            print("Rx: " + str(val))
            caput("HEX2OS12L:hexapod:setPoseA", val)
        if params.has_key("ry"):
            val = params["ry"]
            print("Ry: " + str(val))
            caput("HEX2OS12L:hexapod:setPoseB", val)
        if params.has_key("rz"):
            val = params["rz"]
            print("Rz: " + str(val))
            caput("HEX2OS12L:hexapod:setPoseC", val)

        ## execute target pose
        sleep(1)
        caput("HEX2OS12L:multiaxis:run", 1)
        ## wait for running status
        sleep(1)
        while(caget("HEX2OS12L:multiaxis:running")):
            eta = caget("HEX2OS12L:multiaxis:mvtm")
            print("ETA: " + '{:.3f}'.format(eta) + " sec")
            sleep(1)
        sleep(1)
        caput("HEX2OS12L:hexapod:mbboRunAfterValue", 0)
        print("Mirror in position.")

        ## move gap to desire postion
        if params.has_key("gap"):
            print("\n*** Undulator gap ***")
            print("Changing undulator gap:")
            val = params["gap"]
            print("Gap: " + str(val))
            print("disabled on script!!!")
            pink.gap()


    ###   movegroup function     ######################################
    def __movegroup(self, group):
        log("{mlmirror.py} function: __movegroup")

        try:
            group = int(group)
        except:
            print("Invalid group.")
            return

        grouplabels = ["Optic ID#1", "Optic ID#2", "Optic ID#3"]
        epicsgroupid_array = [2, 1, 0]

        if (group >= 1) and (group <= 3):
            epicsgroup = epicsgroupid_array[int(group-1)]
        else:
            print("invalid mirror group number. [1-3]")
            return

        actualgroup = caget("HEX2OS12L:hexapod:mbboMirrorChoicerRun", 'i')
        if(epicsgroup != actualgroup):
            tout = 0
            while(caget("HEX2OS12L:multiaxis:running")):
                if tout%5==0:
                    print("Mirror is in use. Waiting! ( "+ str(tout) + " sec ) ")
                sleep(1)
                tout = tout+1
            print("Changing mirror to " + grouplabels[group-1] + ". Please wait. This takes a while...")
            print("Epics group: " + str(epicsgroup))
            caput("HEX2OS12L:hexapod:mbboMirrorChoicerRun", epicsgroup)
            sleep(1)
            while(caget("HEX2OS12L:multiaxis:running")):
                eta = caget("HEX2OS12L:multiaxis:mvtm")
                print("ETA: " + '{:.3f}'.format(eta) + " sec")
                sleep(1)
            sleep(1)
        print("Mirror group in position.")

