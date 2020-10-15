from org.python.core.util import StringUtil

ELB = create_channel_device("PINK:SESSION:elab_queue", type='[b',size=2048)

BATCH = BATCH+1
msg = "*** batch {:d} ***".format(BATCH)

#caput("PINK:SESSION:elab_queue",map(ord, msg))
ELB.write(StringUtil.toBytes(msg))

for i in range(5):
    msg = "L"+str(i)
    #caput("PINK:SESSION:elab_queue",map(ord, msg))
    ELB.write(StringUtil.toBytes(msg))
print("OK")

ELB.close()
del ELB