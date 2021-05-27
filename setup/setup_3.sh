#!/bin/bash
tar -xvf ~/5G_measurement_tool/source/other/iperf3_modified.tar.gz -C ~/ 
tar -xvf ~/5G_measurement_tool/source/other/exll_module.tar.gz -C ~/ 
tar -xvf ~/5G_measurement_tool/source/other/tcpprobe.tar.gz -C ~/ 

# install iperf3
cd ~/iperf3
./configure; sudo make; sudo make install
sudo cp ~/iperf3/src/iperf3 /usr/local/lib
sudo ldconfig

# install pcc_module
cp -R ~/5G_measurement_tool/source/other/pcc-vivace/  ~/
cd ~/pcc-vivace/
make
sudo insmod tcp_pcc.ko 

# install exll_module
cd ~/exll_module
make
sudo insmod tcp_exll.ko 

# install tcpprobe
cd ~/module
sudo make
sudo insmod tcp_probe.ko port=9001 full=1 buffer=1

# if you want to check tcp_probe is working or not, then run iperf3 server and client and run following command.
# sudo cat /proc/net/tcpprobe > data 2>&1

# sudo modprobe -r tcp_probe  # to delete if the module is already installed or want to change setting or port

# check the list of congestion control
sysctl net.ipv4.tcp_available_congestion_control

sudo sysctl -w net.ipv4.tcp_wmem="16000000 16000000 256000000"
sudo sysctl -w net.ipv4.tcp_rmem="16000000 16000000 256000000"
sudo sysctl -w net.core.wmem_max="256000000"
sudo sysctl -w net.core.rmem_max="256000000"

sudo sysctl -w net.ipv4.tcp_no_metrics_save=1 # disable tcp cache
sudo chmod 777 -R /mydata/
mkdir /mydata/www/
mkdir /mydata/www/html/
mkdir /mydata/www/html/tmp/

echo "Install Apache"
sudo apt install apache2
sudo cp ~/5G_measurement_tool/source/other/apache/apa/sites-available/* /etc/apache2/sites-available/
sudo cp ~/5G_measurement_tool/source/other/apache/apa/sites-available/* /etc/apache2/sites-available/
service apache2 reload
sudo systemctl status apache2.service

echo "Last step!!!! You must do this following command"
echo "sudo -i"
echo "echo 0 > /sys/module/tcp_cubic/parameters/hystart"  # disable tcp hystart