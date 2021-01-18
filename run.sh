#!/bin/sh
apt update
apt upgrade
apt install -y freerdp2-x11
apt install -y python3-tk
apt install -y python3-pip
pip3 install pillow
sed -i '/XKBOPTIONS/d' /etc/default/keyboard
echo "XKBOPTIONS=\"grp:ctrl_shift_toggle,grp:alt_shift_toggle,grp_led:scroll\"" >> /etc/default/keyboard
adduser user
printf "[SeatDefaults]\nautologin-user=user\nautologin-user-timeout=0\n" >> /etc/lightdm/lightdm.conf.d/autologin.conf
