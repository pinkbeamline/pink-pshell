class PINKCLASS():

    #### SHOW BL SNAPSHOT   ############################################################
    def bl_snapshot_print(self):
        import config.bl_snapshot_config as pcfg
        pvl = pcfg.snapshot_pvlist
        header = []
        rows = []
        temprow = []
        colmaxwidth = 0
        for item in pvl:
            grp = item[0].split('/')
            sector = grp[0]
            L = len(sector)
            if L > colmaxwidth:
                colmaxwidth = L
            temprow.append(sector)
        for i, row in enumerate(temprow):
            rows.append([row.ljust(colmaxwidth+1)])
        header.append('Sector'.ljust(colmaxwidth+1))
        temprow = []
        colmaxwidth = 0
        for item in pvl:
            grp = item[0].split('/')
            device = grp[1]
            L = len(device)
            if L > colmaxwidth:
                colmaxwidth = L
            temprow.append(device)
        for i, row in enumerate(temprow):
            rows[i].append(row.ljust(colmaxwidth+1))
        header.append('Device'.ljust(colmaxwidth+1))
 
        for i, item in enumerate(pvl):
            #print(item[1])
            pvdisconnected=False
            try:
                val = caget(item[1])
            except:
                pvdisconnected=True
                ##print("PV does not respond >>  " + item[1])
            if pvdisconnected: val = unicode('-----')
            if isinstance(val, unicode):
                rows[i].append(val)
            else:
                rows[i].append('{:.3f}'.format(val))
        header.append('Value')
        print("| "+header[0]+" | "+header[1]+" | "+header[2])
        for row in rows:
            print("| "+row[0]+" | "+row[1]+" | "+row[2])
        print("OK")

    #### SAVE BL SNAPSHOT   ############################################################
    def bl_snapshot_save(self):
        set_exec_pars(open=False, name="pink_bl", reset=True)
        pink_save_bl_snapshot()
        print("Pink beamline snapshot saved")

    #### Open hard shutter  ############################################################
    def shutter_hard_OPEN(self):
        for i in range(3):
            shutter_status = caget("PSHY01U012L:State1", 'd')
            if shutter_status == 14:
                return True
            else:
                caputq("PSHY01U012L:SetTa", 1)
                sleep(3)
        print("Failed to open Shutter Hard")
        log("Failed to open Shutter Hard")
        return False

    #### Close hard shutter  ############################################################
    def shutter_hard_CLOSE(self):
        for i in range(3):
            shutter_status = caget("PSHY01U012L:State1", 'd')
            if shutter_status == 5 or shutter_status == 1:
                return True
            else:
                caputq("PSHY01U012L:SetTa", 1)
                sleep(3)
        print("Failed to close Shutter Hard")
        log("Failed to close Shutter Hard")
        return False

    #### Setup Pink Beamline  ############################################################
    def __pvwait(self, pvname, value, deadband=0, timeout=300):
        cdown=timeout
        while cdown>=0:
            val = caget(pvname)
            if (val>=value-abs(deadband)) and (val<=value+abs(deadband)):
                return
            cdown=cdown-1
            sleep(1)
        print("Timeout (" + str(timeout) + " seconds) waiting for PV: " + pvname)

    def bl_set(self):
        import config.bl_setup_config as pcfg

        resp = get_option("Setup PINK beamline will move multiples devices. Are you sure?", type='OkCancel')

        if resp == 'Yes':
            for tsk in task_list:
                grp = tsk[0]
                resp = get_option(tsk[3], type='YesNo')
                if resp == "Yes":
                    print(tsk[1])
                    for mpv in grp:
                        caputq(mpv[0],mpv[1])
                    for mpv in grp:
                        self.__pvwait(mpv[2], mpv[1], deadband=mpv[3], timeout=mpv[4])
                    print(tsk[2])
        else:
            print("PINK Setup canceled")

    #### Move Filters  ############################################################
    def filter1(self, pos):
        caput("PINK:SMA01:m0.VAL", float(pos))

    def filter2(self, pos):
        caput("PINK:SMA01:m1.VAL", float(pos))

    def filter3(self, pos):
        caput("PINK:SMA01:m2.VAL", float(pos))

    #### Open/Close valves  ############################################################
    def valveOPEN(self,vnum):
        dev = None
        if type(vnum) is str:
            print('Enter valve number. Ex: valveOPEN(29)')
            return "Invalid input"
        if (vnum>=10 and vnum<=18) or (vnum>=31 and vnum<=34):
            dev="PLCVAC"
        elif (vnum>=19 and vnum<=29) or (vnum>=40 and vnum<=43):
            dev="PLCGAS"
        if dev != None:
            vpv = "PINK:"+dev+":V"+str(int(vnum))+"open"
            caput(vpv,1)
            print("OK")
        else:
            print("Valve number is invalid")

    def valveCLOSE(self,vnum):
        dev = None
        if type(vnum) is str:
            print('Enter valve number. Ex: valveOPEN(29)')
            return "Invalid input"
        if (vnum>=10 and vnum<=18) or (vnum>=31 and vnum<=34):
            dev="PLCVAC"
        elif (vnum>=19 and vnum<=29) or (vnum>=40 and vnum<=43):
            dev="PLCGAS"
        if dev != None:
            vpv = "PINK:"+dev+":V"+str(int(vnum))+"close"
            caput(vpv,1)
            print("OK")
        else:
            print("Valve number is invalid")

    #### Edit dataset on HDF5 file  ############################################################
    def rename_sample(self, path, newstring):
        path = path.split('|')
        if len(path)!=2:
            print("Path incomplete")
            return 1

        spath = get_exec_pars()
        spath = spath.path
        spath = spath.split('data')
        spath = spath[0]
        argstr = (spath + "script/plib/h5edit.py "+path[0]+" "+path[1]+" "+newstring)
        res=exec_cmd(argstr)
        return(res)

    #### Set undulator gap  ############################################################
    def gap(self, *val):
        if len(val)==0:
            gapval = caget("U17IT6R:BasePmGap.A")
            print("Undulator U17 gap: " + str(gapval))
            return
        else:
            pos = float(val[0])

        lockstatus=caget("U17IT6R:BaseCmdHmLock")
        ## 0:free / 1:locked
        if lockstatus>0:
            print("Abort: Undulator is locked")
            return

        ##channels
        #MOTOR = create_channel_device("U17IT6R:BaseParGapsel.B")
        #MOTOR_SET = create_channel_device("U17IT6R:BaseCmdCalc.PROC")
        #MOTOR_RBV = create_channel_device("U17IT6R::BasePmGap.A")
        #MOTOR_RBV.setMonitored(True)   
        #motor_deadband = 2.0

        ## simulated channels
        MOTOR = create_channel_device("PINK:GAPSIM:gapset")
        MOTOR_SET = create_channel_device("PINK:GAPSIM:gapexec.PROC")
        MOTOR_RBV = create_channel_device("PINK:GAPSIM:m1.RBV")
        MOTOR_RBV.setMonitored(True)   
        motor_deadband = 0.1

        ## variables
        verbose = True
        start=float(MOTOR_RBV.read())
        end=pos
        sensor = []

        ## plot setup
        if verbose: print("Setup plot")
        [p1] = plot(None, "Gap", title="Gap Motion")
        #p1.getAxis(p1.AxisId.X).setRange(min(start, end),max(start,end))
        p1.getAxis(p1.AxisId.Y).setRange(min(start, end),max(start,end))
        sensor.append(MOTOR_RBV.take())
        MOTOR.write(pos)
        MOTOR_SET.write(1)
        while(abs(pos-MOTOR_RBV.take()) > motor_deadband):
            #mystat = "Gap: " + str(MOTOR_RBV.take())
            ##set_status(mystat)
            sensor.append(MOTOR_RBV.take())
            p1.getSeries(0).setData(sensor, sensor)
            sleep(0.5)

        return

    #### Multi player mirror positioning  ############################################################
    def ml_2300ev(self):
        run("plib/mlmirror")
        ml = MLMIRROR()
        ml.set(energy=2300)

    def ml_3000ev(self):
        run("plib/mlmirror")
        ml = MLMIRROR()
        ml.set(energy=3000)

    def ml_4000ev(self):
        run("plib/mlmirror")
        ml = MLMIRROR()
        ml.set(energy=4000)

    def ml_5000ev(self):
        run("plib/mlmirror")
        ml = MLMIRROR()
        ml.set(energy=5000)

    def ml_6300ev(self):
        run("plib/mlmirror")
        ml = MLMIRROR()
        ml.set(energy=6300)

    def ml_6800ev(self):
        run("plib/mlmirror")
        ml = MLMIRROR()
        ml.set(energy=6800)

    def ml_7300ev(self):
        run("plib/mlmirror")
        ml = MLMIRROR()
        ml.set(energy=7300)

    def ml_8000ev(self):
        run("plib/mlmirror")
        ml = MLMIRROR()
        ml.set(energy=8000)

    def ml_9500ev(self):
        run("plib/mlmirror")
        ml = MLMIRROR()
        ml.set(energy=9500)


#        def ml_2300ev(self):
#            layer = 8
#            self.__movemirror(layer)
#    
#        def ml_3000ev(self):
#            layer = 7
#            self.__movemirror(layer)
#    
#        def ml_4000ev(self):
#            layer = 6
#            self.__movemirror(layer)
#    
#        def ml_5000ev(self):
#            layer = 5
#            self.__movemirror(layer)
#    
#        def ml_6300ev(self):
#            layer = 4
#            self.__movemirror(layer)
#    
#        def ml_6800ev(self):
#            layer = 3
#            self.__movemirror(layer)
#    
#        def ml_7300ev(self):
#            layer = 2
#            self.__movemirror(layer)
#    
#        def ml_8000ev(self):
#            layer = 1
#            self.__movemirror(layer)
#    
#        def ml_9500ev(self):
#            layer = 0
#            self.__movemirror(layer)
#    
#        def __movemirror(self,layer):
#            group = self.m2poslist[layer][3]
#            pos = self.m2poslist[layer][2]
#            try:
#                self.__movegroup(group)
#                self.__movelayer(pos)
#                print("Mirror Ready. OK")
#            except:
#                print("Error moving mirror or operation canceled")
#    
#        def __movegroup(self, group):
#            grouplabels = ["Optic ID#3", "Optic ID#2", "Optic ID#1"]
#            actualgroup = caget("HEX2OS12L:hexapod:mbboMirrorChoicerRun", 'i')
#            if(group != actualgroup):
#                tout = 0
#                while(caget("HEX2OS12L:multiaxis:running")):
#                    if tout%5==0:
#                        print("Mirror is in use. Waiting! ( "+ str(tout) + " sec ) ")
#                    sleep(1)
#                    tout = tout+1
#                print("Changing mirror to " + grouplabels[group]+". Please wait. This takes a while...")
#                caput("HEX2OS12L:hexapod:mbboMirrorChoicerRun", group)
#                sleep(1)
#                while(caget("HEX2OS12L:multiaxis:running")):
#                    sleep(1)
#                sleep(1)
#    
#        def __movelayer(self, pos):
#            while(caget("HEX2OS12L:multiaxis:running")):
#                if tout%5==0:
#                    print("Mirror is in use. Waiting! ( "+ str(tout) + " sec ) ")
#                sleep(1)
#                tout = tout+1
#            print("Moving mirror to Tx: "+str(pos)+". Please wait. This takes a while...")
#            caput("HEX2OS12L:hexapod:setPoseX", pos)
#            sleep(1)
#            while(caget("HEX2OS12L:multiaxis:running")):
#                sleep(1)
#            sleep(1)
#    
    ####################################################################################
    #### Internal Functions ############################################################
    ####################################################################################

#    def __ge_setup_file(self, fname="ge"):
#        set_exec_pars(open=False, name=fname, reset=True)

#    def __publish_status(self, message):
#        set_status(message)
