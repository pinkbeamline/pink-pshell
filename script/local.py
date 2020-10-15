###################################################################################################
#  Deployment specific global definitions - executed after startup.py
###################################################################################################
from plib.logger_class import MasterLogger

run("plib/bpm_class.py")
run("plib/pink_extra.py")
run("plib/pink_class.py")
run("plib/blade_func.py")
run("plib/scan_func.py")
run("plib/sim_functions.py")

#mlogger = MasterLogger()

bpm = BPM()
pink = PINKCLASS()
blade = BLADEFUNC()
scan = SCANFUNC()
detector = DETEC()
slit = SLITS()
filters = FILTERS()
source = SOURCES()
axis = SAMPLEAXIS()
sim = SIMFUNC()

#global elab
elab = ELAB()
sleep(1)
mlogger = MasterLogger(elab)

#start_task("tests/elab_loop.py", delay=10.0)

#set_setting("chamber", "cryo")
#set_setting("chamber", "elec")

print("PShell v1.14")
#print("OK")
if(get_setting("chamber")=="cryo"):
    print("Scripts using Cryogenic SEC")
else:
    print("Scripts using Electro SEC")


def on_command_started(info):
    mlogger.onstart(info)

def on_command_finished(info):
    mlogger.onend(info)


#start_task("tests/elab_loop.py", delay=10.0)
