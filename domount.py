#!/usr/bin/env python3

import re
import os
import dbus
import os.path
#
METHOD = {
    "fs": "org.freedesktop.UDisks2.Filesystem",
    "pt": "org.freedesktop.UDisks2.PartitionTable",
}

class UDisksBus():
    def init(self, DEV, method):
        bus = dbus.SystemBus()
        OBJ = bus.get_object('org.freedesktop.UDisks2',
            ''.join(['/org/freedesktop/UDisks2/block_devices/', DEV]))

        try:
            return dbus.Interface(OBJ, dbus_interface=method)
        except Exception as e:
            raise e


    def devExists(self, devpath):
        try:
            os.stat(devpath)
        except OSError:
            return False
        return True


    def partitionTableChecker(self, DEV):
        status = False
        devs = []

        for device in DEV:
            if device[-1].isdigit():
                devs.append(device)
            else:
                for x in range(1,11):
                    devpath = ''.join(["/dev/", device, str(x)])

                    if self.devExists(devpath) == True:
                        devs.append(''.join([device, str(x)]))
                        status = True

                    if x == 10 and status == False:
                        devs.append(device)
                        status = False
                        x = 0
        return devs


    def mount(self, DEV):
        for device in self.partitionTableChecker(DEV):
            init = self.init(device, METHOD['fs'])
            domount = init.get_dbus_method('Mount')

            try:
                target = domount({'s': 'a'})

                if os.path.ismount(target):
                    yield 'mounted', device, target
            except Exception as e:
                expt = str(e)

                if "AlreadyMounted" in expt:
                    yield 'already', device, re.findall(r"\`(.+?)\'", str(expt))[0]
                    pass


    def umount(self, DEV):
        if type(DEV) == str:
            _devs = [DEV]
        else:
            _devs = DEV
            pass

        for device in self.partitionTableChecker(_devs):
            init = self.init(device, METHOD['fs'])
            doumount = init.get_dbus_method('Unmount')

            try:
                doumount({'s': 'a'})
            except Exception as e:
                expt = str(e)
                if "AlreadyMounted" in expt:
                    yield 'already', device, re.findall(r"\`(.+?)\'", mntOut)[0]
                    pass
                


    def repair(self, DEV):
        for device in self.partitionTableChecker(DEV):
            self._umount() # You need to unmount before repairing the disc.

            init = self.init(device, METHOD['fs'])
            repair = init.get_dbus_method('Repair')

            try:
                repair({'s': 'a'})
            except Exception as e:
                print(e)


    # def resize(self, DEV):
    #     return self.init(DEV, METHOD['fs']).get_dbus_method('Resize')({'s': 'a'})

    # def setlabel(self, DEV):
    #     return self.init(DEV, METHOD['fs']).get_dbus_method('SetLabel')('NEEWW')

    # def ownership(self, DEV):
    #     try:
    #         return self.init(DEV, METHOD['fs']).get_dbus_method('TakeOwnership')({'s': 'a'})
    #     except Exception as e:
    #         print(e)
