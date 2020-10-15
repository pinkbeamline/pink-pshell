# test task
counter = 700
print("begin...")
for i in range(20):
    counter = counter+1
    #print("B: {:d}".format(BATCH))
    msg = "[B]: {:03d}".format(counter)
    elab.put(msg)
print("...end")
