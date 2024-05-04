#!/bin/bash
## Not yet optimized
# yay and packages (ypacs) from the aur dont work and I just can't be bothered to fix that right now.
#


set -exu
set -o noclobber

{
rm /home/jan/Schreibtisch/setup_sh_log.txt
} || {
echo "bump"
}

echo "log has been created"
echo > /home/jan/Schreibtisch/setup_sh_log.txt
fail=1

# Shell Setup Script for my manjaro system

# Package List
pacs=(spotify-launcher qrencode telegram-desktop element-desktop deepin-boot-maker torbrowser-launcher signal-desktop thunderbird korganizer p7zip vlc firefox kdeconnect vim kicad blender steam gimp inkscape discord pdfarranger handbrake sl hollywood brasero)

# Package List from AUR
ypacs=(visual-studio-code-bin)


# Eduroam (zuerst weil da input)

{
curl "https://cat.eduroam.org/user/API.php?action=downloadInstaller&lang=en&profile=12188&device=linux&generatedfor=user&openroaming=0" -o/home/jan/Donwloads/eduroam-linux-FEF-FAU_2024.py
chmod a+x /home/jan/Donwloads/eduroam-linux-FEF-FAU_2024.py
./home/jan/Donwloads/eduroam-linux-FEF-FAU_2024.py
echo
} || {
echo "failure to install EDUROAM" >> /home/jan/Schreibtisch/setup_sh_log.txt
}



# Update base programs

sudo pacman -Syu

# FAUBOX

{
curl https://faubox.rrze.uni-erlangen.de/client_deployment/FAUbox_Linux.tar.gz -o/home/jan/Downloads/FAUbox_Linux.tar.gz
7z x /home/jan/Downloads/FAUbox_Linux.tar.gz -o/home/jan/Downloads
7z x /home/jan/Downloads/FAUbox_Linux.tar -o/home/jan/Downloads
chmod a+x /home/jan/Downloads_/FAUbox/FAUbox-Install.sh
#sudo ./home/jan/Downloads/FAUbox/FAUbox-Install.sh install

} || {
echo "failure to install FAUBOX" >> /home/jan/Schreibtisch/setup_sh_log.txt
}

# FAU VPN Fulltunnel
{
curl https://www.anleitungen.rrze.fau.de/files/2023/01/FAU_Fulltunnel.ovpn -o/etc/openvpn/client/FAU_Fulltunnel.ovpn
chmod 644 /etc/openvpn/client/FAU_Fulltunnel.ovpn
#nmcli connection import type openvpn file /etc/openvpn/client/FAU_Fulltunnel.ovpn

} || {
echo "failure to install FAU-VPN" >> /home/jan/Schreibtisch/setup_sh_log.txt
}


# So langsam mal die ganzen Programme, die ich haben möchte

{
sudo pacman -S --needed git base-devel --noconfirm
git clone https://aur.archlinux.org/yay-bin.git
sudo mv yay-bin /home/$USER/Downloads/yay-bin
cd /home/$USER/Downloads/yay-bin && makepkg -si

yay -Y --gendb
yay -Syu --devel
yay -Y --devel --save

aur = 0

} || {
echo "failure to install yay" >> /home/jan/Schreibtisch/setup_sh_log.txt
}

for item in "${pacs[@]}"; do
{
sudo pacman -S $item --noconfirm && echo "successfully installed: $item" >> /home/jan/Schreibtisch/setup_sh_log.txt
echo bump
} || {
echo "failure to install $item" >> /home/jan/Schreibtisch/setup_sh_log.txt
}
done



for item in "${ypacs}"; do
{
sudo pacman -S $item --noconfirm && echo "successfully installed: $item"
} || {
echo "failure to install aur $item" >> /home/jan/Schreibtisch/setup_sh_log.txt
}
done
