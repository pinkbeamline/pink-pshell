## U17AU1 apperture functions

class U17AU1():
    def move(self, top=None, bottom=None, wall=None, ring=None):
        #variables
        cell_width = 11
        cell_border = "|"
        motor_deadband = 0.1

        #EPICS pvs
        top_app = create_channel_device("WAUY02U012L:AbsM1")
        top_app_RBV = create_channel_device("WAUY02U012L:rdPosM1")
        top_app_RBV.setMonitored(True)
        bottom_app = create_channel_device("WAUY02U012L:AbsM2")
        bottom_app_RBV = create_channel_device("WAUY02U012L:rdPosM2")
        bottom_app_RBV.setMonitored(True)
        wall_app = create_channel_device("WAUY02U012L:AbsM3")
        wall_app_RBV = create_channel_device("WAUY02U012L:rdPosM3")
        wall_app_RBV.setMonitored(True)
        ring_app = create_channel_device("WAUY02U012L:AbsM4")
        ring_app_RBV = create_channel_device("WAUY02U012L:rdPosM4")
        ring_app_RBV.setMonitored(True)

        ##### Just grab values and print
        if (top==None) and (bottom==None) and (wall==None) and (ring==None):
            sensor = 0

            print(cell_border+"TOP".center(cell_width)+cell_border+"BOTTOM".center(cell_width)+cell_border+"WALL".center(cell_width)+cell_border+"RING".center(cell_width)+cell_border+"Gap V".center(cell_width)+cell_border+"Center V".center(cell_width)+cell_border+"Gap H".center(cell_width)+cell_border+"Center H".center(cell_width)+cell_border+"Izero".center(cell_width)+cell_border)

            gapv = abs(top_app_RBV.read()-bottom_app_RBV.read())
            gaph = abs(wall_app_RBV.read()-ring_app_RBV.read())
            centerv = (top_app_RBV.read()+bottom_app_RBV.read())/2
            centerh = (wall_app_RBV.read()+ring_app_RBV.read())/2

            print(cell_border+'{:.3f}'.format(top_app_RBV.read()).center(cell_width)+
            cell_border+'{:.3f}'.format(bottom_app_RBV.read()).center(cell_width)+
            cell_border+'{:.3f}'.format(wall_app_RBV.read()).center(cell_width)+
            cell_border+'{:.3f}'.format(ring_app_RBV.read()).center(cell_width)+
            cell_border+'{:.3f}'.format(gapv).center(cell_width)+
            cell_border+'{:.3f}'.format(centerv).center(cell_width)+
            cell_border+'{:.3f}'.format(gaph).center(cell_width)+
            cell_border+'{:.3f}'.format(centerh).center(cell_width)+
            cell_border+'{:.1e}'.format(sensor).center(cell_width)+cell_border)
            return

        #### Move necessary motors
        ## Check ampmeter
        if caget("PINK:AUX:CAE2VALID")<1:
            print("Setting up ampmeter...")
            caput("PINK:CAE2:TriggerMode", 0)
            caput("PINK:CAE2:AcquireMode", 0)
            caput("PINK:CAE2:ValuesPerRead", 1000)
            caput("PINK:CAE2:AveragingTime", 1)
            sleep(1)
            caputq("PINK:CAE2:Acquire", 1)
            sleep(1)

        ## Move apertures
        print("Moving appertures...")

        ## simulation
        # caputq("PINK:MSIM2:m1.VAL", top)
        # caputq("PINK:MSIM2:m2.VAL", bottom)
        # caputq("PINK:MSIM2:m3.VAL", wall)
        # caputq("PINK:MSIM2:m4.VAL", ring)

        ## real motors
        if top!=None:
            top_app.write(top)
        if bottom!=None:
            bottom_app.write(bottom)
        if wall!=None:
            wall_app.write(wall)
        if ring!=None:
            ring_app.write(ring)

        notready=True
        tbegin = time.clock()

        try:
            while(notready):
                alldone = self.ismotordone(top, top_app_RBV, motor_deadband) and (
                self.ismotordone(bottom, bottom_app_RBV, motor_deadband)) and (
                self.ismotordone(wall, wall_app_RBV, motor_deadband)) and (
                self.ismotordone(ring, ring_app_RBV, motor_deadband))

                if alldone:
                    notready = False
                    sleep(2)
                else:
                    telapse = time.clock()-tbegin
                    #mystat = "Time elapse: " + '{:.1f}'.format(telapse) + " seconds"
                    mystat = "top: " + '{:.3f}'.format(top_app_RBV.take())+" bottom: " + '{:.3f}'.format(bottom_app_RBV.take())+" wall: " + '{:.3f}'.format(wall_app_RBV.take())+" ring: " + '{:.3f}'.format(ring_app_RBV.take())
                    set_status(mystat)
                    sleep(1)
        except:
            pass

        print("all done..\n")

        sensor = caget("PINK:CAE2:SumAll:MeanValue_RBV")

        print(cell_border+"TOP".center(cell_width)+
        cell_border+"BOTTOM".center(cell_width)+
        cell_border+"WALL".center(cell_width)+
        cell_border+"RING".center(cell_width)+
        cell_border+"Gap V".center(cell_width)+
        cell_border+"Center V".center(cell_width)+
        cell_border+"Gap H".center(cell_width)+
        cell_border+"Center H".center(cell_width)+
        cell_border+"Izero".center(cell_width)+
        cell_border)

        gapv = abs(top_app_RBV.read()-bottom_app_RBV.read())
        gaph = abs(wall_app_RBV.read()-ring_app_RBV.read())
        centerv = (top_app_RBV.read()+bottom_app_RBV.read())/2
        centerh = (wall_app_RBV.read()+ring_app_RBV.read())/2

        print(cell_border+'{:.3f}'.format(top_app_RBV.read()).center(cell_width)+
        cell_border+'{:.3f}'.format(bottom_app_RBV.read()).center(cell_width)+
        cell_border+'{:.3f}'.format(wall_app_RBV.read()).center(cell_width)+
        cell_border+'{:.3f}'.format(ring_app_RBV.read()).center(cell_width)+
        cell_border+'{:.3f}'.format(gapv).center(cell_width)+
        cell_border+'{:.3f}'.format(centerv).center(cell_width)+
        cell_border+'{:.3f}'.format(gaph).center(cell_width)+
        cell_border+'{:.3f}'.format(centerh).center(cell_width)+
        cell_border+'{:.1e}'.format(sensor).center(cell_width)+
        cell_border)

        #pink_save_bl_snapshot()

        print("\nDone. OK")

    def ismotordone(self, pos, RBV, deadband):
        if pos == None:
            return True

        motorerr = abs(pos-RBV.read())
        if motorerr<=abs(deadband):
            return True
        else:
            return False
