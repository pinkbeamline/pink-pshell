## PINK Master logger class
import sys
import time
import os
from os import walk


class MasterLogger():
    def __init__(self):
        dpath = sys.path[0]
        dpath = dpath.split("script")
        self.data_path = dpath[0] + "data/"
        self.start_id = -1
        self.start_time = ""
        self.asctime = ""
        self.end_id = -2
        self.start_list = []
        self.end_list = []
        self.new_list = []
        self.script = None
        self.start_path = None
        self.end_path = None
        self.fullpath = ""
        self.status = "OK"

    def onstart(self, info):
        self.start_id = info.id
        if info.script != None:
            self.start_time = time.localtime()
            self.script = info.script
            self.start_path = self._makepath(self.data_path)
            #start_path_before = "/home/nilson/PShell/pshellcontrol/home/data/2018_09_0"
            self.start_list = []
            for (dirpath, dirnames, filenames) in walk(self.start_path):
                self.start_list.extend(filenames)

    def onend(self, info):
        self.end_id = info.id
        if info.script != None and self.end_id==self.start_id:
            self.end_path = self._makepath(self.data_path)
            #start_path_after = "/home/nilson/PShell/pshellcontrol/home/data/2018_09_1"
            self.end_list = []
            for (dirpath, dirnames, filenames) in walk(self.end_path):
                self.end_list.extend(filenames)
            self.new_list = list(set(self.end_list)-set(self.start_list))
            if len(self.new_list)>0:
                self.new_list = self._remove_mca(self.new_list)
                self.new_list.sort()
                try:
                    self._createmasterlog(info)
                    pass
                except:
                    print("[Error]: Failed to create master file")

    def _makepath(self, dpath):
        tnow = time.localtime()
        fullpath = dpath + '{:d}'.format(int(tnow.tm_year))+ "_"+'{:02d}'.format(int(tnow.tm_mon))
        return fullpath

    def _remove_mca(self, flist):
        retlist = []
        for ff in flist:
            if "mca" not in ff: retlist.append(ff)
        return retlist

    def _createmasterlog(self, info):
        foldername = (
            '{:d}'.format(int(self.start_time.tm_year))+
            '{:02d}'.format(int(self.start_time.tm_mon))+
            '{:02d}'.format(int(self.start_time.tm_mday))
            )

        fname = (
            foldername+"_"+
            '{:02d}'.format(int(self.start_time.tm_hour))+
            '{:02d}'.format(int(self.start_time.tm_min))+
            '{:02d}'.format(int(self.start_time.tm_sec))+
            '_master.txt'
            )
        folderpath = self.start_path+'/'+foldername+"/master"
        if os.path.isdir(folderpath) == False:
            os.mkdir(folderpath)
        fullpath = folderpath+"/"+fname
        self.fullpath = fullpath
        datestr = (
            '{:02d}'.format(int(self.start_time.tm_mday))+"."+
            '{:02d}'.format(int(self.start_time.tm_mon))+"."+
            '{:04d}'.format(int(self.start_time.tm_year))+" - "+
            '{:02d}'.format(int(self.start_time.tm_hour))+":"+
            '{:02d}'.format(int(self.start_time.tm_min))+":"+
            '{:02d}'.format(int(self.start_time.tm_sec))
            )

        f = open(self.script, 'r')
        scripttext = f.read()
        f.close()

        logtext = []
        logtext.append("###  date  ###\n")
        logtext.append(datestr+'\n\n')
        logtext.append("###  script name  ###\n")
        logtext.append(self.script+'\n\n')
        logtext.append("###  data files  ###\n")
        for lines in self.new_list:
            logtext.append(lines+'\n')
        logtext.append("\n###  Status  ###\n")
        logtext.append("Error: " + str(info.isError())+'\n')
        logtext.append(str(info.getResult())+'\n\n')
        logtext.append("###  script code  ###\n")
        logtext.append(scripttext)

        f = open(fullpath, "w")
        for lines in logtext:
            f.write(lines)
        f.close()
