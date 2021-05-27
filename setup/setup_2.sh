#!/bin/bash
sudo apt update
sudo apt install openssl git vim build-essential openssh-server gnuplot -y
sudo apt install libtinfo5 libtinfo-dev libncurses5 libncurses5-dev -y
sudo apt install software-properties-common -y
sudo apt install zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev wget libbz2-dev -y
sudo apt install autoconf automake libtool curl make g++ unzip -y
sudo apt install libboost-system-dev libboost-filesystem-dev libboost-chrono-dev libboost-program-options-dev libboost-test-dev libboost-thread-dev -y
sudo apt install libasio-dev libalglib-dev libboost-system-dev -y
sudo apt install protobuf-c-compiler protobuf-compiler -y
sudo apt install libprotobuf-dev -y
sudo apt install qt5-default checkinstall libc6-dev libexpat1-dev libqt4-dev libavcodec-dev libavutil-dev pkg-config -y
sudo apt install libgl1-mesa-dev libboost-all-dev makepp libboost-dev libjemalloc-dev libboost-python-dev -y
sudo apt install debhelper autotools-dev dh-autoreconf iptables ssl-cert libxcb-present-dev libcairo2-dev libpango1.0-dev apache2-dev apache2-bin dnsmasq-base iproute2 apache2-api-20120211 libwww-perl -y

sudo apt-add-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.7 python3-pip python3-dev python3-virtualenv python-apt -y

sudo rm /usr/bin/python3
sudo ln -s /usr/bin/python3.7 /usr/bin/python3
sudo rm /usr/bin/python3m
sudo ln -s /usr/bin/python3.7m /usr/bin/python3m

sudo apt-get install --reinstall python3-apt
cd  /usr/lib/python3/dist-packages
ls -la /usr/lib/python3/dist-packages
sudo cp apt_pkg.cpython-35m-x86_64-linux-gnu.so apt_pkg.so
cd ~/

sudo apt-add-repository ppa:ubuntu-toolchain-r/test -y
sudo apt update
sudo apt install g++-6 -y

pip3 install --upgrade pip
pip3 install typing yattag numpy sh pexpect matplotlib

# COPA
git clone https://bitbucket.org/sandesh_dhawaskar/modified_copa.git
# # git clone https://github.com/venkatarun95/genericCC.git
# VERUS
git clone https://github.com/yzaki/verus.git 
# SPROUT
git clone https://github.com/keithw/sprout.git
# c2tcp
git clone https://github.com/Soheil-ab/c2tcp.git

# # install COPA
mv ~/modified_copa/genericCC ~/genericCC
cd ~/genericCC
cp ~/5G_measurement_tool/source/other/copa/sender.cc ~/genericCC
cp ~/5G_measurement_tool/source/other/copa/client.cc ~/genericCC
cp ~/5G_measurement_tool/source/other/copa/markoviancc.cc ~/genericCC
cp ~/5G_measurement_tool/source/other/copa/udp-socket.cc ~/genericCC  # put your server IP address @line.22
makepp

# install verus
sudo apt-get install -y libtbb-dev
cd ~/verus
./bootstrap.sh && ./configure && make

# # install sprout
cd ~/sprout
cp ~/5G_measurement_tool/source/other/sprout/sproutconn.cc ~/sprout/src/network/
./autogen.sh && ./configure --enable-examples && make

# c2tcp
cp ~/5G_measurement_tool/source/other/c2tcp/client.c ~/c2tcp/src
cp ~/5G_measurement_tool/source/other/c2tcp/define.h ~/c2tcp/src
cp ~/5G_measurement_tool/source/other/c2tcp/server-standalone.cc ~/c2tcp/src
cd ~/c2tcp
./build.sh