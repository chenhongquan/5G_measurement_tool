#!/bin/bash
sudo apt update
sudo apt install git -y

git clone https://github.com/syslabshare1/5G_measurement_tool.git

cp ~/5G_measurement_tool/setup/setup_1.sh ~/
cp ~/5G_measurement_tool/setup/setup_2.sh ~/
cp ~/5G_measurement_tool/setup/setup_3.sh ~/

cd ~/
chmod 755 setup_*