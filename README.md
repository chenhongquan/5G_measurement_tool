# 5G Measurement Automation Script #

Here we will provide you with detailed instructions to test CCAs over 5G and LTE.

---------------
## Install Guide

sudo apt install git
git clone https://github.com/syslabshare1/5G_measurement_tool.git

### Client (For Smartphone)

For cross-complile,

To run the automation scripts in client please add `modified version of iperf3` into your android phone:

1. Download Android Studio, if you alreay have it, no need to install this. 
   
   Go to https://developer.android.com/studio and download Android Studio for Linux
   
   tar -zxvf android-sudio-ide-193.6821437-linux.tar.gz
   
   cd android-studio
   
   cd bin
   
   ./studio.sh
   
   #go to tool > SDK Manager > SDK Tools > Check NDK (Side by Side) & Latest Android SDK COmmand Line Tools

2. Install Requirement 
    ``` 
    sudo apt install gyp -y
    ```
3. Copy iperf3-android and complie
    ```
    tar -xvf iperf3-android.tar.gz -C ~/iperf3-android
    ./configure-android.sh ~/Android/Sdk/ndk/21.3.6528147
    (./configure-android.sh (Path to ndkk))
    ``` 
4. Connect the phone using USB and enable debugging mode : 
(setup link  = https://developer.android.com/studio/debug/dev-options)

    ```
    adb push ./out_arm64/Default/iperf3 /data/local/tmp/
    ```
5. Check iperf3 is successfully installed
    ```
    adb shell
    cd /data/local/tmp
    ./iperf3 -v 
    ```

    OR
    ```
    adb shell /data/local/tmp/iperf3 -v 
    ```
    You could get: 
    ```
    Modified iperf3 for 5G Measuerment iperf 3.6 (cJSON 1.5.2)
    Linux localhost 4.19.81-18952831 #1 SMP PREEMPT Tue Jul 7 12:01:19 KST 2020 aarch64
    Optional features available: CPU affinity setting, IPv6 flow label, TCP congestion algorithm setting, sendfile / zerocopy, socket pacing
    ```
    
    
    ./setup_client.sh

    install files on phone
    
    for iperf3
    cd ~/5G_measurement_tool/source/other/iperf3/
    adb push iperf3 /data/local/tmp/
    
    for copa
    cd ~/5G_measurement_tool/source/other/copa/
    adb push receiver /data/local/tmp/
    
    for verus
    cd ~/5G_measurement_tool/source/other/verus/
    adb push verus_client /data/local/tmp/
    
    for c2tcp
    cd ~/5G_measurement_tool/source/other/c2tcp/
    adb push sender /data/local/tmp/
---------------
### Server

* In the client code please update the private key information and do `scp` before running the scripts. If you don't use the private key, you need to comment the private key part.

1. Download scripts.
   ```
   git clone https://github.com/syslabshare1/5G_measurement_tool.git
   ```

   * put your id_rsa file into 5G_measurement_tool/ssh_key/ directory.

2. In the `5G_measurement_tool/setup/`, setup scripts exist.
    ```
    cp ~/5G_measurement_tool/setup/setup_0.sh ~/
    cp ~/5G_measurement_tool/setup/setup_1.sh ~/
    cp ~/5G_measurement_tool/setup/setup_2.sh ~/
    cp ~/5G_measurement_tool/setup/setup_3.sh ~/

    cd ~/
    chmod 755 setup_*
    ```
3. Install `kernel 4.14.161`, we modifid kernel and put `tcp_probe.c`
   
   ```
   ./setup_1.sh
   ```
4. Install UDP based CCAs(COPA, Sprout, Verus)
   ```
   ./setup_2.sh
   ```

5. Install Exll and PCC-vivace, modified iperf3, tcp_probe module
   ```
   ./setup_3.sh
   ```
6. Check the list of congestion control
   ```
    $ sysctl net.ipv4.tcp_available_congestion_control
    net.ipv4.tcp_available_congestion_control = reno cubic bbr vegas exll pcc westwood
--------
## Measure Network with CCAs

1. Config file : `source/server/setup.py` & `source/client/setup.py`

    ```
    HOST = '127.0.0.1'       # server ip address
    username = 'username'    # server username 
    PORT = 9001              # Port to listen on (non-privileged ports are > 1023) 
    interval= 0.5            # interval (s)
    duration = 30	         # duration (s)
    direction= 'download'    # or 'upload'


    def getPassword():
	return "yourpassword"    # put your ssh key password

    ```

2. SSH connection to the server: check ssh connection is working

    When you connect with `ssh` and `scp`, you shoud type `"yes"` with following message.
    
    ```
    The authenticity of host 'c220g1-030610.wisc.cloudlab.us (128.105.145.183)' can't be established.
    RSA key fingerprint is SHA256:/ooH3X5gHoyIFYFol8R2u0XpxMGgmlvRznPYsuBdGuU.
    Are you sure you want to continue connecting (yes/no)? 
    ```


3. Sysctl tunes

    ```
    sudo sysctl -w net.ipv4.tcp_wmem="16000000 16000000 256000000"
    sudo sysctl -w net.ipv4.tcp_rmem="16000000 16000000 256000000"
    sudo sysctl -w net.core.wmem_max="256000000"
    sudo sysctl -w net.core.rmem_max="256000000"
    ```
    ```
    sudo sysctl -w net.ipv4.tcp_no_metrics_save=1 # disable tcp cache
    sudo su
    echo 0 > /sys/module/tcp_cubic/parameters/hystart  # disable tcp hystart
    exit
    ```

4. Run the server and client
    * Server: If you want to test with cubic,
        ```
        rm ../../data/* ../../plot/* ../../tmpData/*  # Check the data/plot/tmpData directory is empty
        sudo sysctl -w net.ipv4.tcp_congestion_control=cubic
        python3 server.py cubic
        ```
        Every collected data and plot will save in directory `~/backup/`.

        Only BBR has different setting
        ```
        rm ../../data/* ../../plot/* ../../tmpData/* 
        sudo sysctl -w net.core.default_qdisc=fq
        sudo sysctl -w net.ipv4.tcp_congestion_control=bbr
        python3 server.py bbr
        ```

        After finishing with BBR, 
        ```
        sudo sysctl -w net.core.default_qdisc=pfifo_fast  # default value
        ```

    * Client

        --#streams 
        --background|foreground 
        --exp_count (start with 0,1,2,3,....)
        --finish_num(0:keepgoing, 1:finish)
        --cca_name(cubic, bbr, reno, exll, vegas, ppc)

        ```
        python3 client.py  --#streams --background|foreground --exp_count --finish_num(0:keepgoing, 1:finish) --cca_name
        ```

        ```
        python3 client.py 1 foreground 0 1 bbr
        ```


    * Automation Script (every CCAs)

        * Server: 
        ```
        ./run_server.sh
        ```
        
        * Client:
        ```
        ./run_client.sh # 5 times with 6 CCAs
        ./run_client_test.sh # 1 time with 6 CCAs
        ```

--------
## Error cases

1. Copa 
- when you try to build copa with `makepp`

```
username@node0:~/genericCC$ makepp
makepp: Loading makefile `/users/username/genericCC/makefile'
makepp: Entering directory `/users/username/genericCC'
protoc --cpp_out=. protobufs-default/dna.proto
makepp: Scanning `/users/username/genericCC/protobufs-default/dna.pb.cc'
makepp: Scanning `/users/username/genericCC/protobufs-default/dna.pb.h'
g++-6 -I.. -I. -O2 -fPIC -c protobufs-default/dna.pb.cc -o protobufs-default/dna.pb.o
exec g++-6 -I.. -I. -O2 -fPIC -c protobufs-default/dna.pb.cc -o protobufs-default/dna.pb.o failed--No such file or directory
makepp: error: Failed to build target `/users/username/genericCC/protobufs-default/dna.pb.o' [254]
makepp: 1 file updated and 1 target failed
```

Then, do this again

```
sudo apt install protobuf-c-compiler protobuf-compiler -y
sudo apt install libgl1-mesa-dev libboost-all-dev makepp libboost-dev libjemalloc-dev libboost-python-dev -y

sudo apt-add-repository ppa:ubuntu-toolchain-r/test -y
sudo apt update
sudo apt install g++-6 -y
```

2. ModuleNotFoundError: No module named 'apt_pkg'
```
$ sudo apt-get install --reinstall python3-apt
$ cd  /usr/lib/python3/dist-packages
$ ls -la /usr/lib/python3/dist-packages
$ sudo cp apt_pkg.cpython-35m-x86_64-linux-gnu.so apt_pkg.so
```

3. 
/# makepp
makepp: error: no targets specified and no default target in makefile `/usr/share/makepp/makepp_default_makefile.mk'

-> cd ~/genericCC
makepp