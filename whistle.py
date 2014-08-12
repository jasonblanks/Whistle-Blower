
import logging
import os
from rekall import session
from rekall import plugins
from rekall.plugins.addrspaces import standard
from rekall import interactive

from sys import platform as _platform

if _platform == "win32":
        from _winreg import *

def OSCheck():
    if _platform == "linux" or _platform == "linux2":
        return _platform
    elif _platform == "darwin":
        # OS X
        return _platform
    elif _platform == "win32":
        return _platform
        # Windows...
    elif _platform == "win64":
        return _platform


def RegScan():
    RegKey = open("RegKeys.txt").readlines()
    for r in RegKey:
            r = r.strip()
            HIVE = r.partition("\\")
            KEY = HIVE[2].rpartition("\\")[0]
            if HIVE[0] == "HKEY_LOCAL_MACHINE":
                reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            #print HIVE
            #print KEY
            try:
                k = OpenKey(reg, KEY, 0, KEY_ALL_ACCESS)
            except:
                print KEY+ " Not found."
                continue

            if k:
                try:
                    count = 0
                    while 1:
                        name, value, type = EnumValue(k, count)
                        KEYVALUE = HIVE[2].rpartition("\\")[2]
                        if KEYVALUE.strip() == name:
                            print "\n"+r+" Exist!"

                        count = count + 1
                except WindowsError:
                    pass

def memscan():
    #logging.getLogger().setLevel(logging.DEBUG)
    livecapture = False
    OS = OSCheck()
    share=r"\\VBOXSVR\Temp"
    if OS == r"win32" or OS == r"win64":
        if livecapture == True:
            root = os.getcwd()
            os.system("winpmem_1.6.0.exe -u")
            os.system("winpmem_1.6.0.exe -l")
            os.system("winpmem_1.6.0.exe "+share+"\\image.raw")
            s = session.Session(
                filename=share+"\\image.raw",
                profile_path=["http://profiles.rekall-forensic.com"])

        else:
            os.system("winpmem_1.6.0.exe -u")
            os.system("winpmem_1.6.0.exe -l")

            s = session.Session(
                filename=r"\\.\pmem",
                profile_path=["http://profiles.rekall-forensic.com"])

        print s.GetParameter("profile")
        print  s.plugins.pslist()
        os.system("winpmem_1.6.0.exe -u")

    else:
        print "Only Windows Memory Analysis is supported at this time"
        #system("winpmem_1.6.0.exe -u")
        #with s:
        #    s.physical_address_space = standard.FDAddressSpace(fhandle=open(
        #            "/home/jason/PycharmProjects/Whistle-Blower/Win7SP1x86.raw"), session=s)
        #    s.GetParameter("profile")
        #
        #    print s.plugins.version_scan()




def main():
    OS = OSCheck()
    if OS == r"win32" or OS == r"win64":
        print OS
        RegScan()
        memscan()
    else:
        print "System is a "+OS+" Machine, nothing to be done here."
        memscan()

main()
