#!/usr/bin/bash

USER=$(id -nu 1000)
DEST_DIR="/home/${USER}/.config/automount"
DEST="/etc/systemd/system/"

echo "USER:" "${USER}"

function CLONE () {
    if sudo apt-get install udisks2; then
        echo 
        echo "udisks2 installed"
        echo 
        sleep 2 
    fi

    if [[ ! -d "${DEST_DIR}" ]]; then
        echo "DEST_DIR:" "${DEST_DIR}"
        sudo -u ${USER} git clone "git@github.com/luizoti/automount.git" "${DEST_DIR}"
    fi
}

function COPYSERVICES () {
    SERVICES=(
            "0:automont_disconect@.service"
            "1:automont_mount@.service"
            "2:automont_umount@.service"
            )
            
    for SERV in "${SERVICES[@]}"; do
        SERV=${DEST_DIR}/${SERV##*:}
        DEST_SERV=${DEST}/${SERV##*:}

        if [[ ! -f "${DEST_SERV}" ]]; then
            if cp -rf "${SERV}" "${DEST_SERV}"; then
                echo "Serviço copiado com ${DEST_SERV}"
                sudo systemctl stop "${SERV}"
            fi
        fi
    done

}

COPYSERVICES
exit