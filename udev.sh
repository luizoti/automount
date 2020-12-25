#!/bin/bash

# https://superuser.com/questions/677106/how-to-check-if-a-udev-rule-fired
# http://billauer.co.il/blog/2011/06/udev-dok-disk-on-key-usb-stick/
# https://www.axllent.org/udev-dok-disk-on-key-usb-stickcs/view/auto-mounting-usb-storage/
# 
# udevadm info -q all -a /dev/sdb
# sudo udevadm control --reload-rules && sudo systemctl daemon-reload
# sudo udevadm info --query=all --name=/dev/sdd1
# /usr/bin/sudo -u luiz /usr/bin/udisksctl mount -b /dev/sdg1
# 

echo " ____________________________________________________________________________ "
echo "|____________________________________________________________________________|"
echo "|___________________________________ UDEV ___________________________________|"
echo "|____________________________________________________________________________|"
echo "|____________________________________________________________________________|"

LIB=/lib/udev/rules.d

LIB_CUSTON="${LIB}/10-udev-custon.rules"

echo -e '#!/bin/bash

ACTION=="change", \
    KERNEL=="card0", \
        SUBSYSTEM=="drm" \
            RUN+="/bin/systemctl start --no-block display_detect.service"
 
' > ${LIB_CUSTON}

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


LIB_ZZ="${LIB}/zz-custon.rules"

echo -e '#!/bin/bash
# 
ACTION=="add", \
    SUBSYSTEM=="block", \
        KERNEL=="[sh]d[a-z]|mmcblk[0-9]", \
            RUN+="/usr/bin/logger adicionado %k", \
                RUN+="/usr/bin/sudo /bin/systemctl start --no-block automont_mount@.service"

ACTION=="change", \
    SUBSYSTEM=="block", \
        KERNEL=="[sh]d[a-z]|mmcblk[0-9]", \
            RUN+="/usr/bin/sudo /bin/systemctl start --no-block automont_umount@.service"

ACTION=="remove", \
    SUBSYSTEM=="block", \
        KERNEL=="[sh]d[a-z]|mmcblk[0-9]", \
            RUN+="/usr/bin/sudo /bin/systemctl start --no-block automont_disconect@.service"

ACTION=="add", \
    SUBSYSTEM=="input", \
        ATTR{uniq}=="00:06:f5:97:ab:94" \
            # ATTR{name}=="Sony Computer Entertainment Inc BD Remote Control" \
                RUN+="/bin/systemctl start --no-block ps3bdremote.service"

ACTION=="change", \
    KERNEL=="card0", \
        SUBSYSTEM=="drm" \
            RUN+="/usr/bin/logger video change %k"

' > ${LIB_ZZ}
echo
echo ${LIB_CUSTON}
echo ${LIB_ZZ}
echo

sudo udevadm control --reload-rules && sudo systemctl daemon-reload