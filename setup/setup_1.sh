#!/bin/bash
sudo apt update
sudo apt-get install wget fakeroot build-essential ncurses-dev xz-utils libssl-dev bc -y
git clone https://github.com/Soheil-ab/c2tcp.git
# Download linux-4.14.161 -? 4.13.1 for c2tcp
# wget https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/snapshot/linux-4.14.161.tar.gz
wget https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/snapshot/linux-4.13.1.tar.gz # c2tcp
# wget http://www.kernel.org/pub/linux/kernel/v4.0/linux-4.13.1.tar.gz # c2tcp
# copy tar file into your folder : change the name of directory if you need (/mydata/)
# sudo mkdir /mydata/
sudo cp linux-4.13.1.tar.gz /mydata/
cd /mydata/
# unzip the file
sudo tar -xvf linux-4.13.1.tar.gz -C /mydata/
cd /mydata/linux-4.13.1

sudo patch -p1 < ~/c2tcp/linux-patch/linux-4-13-1-orca-c2tcp-0521.patch
# copy modified files:
sudo cp ~/5G_measurement_tool/source/other/kernel_4.13.1/inet_diag.h /mydata/linux-4.13.1/include/uapi/linux/inet_diag.h
sudo cp ~/5G_measurement_tool/source/other/kernel_4.13.1/tcp_bbr.c /mydata/linux-4.13.1/net/ipv4/tcp_bbr.c
sudo cp /boot/config-$(uname -r) .config   
# setup manually!
echo "Now, you should set up with menuconfig."
echo "-> Networking support -> Networking options -> TCP: advanced congestion control"
echo "-> cubic, reno, bbr, (westwood) includes with [Y] command -> Save and exit"
cd /mydata/linux-4.13.1
sudo make menuconfig
echo "sudo make -j 4 && sudo make modules_install -j 4 && sudo make install -j 4"
echo "sudo update-initramfs -c -k 4.13.1"
echo "sudo update-grub"
echo "sudo reboot"
# sudo make menuconfig
# sudo make -j 4 && sudo make modules_install -j 4 && sudo make install -j 4

# set a new kernel into a defalut
# sudo update-initramfs -c -k 4.13.1
# sudo update-grub  

# reboot the server
# sudo reboot

# check kernel version
uname -r
# you will see : 4.13.1

# # if your kernel version is not below 4.13.1, then use this command
# # 
# 1. Open and edit GRUB setup file:

# sudo nano /etc/default/grub

# # 2. Find line GRUB_DEFAULT=...(by default GRUB_DEFAULT=0) and sets in quotes menu path to concrete Kernel(Remember menu indexes from steps 2 and 3). In my system first index was 1 and second was 2. I set in to GRUB_DEFAULT

# GRUB_DEFAULT="1>2" # Save file.

# # 3. Update GRUB information for apply changes:

# sudo update-grub

# # 4. After reboot you automatically boot on Kernel by chosen menu path. An example on my machine 1 -> 2

# # 5. Check Kernel version after reboot:

# uname -r
# #