#!/usr/bin/bash

USER=$(id -nu 1000)
DEST_DIR="/home/${USER}/.config/automount"
DEST="/etc/systemd/system"

echo "USER    : ${USER}"
echo "DEST_DIR: ${DEST_DIR}"
echo 

function CLONE () {
    if sudo apt-get install udisks2; then
        echo 
        echo "udisks2 installed"
        echo 
        sleep 2 
    fi

    if [[ ! -d "${DEST_DIR}" ]]; then
        echo "DEST_DIR:" "${DEST_DIR}"
        sudo -u ${USER} git clone "https://github.com/luizoti/automount.git" "${DEST_DIR}"
    fi
}

function COPYSERVICES () {
    SERVICES=(
            "0:automont_disconect@.service"
            "1:automont_mount@.service"
            "2:automont_umount@.service"
            )
    
    for SERV in "${SERVICES[@]}"; do
        DESTINY_SERV=${DEST_DIR}/${SERV##*:}
        DEST_SERV=${DEST}/${SERV##*:}

        if cp -rf "${DESTINY_SERV}" "${DEST_SERV}"; then
            echo "Serviço copiado com ${DEST_SERV}"
        fi
    done
    sudo systemctl daemon-reload
}

function UDEV () {
    echo " ____________________________________________________________________________ "
    echo "|____________________________________________________________________________|"
    echo "|___________________________________ UDEV ___________________________________|"
    echo "|____________________________________________________________________________|"
    echo "|____________________________________________________________________________|"

    LIB_ZZ="/lib/udev/rules.d/automount-custon.rules"

    echo -e '#!/bin/bash
# 
ACTION=="add", \
    SUBSYSTEM=="block", \
        KERNEL=="[sh]d[a-z]|mmcblk[0-9]", \
            RUN+="/usr/bin/sudo /bin/systemctl start --no-block automont_mount@.service"

ACTION=="change", \
    SUBSYSTEM=="block", \
        KERNEL=="[sh]d[a-z]|mmcblk[0-9]", \
            RUN+="/usr/bin/sudo /bin/systemctl start --no-block automont_umount@.service"

ACTION=="remove", \
    SUBSYSTEM=="block", \
        KERNEL=="[sh]d[a-z]|mmcblk[0-9]", \
            RUN+="/usr/bin/sudo /bin/systemctl start --no-block automont_disconect@.service"' > ${LIB_ZZ}
    # 
    echo
    echo ${LIB_ZZ}
    echo
    # 
    sudo udevadm control --reload-rules
}

CLONE
COPYSERVICES
UDEV

exit