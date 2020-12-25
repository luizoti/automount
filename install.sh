#!/usr/bin/bash

USER=$(id -nu 1000)
WORKDIR="$(cd $(dirname ${BASH_SOURCE[0]}) && pwd)"
DEST_DIR="/home/${USER}/.config/automount"
DEST="/etc/systemd/system"

echo "USER    : ${USER}"
echo "DEST_DIR: ${DEST_DIR}"
echo "WORKDIR : ${WORKDIR}"
echo 

function _gc () {
    sudo -u ${USER} git clone "https://github.com/luizoti/automount.git" "${DEST_DIR}"
}

function CLONE () {
    if sudo apt-get install udisks2; then
        echo 
        echo "udisks2 installed"
        echo 
        sleep 2 
    fi

    if [[ ! -d "${DEST_DIR}" ]]; then
        echo "DEST_DIR:" "${DEST_DIR}"
        _gc
        echo "${DEST_DIR}, clonado /tmp/"
    else
        sudo rm -rf "${DEST_DIR}"
        echo "${DEST_DIR}, deletado"
        _gc
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
            echo
            CMDOLD=USER
            CMDNEW=${USER}
            sed -i "s/$CMDOLD/$CMDNEW/g" "${DEST_SERV}"
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
            RUN+="/usr/bin/sudo /bin/systemctl start --no-block automont_mount@%k.service"

ACTION=="change", \
    SUBSYSTEM=="block", \
        KERNEL=="[sh]d[a-z]|mmcblk[0-9]", \
            RUN+="/usr/bin/sudo /bin/systemctl start --no-block automont_umount@%k.service"

ACTION=="remove", \
    SUBSYSTEM=="block", \
        KERNEL=="[sh]d[a-z]|mmcblk[0-9]", \
            RUN+="/usr/bin/sudo /bin/systemctl start --no-block automont_disconect@%k.service"' > ${LIB_ZZ}
    # 
    echo
    echo ${LIB_ZZ}
    echo
    # 
    sudo udevadm control --reload-rules
}

function POLKITRULES() {
    echo "instalando polkit-rules"
    if /usr/bin/python3 "${WORKDIR}/polkit_rules.py"; then
        echo
        echo "Sem erros ao instalar regras"
    fi
}

CLONE
COPYSERVICES
UDEV
POLKITRULES

exit