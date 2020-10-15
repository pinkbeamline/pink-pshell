from org.python.core.util import StringUtil
import Queue
import threading
import time

## PINK Extra functions
def pink_save_bl_snapshot():
    print("Saving beamline snapshot...")
    run("config/bl_snapshot_config.py")
    for spdev in snapshot_pvlist:
        try:
            pval = caget(spdev[1])
        except:
            msg = "[snapshot]: caget failed for PV: " + spdev[1]
            print(msg)
            log(msg, data_file = True)
            pval = "----"
        save_dataset(spdev[0], pval)

def linspace(start, end, step):
    if start==end:
        return [start]
    if type(step)==type(int(0)):
        if step<2:
            return[start]
        step = abs(step)
        N = int(abs(step))
        ds = float((end-start))/(step-1)
    else:
        if step==0.0:
            return [start]
        N = abs(int(math.floor(abs((end-start)/step))))+1
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

class ELAB():
    from org.python.core.util import StringUtil
    #import Queue
    
    def __init__(self):
        def post_thread(self):
            #print("ELAB post thread has started.")
            print("..")
            while(True):
                self.__post()
                time.sleep(5)
            
        self.debug = False
        self.qbuff = Queue.Queue(100)
        self.ready = False
        self.busy = False
        try:
            self.postpv = create_channel_device("PINK:SESSION:elab_queue", type='[b',size=2048)
            self.ready=True
        except:
            self.ready=False
        ## thread
        self.pt = threading.Thread(target=post_thread, args=(self,))
        self.pt.start()
        
    def put(self, msg):
        if self.qbuff.full()==False:
            self.qbuff.put_nowait(msg)

    def __post(self):
        if (self.ready):
            while self.qbuff.qsize():
                msg = self.qbuff.get()
                #print("[->] " + msg)
                try:
                    self.postpv.write(StringUtil.toBytes(msg))
                except:
                    pass
                sleep(0.250)
        else:
            while self.qbuff.qsize():
                discard = self.qbuff.get()
                