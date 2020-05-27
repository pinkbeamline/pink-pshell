### move ATM spec to stand by position to replace detector

class SPECSTDBY():
    def move(self):
        print("Moving detector to stand by position ...")

        #print("Code not finished.")

        #get_option("Move spectrometer to stand-by position?", type='OkCancel')

        #return

        ## variables
        vert_pos1 = 250.0
        horiz_end_pos = 470.0
        horiz_free_pos = 460.0
        rot_end_pos = 80.0
        vert_end_pos = 200.0

        ## EPICS pvs
        vert_motor_PV = "PINK:PHY:AxisL"
        horiz_motor_PV = "PINK:PHY:AxisK"
        rotation_motor_PV = "PINK:PHY:AxisM"

        ## Create channels
        motor_vert = create_channel_device(vert_motor_PV)
        motor_vert_RBV = create_channel_device(vert_motor_PV+".RBV")
        motor_vert_RBV.setMonitored(True)
        motor_vert_DMOV = create_channel_device(vert_motor_PV+".DMOV")
        motor_vert_DMOV.setMonitored(True)
        motor_horiz = create_channel_device(horiz_motor_PV)
        motor_horiz_RBV = create_channel_device(horiz_motor_PV+".RBV")
        motor_horiz_RBV.setMonitored(True)
        motor_horiz_DMOV = create_channel_device(horiz_motor_PV+".DMOV")
        motor_horiz_DMOV.setMonitored(True)
        motor_rotation = create_channel_device(rotation_motor_PV)
        motor_rotation_RBV = create_channel_device(rotation_motor_PV+".RBV")
        motor_rotation_RBV.setMonitored(True)
        motor_rotation_DMOV = create_channel_device(rotation_motor_PV+".DMOV")
        motor_rotation_DMOV.setMonitored(True)
        sleep(1)

        # move
        dist_vert = abs(vert_end_pos-vert_pos1)
        dist_horiz = abs(horiz_end_pos-motor_horiz_RBV.read())
        dist_rot = abs(rot_end_pos-motor_rotation_RBV.read())

        try:
            # move vert to pos 1
            print("Moving vertical motor...")
            motor_vert.write(vert_pos1)
            motor_vert_RBV.waitValueInRange(vert_pos1, 1.0, 60000)
            motor_vert_DMOV.waitValueInRange(1, 0.5, 5000)
            print("Vertical motor in lower position")

            # move horiz and wait to be past free position
            print("Moving horizontally...")
            motor_horiz.write(horiz_end_pos)
            motor_horiz_RBV.waitValueInRange(horiz_free_pos, 1.0, 60000)

            # once passed the free position, move other axis
            print("Moving other axis...")
            motor_vert.write(vert_end_pos)
            motor_rotation.write(rot_end_pos)

            notdone = True
            while(notdone):
                status_vert = '{:d}'.format(int(round((1-(abs(vert_end_pos-motor_vert_RBV.take())/dist_vert))*100)))+"%"
                status_horiz = '{:d}'.format(int(round((1-(abs(horiz_end_pos-motor_horiz_RBV.take())/dist_horiz))*100)))+"%"
                status_rot = '{:d}'.format(int(round((1-(abs(rot_end_pos-motor_rotation_RBV.take())/dist_rot))*100)))+"%"
                mymsg = "Spec ATM move status: |Vert: " + status_vert + "| |Horiz: " + status_horiz + "| |Rot: " + status_rot + "|"
                set_status(mymsg)
                notdone = (motor_vert_DMOV.read()<1) or (motor_horiz_DMOV.read()<1) or (motor_rotation_DMOV.read()<1)
                sleep(1)
            print("Spectrometer in stand by position")
        except:
            print("Failed moving motors. Stopping motors and aborting")
            notdone = True
            while(notdone):
                caput(vert_motor_PV+".STOP", 1)
                caput(horiz_motor_PV+".STOP", 1)
                caput(rotation_motor_PV+".STOP", 1)
                notdone = (motor_vert_DMOV.read()<1) or (motor_horiz_DMOV.read()<1) or (motor_rotation_DMOV.read()<1)
                sleep(1)
            print("All motors stopped.")
            return
        print("OK")
