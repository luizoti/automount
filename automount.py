#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import subprocess
import argparse
#
from domount import UDisksBus
from dbus_notify import *

parse = argparse.ArgumentParser(description='AutoMount devices with udev')
parse.add_argument('-m', nargs='+', metavar='sda sdb2 sdc', help='Mount devices')
parse.add_argument('-s', help='Show devices', action='store_true')
args = parse.parse_args()


class AutoMount():
    def __init__(self, devices):
        self.mnt = UDisksBus()
        self.nt = NotifyAction()

        for dev in devices:
            self.mount(dev)
            pass


    def mount(self, dev):
        try:
            for messege in self.mnt.mount([dev]):
                self.notify(list(messege))
        except Exception as e:
            raise e


    def notify(self, messege):          
        appname = "AutoMount"
        _id     = randrange(999)
        icon    = "drive-removable-media-usb-pendrive"
        summary = ''.join(['/dev/', messege[1]])

        if "already" in messege:
            messege = ' '.join([messege[1], "já montado em", messege[2]])
        elif "mounted" in messege:
            messege = ' '.join([messege[1], "foi montado em", messege[2]])
            pass
        actions = ''
        hints   = ''
        timeout = 10000

        try:
            self.nt.create(appname, _id, icon, summary, messege, actions, hints, timeout)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    mount = args.m
    show = args.s

    if not mount == None:
        try:
            AutoMount(mount)
        except Exception as e:
            raise e

    if show is True:
        print("devss")
        pass
