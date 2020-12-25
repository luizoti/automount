#!/usr/bin/python3

# /usr/share/polkit-1/actions/org.freedesktop.UDisks2.policy
# /usr/share/polkit-1/actions/org.freedesktop.NetworkManager.policy
# /usr/share/polkit-1/actions/org.freedesktop.login1.policy

desc = ""
user = "luiz"
action = ""
_bool = ""

_DIR = "/etc/polkit-1/localauthority/50-local.d/"

POLKIT_DICT = {
    0: ["Control udisks2 mount", "org.freedesktop.udisks2.filesystem-mount", "yes", '*'],
    1: ["Control udisks2 umount", "org.freedesktop.udisks2.filesystem-unmount-others", "yes", '*'],
    2: ["Control udisks2 power-off", "org.freedesktop.udisks2.power-off-drive", "yes", '*'],
    3: ["Control udisks2 system drive power-off", "org.freedesktop.udisks2.power-off-drive-system", "no", '*'],
    4: ["Control udisks2 power-off seat", "org.freedesktop.udisks2.power-off-drive-other-seat", "yes", '*'],
    5: ["Control udisks2 eject", "org.freedesktop.udisks2.eject-media", "yes", '*'],
    6: ["Control udisks2 eject seat", "org.freedesktop.udisks2.eject-media-other-seat", "yes", '*'],
    7: ["Control udisks2", "org.freedesktop.udisks2.filesystem-mount-system", "yes", '*'],
    8: ["Control udisks2", "org.freedesktop.udisks2.filesystem-mount-other-seat", "yes", '*'],
    9: ["Control udisks2", "org.freedesktop.udisks2.filesystem-mount-fstab", "yes", '*'],
}

def returnrulepath(_action):
    toremove = "org.freedesktop."

    try:
        if toremove in _action:
            return ''.join([_DIR, _action.replace(toremove, '').replace('.*', ''), ".pkla"])
    except Exception as e:
        raise e


for item in POLKIT_DICT:
    _PL = POLKIT_DICT[item]
    desc = _PL[0]
    action = _PL[1]
    _bool = _PL[2]

    if len(_PL) == 4 and _PL[3] == "*":
        user = _PL[3]
        pass

    try:
        _PATH = returnrulepath(action)

        TEMPLATE = [f"[{desc}]\n", f"Identity=unix-group:{user}\n", f"Action={action}\n", f"ResultAny={_bool}\n"]
        new_pklt = open(_PATH, "w")
        print("Regra instalada:", _PATH)
        new_pklt.write(''.join(TEMPLATE))
        new_pklt.close()
    except Exception as e:
        raise e
    pass