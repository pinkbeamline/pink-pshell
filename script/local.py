###################################################################################################
#  Deployment specific global definitions - executed after startup.py
###################################################################################################

run("plib/bpm_class.py")
run("plib/pink_extra.py")
run("plib/pink_class.py")
run("plib/blade_func.py")

bpm = BPM()
pink = PINKCLASS()
blade = BLADEFUNC()

print("OK")
