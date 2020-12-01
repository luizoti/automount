#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import subprocess
import argparse
from os.path import dirname, join
#
from udisksbus import UDisksBus
from dbus_notify import *

parse = argparse.ArgumentParser(description='AutoMount devices with udev')
parse.add_argument('-m', nargs='+', metavar='sda sdb2 sdc', help='Mount devices')
parse.add_argument('-u', nargs='+', metavar='sda sdb2 sdc', help='Umount devices')
parse.add_argument('-nu', action='store_true', help='Umount - notify only use with udev')
parse.add_argument('-nd', action='store_true', help='Disconect - notify only use with udev')
parse.add_argument('-s', help='Show devices', action='store_true')
args = parse.parse_args()


class AutoMount():
    def __init__(self):
        self.mnt = UDisksBus()
        self.nt = NotifyAction()


    def mount(self, devices):
        _mnt = self.mnt.mount(devices)

        try:
            for messege in _mnt:
                self.notify(list(messege))
        except Exception as e:
            raise e


    def umount(self, devices):
        _mnt = self.mnt.mount(devices)

        try:
            for messege in _mnt:
                self.notify(list(messege))
        except Exception as e:
            raise e


    def notify(self, messege):          
        appname = "AutoMount"
        _id     = randrange(999)
        icon    = join(dirname(__file__), "drive-removable-media-usb-pendrive.svg")
        summary = ''.join(['/dev/', messege[1]])

        if "already" in messege:
            messege = ' '.join([messege[1], "já montado em", messege[2]])
        elif "mounted" in messege:
            messege = ' '.join([messege[1], "foi montado em", messege[2]])
            pass

        actions = ''
        hints   = ''
        timeout = 4000

        try:
            self.nt.create(appname, _id, icon, summary, messege, actions, hints, timeout)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    am = AutoMount()

    mount = args.m
    umount = args.u
    show = args.s
    notify_umount = args.nu
    notify_disconect = args.nd

    if not mount == None:
        try:
            am.mount(mount)
        except Exception as e:
            raise e
    elif not umount == None:
        try:
            am.umount(mount)
        except Exception as e:
            raise e


    if notify_umount == True:
        print("notify_umount")
    elif notify_disconect == True:
        print("notify_disconect")
        pass

    if show is True:
        print("devss")
        pass
