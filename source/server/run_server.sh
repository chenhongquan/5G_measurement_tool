#!/bin/bash
echo "Starting Server with reno"

sysctl net.ipv4.tcp_available_congestion_control

sudo sysctl -w net.ipv4.tcp_wmem="16000000 16000000 256000000"
sudo sysctl -w net.ipv4.tcp_rmem="16000000 16000000 256000000"
sudo sysctl -w net.core.wmem_max="256000000"
sudo sysctl -w net.core.rmem_max="256000000"

sudo sysctl -w net.ipv4.tcp_no_metrics_save=1 # disable tcp cache
# sudo su
# echo 0 > /sys/module/tcp_cubic/parameters/hystart  # disable tcp hystart
# exit

sudo sysctl net.ipv4.tcp_available_congestion_control
rm ../../data/* ../../plot/* ../../tmpData/* 


python3 server.py reno

python3 server.py cubic

sudo sysctl -w net.core.default_qdisc=fq
python3 server.py bbr

sudo sysctl -w net.core.default_qdisc=pfifo_fast
python3 server.py vegas

python3 server.py exll

python3 server.py pcc

# reset
sudo sysctl -w net.ipv4.tcp_congestion_control=cubic
sudo sysctl -w net.core.default_qdisc=pfifo_fast
sudo sysctl -w net.ipv4.tcp_no_metrics_save=1
sudo sysctl -w net.ipv4.tcp_c2tcp_enable=0
tar -cvf ~/backup.tar.gz ~/backup
rm -rf  ~/backup

# # for sprout,verus,copa,c2tcp
# sudo sysctl -w net.ipv4.tcp_congestion_control=cubic

# #sprout
# python3 server.py sprout
# rm ../../data/* ../../plot/* ../../tmpData 

# #verus
# python3 server.py verus
# rm ../../data/* ../../plot/* ../../tmpData 

# #copa
# python3 server.py copa
# rm ../../data/* ../../plot/* ../../tmpData 

# #c2tcp
# python3 server.py c2tcp
# rm ../../data/* ../../plot/* ../../tmpData 
