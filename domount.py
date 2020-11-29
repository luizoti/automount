#!/usr/bin/env python3

import re
import os
import dbus
from os.path import join, realpath, basename
#
INTERFACES = {
    "fs": "org.freedesktop.UDisks2.Filesystem",
    "dr": "org.freedesktop.UDisks2.Drive",
    "pp": "org.freedesktop.DBus.Properties",
    "pt": "org.freedesktop.UDisks2.PartitionTable",
}

PATHS = {
    "drives": "/org/freedesktop/UDisks2/drives/",
    "block_devices": "/org/freedesktop/UDisks2/block_devices/",
}

class UDisksBus():
    def __init__(self):
        self.bus = dbus.SystemBus()

    def SetDevice(self, path, dev_device):
        return self.bus.get_object('org.freedesktop.UDisks2', ''.join([path, dev_device]))

    def SetInterface(self, device, dbus_iface):
        return dbus.Interface(device, dbus_interface=dbus_iface)

    def getProperties(self, dev_device, path, interface, propkey=None):
        if path == "drives":
            dev_name = self.getDeviceName(dev_device)
        elif path == "block_devices":
            dev_name = dev_device
            pass

        device = self.SetDevice(PATHS[path], dev_name)
        iface = self.SetInterface(device, INTERFACES['pp'])
        props = iface.GetAll(INTERFACES[interface])

        if propkey != None:
            return props[propkey]
            pass

        return props

    def devExists(self, devpath):
        try:
            os.stat(devpath)
        except OSError:
            return False
        return True

    def getDeviceName(self, device):
        DISKS_PATH = "/dev/disk/by-id/"

        for devicename in os.listdir(DISKS_PATH):
            devicepath = join(DISKS_PATH, devicename)
            if device in realpath(devicepath):
                return re.sub(r'(usb|ata|wwn)\-', '', re.sub(r'\-([a-z].*|[0,99]\:.+?)', '', devicename))

    def partitionTableChecker(self, deviceslist):
        for device in deviceslist:
            try:
                prop = self.getProperties(device, "block_devices", "pt", "Partitions")
            except dbus.exceptions.DBusException as e:
                if 'No such interface “org.freedesktop.UDisks2.PartitionTable”' in str(e):
                    yield basename(device)
                    pass

            for ptb in prop:
                yield basename(ptb)

    def checkCanPowerOff(self, dev_device):
        prop = self.getProperties(dev_device, "drives", "dr", "CanPowerOff")

        if prop == 0:
            return False
        elif prop == 1:
            return True
            pass
    # 
    def mount(self, dev_device):
        if type(dev_device) == str:
            _devs = [dev_device]
        else:
            _devs = dev_device
            pass

        for dev in self.partitionTableChecker(_devs):
            device = self.SetDevice(PATHS['block_devices'], dev)
            iface = self.SetInterface(device, INTERFACES['fs'])
            domount = iface.get_dbus_method('Mount')

            try:
                target = domount({'s': 'a'})

                if os.path.ismount(target):
                    yield 'mounted', dev, target
            except Exception as e:
                expt = str(e)

                if "AlreadyMounted" in expt:
                    yield 'already', dev, re.findall(r"\`(.+?)\'", str(expt))[0]

    def umount(self, dev_device):
        if type(dev_device) == str:
            _devs = [dev_device]
        else:
            _devs = dev_device
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

    def repair(self, dev_device):
        for device in self.partitionTableChecker(dev_device):
            self._umount() # You need to unmount before repairing the disc.

            init = self.init(device, 'fs')
            repair = init.get_dbus_method('Repair')

            try:
                repair({'s': 'a'})
            except Exception as e:
                print(e)

    def resize(self, dev_device):
        return self.init(dev_device, 'fs').get_dbus_method('Resize')({'s': 'a'})

    def setlabel(self, dev_device):
        return self.init(dev_device, 'fs').get_dbus_method('SetLabel')('NEEWW')

    def ownership(self, dev_device):
        try:
            return self.init(dev_device, 'fs').get_dbus_method('TakeOwnership')({'s': 'a'})
        except Exception as e:
            print(e)

# for x in UDisksBus().partitionTableChecker("sdb"):
#     print(x)
#     pass