###################################################################################################
#  Deployment specific global definitions - executed after startup.py
###################################################################################################

run("plib/bpm_class.py")
run("plib/pink_extra.py")
run("plib/pink_class.py")
run("plib/blade_func.py")
run("plib/scan_func.py")

bpm = BPM()
pink = PINKCLASS()
blade = BLADEFUNC()
scan = SCANFUNC()
detector = DETEC()
slit = SLITS()

print("PShell v13 - New Pink refactored version")
print("OK")
