class BLSETUP():
    ###   set function     ######################################
    def set(self, energy=0):
        #log("{mlmirror.py} function: set")
        #check input
        try:
            energy = int(energy)
        except:
            print("Invalid energy input")
            return

        ## create filename
        fname = "/home/epics/PShell/pink-pshell/script/config/e{:d}.py".format(energy)
        
        ## load lines from file
        try:
            #fp = open("pink-pshell/script/config/mirror.py")
            fp = open(fname)
            lines = fp.readlines()
            fp.close()
        except:
            raise Exception("Could not open configuration file: {}".format(fname))

        ## set variables
        matched = False
        params = {}

        ## look for energy settings and parse settings
        for line in lines:
            # ignore comments
            if len(line.strip())>0:
                if (line.strip()[0])=="#":
                    continue
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
            #self.__movemirror(params)
            #print(params)
            run("plib/blsetup_set")
            blset = BLSETUPSET()
            blset.set(params, energy)
        else:
            print("No configuration found")
