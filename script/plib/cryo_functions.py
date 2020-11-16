class CRYOFUN():
    def sample_number(self, num):
        if (num<1 or num>8):
            print("Invalid holder number. Valid numbers are 1 to 8")
            return
        else:
            print("Moving to sample {:d}".format(num))
            caput("PINK:CRYO:samplenumber", (num-1))
            sleep(1)
            print("Waiting for holder in position...")
            notdone=True
            while(notdone):
                dmov = int(caget("PINK:PHY:AxisJ.DMOV"))
                notdone = (dmov == 0 )
                sleep(1)
            print("OK")
        return

    def sample_X(self, pos):
        pass
        caput("PINK:CRYO:samplex", pos)
        return
    def sample_Y(self, pos):
        pass
        caput("PINK:CRYO:sampley", pos)
        return
