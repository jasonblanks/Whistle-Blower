#from _winreg import *
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
        # Windows...
        return _platform
    elif _platform == "win64":
        return _platform


def RegScan():
    #reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    RegKey = open("RegKeys.txt").readlines()

    #RegKey = [r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\SynTPEnh",r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\SynTPEnh']

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


def main():
    OS = OSCheck()
    if OS == r"win32" or OS == r"win64":
        print OS
        RegScan()
    else:
        print "System is a "+OS+" Machine, nothing to be done here."


main()
