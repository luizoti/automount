#!/usr/bin/env python3

import re
import os
import dbus
from os.path import join, realpath
#
METHOD = {
    "fs": "org.freedesktop.UDisks2.Filesystem",
    "pt": "org.freedesktop.UDisks2.PartitionTable",
    "canpoweroff": "org.freedesktop.UDisks2.Drive.CanPowerOff",
    "poweroff": "org.freedesktop.UDisks2.Drive.PowerOff",
    "ejectable": "org.freedesktop.UDisks2.Drive.Ejectable",
    "eject": "org.freedesktop.UDisks2.Drive.Eject",
}

PATHS = {
    "drives": "/org/freedesktop/UDisks2/drives",
    "block_devices": "/org/freedesktop/UDisks2/block_devices/",
}

class UDisksBus():
    def init(self, DEV, method):
        if method in ['fs', 'pt']:
            path = PATHS['block_devices']
        elif method in ['canpoweroff', 'poweroff', 'ejectable', 'eject']:
            path = PATHS['drives']
            pass

        bus = dbus.SystemBus()
        OBJ = bus.get_object('org.freedesktop.UDisks2', ''.join([path, DEV]))

        try:
            return dbus.Interface(OBJ, dbus_interface=METHOD[method])
        except Exception as e:
            raise e


    def devExists(self, devpath):
        try:
            os.stat(devpath)
        except OSError:
            return False
        return True

    def getDevicePath(self, device):
        DISKS_PATH = "/dev/disk/by-id/"

        for devicename in os.listdir(DISKS_PATH):
            devicepath = join(DISKS_PATH, devicename)
            if device in realpath(devicepath):
                print(device)
                print(re.sub(r'(usb|ata|wwn)\-', '', re.sub(r'\-([a-z].*|[0,99]\:.+?)', '', devicename)))
                pass
            pass


    def partitionTableChecker(self, deviceslist):
        devs = []

        for device in deviceslist:
            status = False
            if device[-1].isdigit():
                devs.append(device)
            else:
                for x in range(1,11):
                    devpath = ''.join(["/dev/", device, str(x)])

                    if self.devExists(devpath) == True:
                        devs.append(os.path.basename(devpath))
                        status = True

                    if x == 10 and status == False:
                        devs.append(device)
                        status = False
                        x = 0
        return devs


    def mount(self, devices):
        for device in self.partitionTableChecker(devices):
            init = self.init(device, 'fs')
            domount = init.get_dbus_method('Mount')

            try:
                target = domount({'s': 'a'})

                if os.path.ismount(target):
                    yield 'mounted', device, target
            except Exception as e:
                expt = str(e)

                if "AlreadyMounted" in expt:
                    yield 'already', device, re.findall(r"\`(.+?)\'", str(expt))[0]


    def umount(self, DEV):
        if type(DEV) == str:
            _devs = [DEV]
        else:
            _devs = DEV
            pass

        for device in self.partitionTableChecker(_devs):
            init = self.init(device, 'fs')
            doumount = init.get_dbus_method('Unmount')

            try:
                doumount({'s': 'a'})
            except Exception as e:
                expt = str(e)
                if "AlreadyMounted" in expt:
                    yield '', device, re.findall(r"\`(.+?)\'", mntOut)[0]
                    pass
                


    def repair(self, DEV):
        for device in self.partitionTableChecker(DEV):
            self._umount() # You need to unmount before repairing the disc.

            init = self.init(device, 'fs')
            repair = init.get_dbus_method('Repair')

            try:
                repair({'s': 'a'})
            except Exception as e:
                print(e)


    # def resize(self, DEV):
    #     return self.init(DEV, 'fs').get_dbus_method('Resize')({'s': 'a'})

    # def setlabel(self, DEV):
    #     return self.init(DEV, 'fs').get_dbus_method('SetLabel')('NEEWW')

    # def ownership(self, DEV):
    #     try:
    #         return self.init(DEV, 'fs').get_dbus_method('TakeOwnership')({'s': 'a'})
    #     except Exception as e:
    #         print(e)

UDisksBus().getDevicePath("sdc")