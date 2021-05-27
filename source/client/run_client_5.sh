#!/bin/bash
#reno
python3 client.py 1 foreground 0 0 reno
sleep 5
python3 client.py 1 foreground 1 0 reno
sleep 5
python3 client.py 1 foreground 2 0 reno
sleep 5
python3 client.py 1 foreground 3 0 reno
sleep 5
python3 client.py 1 foreground 4 1 reno
sleep 5
#cubic
python3 client.py 1 foreground 0 0 cubic
sleep 5
python3 client.py 1 foreground 1 0 cubic
sleep 5
python3 client.py 1 foreground 2 0 cubic
sleep 5
python3 client.py 1 foreground 3 0 cubic
sleep 5
python3 client.py 1 foreground 4 1 cubic
sleep 5
#bbr
python3 client.py 1 foreground 0 0 bbr
sleep 5
python3 client.py 1 foreground 1 0 bbr
sleep 5
python3 client.py 1 foreground 2 0 bbr
sleep 5
python3 client.py 1 foreground 3 0 bbr
sleep 5
python3 client.py 1 foreground 4 1 bbr
sleep 5
#vegas
python3 client.py 1 foreground 0 0 vegas
sleep 5
python3 client.py 1 foreground 1 0 vegas
sleep 5
python3 client.py 1 foreground 2 0 vegas
sleep 5
python3 client.py 1 foreground 3 0 vegas
sleep 5
python3 client.py 1 foreground 4 1 vegas
sleep 5
#exll

python3 client.py 1 foreground 0 0 exll
sleep 5
python3 client.py 1 foreground 1 0 exll
sleep 5
python3 client.py 1 foreground 2 0 exll
sleep 5
python3 client.py 1 foreground 3 0 exll
sleep 5
python3 client.py 1 foreground 4 1 exll
sleep 5
#pcc
python3 client.py 1 foreground 0 0 pcc
sleep 5
python3 client.py 1 foreground 1 0 pcc
sleep 5
python3 client.py 1 foreground 2 0 pcc
sleep 5
python3 client.py 1 foreground 3 0 pcc
sleep 5
python3 client.py 1 foreground 4 1 pcc
sleep 5
#westwood
# sleep 5
# python3 client.py 1 foreground 0 0
# sleep 5
# python3 client.py 1 foreground 1 0
# sleep 5
# python3 client.py 1 foreground 2 0
