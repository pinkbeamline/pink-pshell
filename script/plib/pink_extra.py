## PINK Extra functions

def pink_save_bl_snapshot():
    import config.bl_snapshot_config as pcfg

    for dat in pcfg.snapshot_pvlist:
        try:
            pval = caget(dat[1])
        except:
            print("PV is unreachable: " + dat[1])
            pval = "----"
        save_dataset(dat[0], pval)

def linspace(start, end, step):
    if type(step)==type(int(0)):
        step = abs(step)
        N = int(abs(step))
        ds = float((end-start))/(step-1)
    else:
        N = abs(int(math.floor((end-start)/step)))+1
        ds = abs(step)
        if end-start < 0:
            ds = -1*ds
    resp = [start+(i*ds) for i in range(N)]
    return resp        

# ******** Pseudo Devices ************

class Array2Matrix(ReadonlyRegisterBase, ReadonlyRegisterMatrix):
    def __init__(self, name, src_array, src_width, src_height):
        ReadonlyRegisterBase.__init__(self, name)
        self.src_array = src_array
        self.src_width = src_width
        self.src_height = src_height

    def doRead(self):
        data = self.src_array.take()
        h = self.getHeight()
        w = self.getWidth()
        ret = Convert.reshape(data, h, w)
        return ret

    def getWidth(self):
        return int(self.src_width.take())

    def getHeight(self):
        return int(self.src_height.take())

##add_device(Array2Matrix("GE_BG_Image", GE_BG_Array, GE_BG_SizeX, GE_BG_SizeY), True)
##sleep(1)
##GE_BG_Image.read()