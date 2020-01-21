class MLMIRROR():

    def set(self, energy=0):
        log("{mlmirror.py} set")
        
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

    def __movemirror(self, params):
        log("{mlmirror.py} __movemirror")

        #channels

        #Simulation channels
        MGROUP = create_channel_device("PINK:MSIM2:m1")
        MTX = create_channel_device("PINK:MSIM2:m1")
        MTY = create_channel_device("PINK:MSIM2:m2")
        MTX = create_channel_device("PINK:MSIM2:m1")
        #continue        
        
        
        print(params)