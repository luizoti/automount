#!/usr/bin/python3

import dbus
from random import randrange
from dbus.mainloop.glib import DBusGMainLoop

_id = randrange(999)
actions = ''
hints = ''

class NotifyAction(object):
    def __init__(self):
        maintloop = DBusGMainLoop()
        dbus_session = dbus.SessionBus(maintloop)
        self.obj = dbus_session.get_object('org.freedesktop.Notifications',
                                                    '/org/freedesktop/Notifications')


    def create(self, appname, _id, icon, summary, messege, actions, hints, timeout):
        print(appname, _id, icon, summary, messege, actions, hints, timeout)
        dbus.Interface(self.obj,
            'org.freedesktop.Notifications').Notify(appname,
                                                    _id,
                                                    icon,
                                                    summary,
                                                    messege,
                                                    actions,
                                                    hints,
                                                    timeout)
