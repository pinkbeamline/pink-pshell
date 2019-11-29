#!/usr/bin/python3

import sys
import os.path
import h5py

argnum = len(sys.argv)
#print("argnum: "+str(argnum))
status = 1

if len(sys.argv)<4:
    print('Error: not enough arguments')
    status=0

if status:
    fname = sys.argv[1]
    dataset = sys.argv[2]
    newdata = sys.argv[3]
    for i in range(4,argnum):
        newdata = newdata+' '+sys.argv[i]

    #print("newdata: "+newdata)
    dtype = "S"+str(int(len(newdata)))
    #print(dtype)

    #fpath = "/home/epics/PShell/pshellcontrol/home/data/"+fname
    fpath = "/home/epics/PShell/pink-pshell/data/"+fname
    if(os.path.exists(fpath)==False):
        print("Error: File does not exist")
        status=0

if status:
    try:
        f1 = h5py.File(fpath, 'r+')
        del f1[dataset]
        data = f1.create_dataset(dataset, (1,), dtype=dtype)
        data[...]=newdata.encode()
        f1.close()
    except:
        print("Error: Could not write new data")
        status=0

if status:
    print("OK")