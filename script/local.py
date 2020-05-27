###################################################################################################
#  Deployment specific global definitions - executed after startup.py
###################################################################################################
from plib.logger_class import MasterLogger

run("plib/bpm_class.py")
run("plib/pink_extra.py")
run("plib/pink_class.py")
run("plib/blade_func.py")
run("plib/scan_func.py")

mlogger = MasterLogger()

bpm = BPM()
pink = PINKCLASS()
blade = BLADEFUNC()
scan = SCANFUNC()
detector = DETEC()
slit = SLITS()
filters = FILTERS()
diode = DIODE()
axis = SAMPLEAXIS()

print("PShell v1.14")
#print("OK")

def on_command_started(info):
    mlogger.onstart(info)

def on_command_finished(info):
    mlogger.onend(info)
