#!/bin/bash
#reno
python3 client.py 1 foreground 0 1 reno
sleep 5
#cubic
python3 client.py 1 foreground 0 1 cubic
sleep 5
#bbr
python3 client.py 1 foreground 0 1 bbr
sleep 5
#vegas
python3 client.py 1 foreground 0 1 vegas
#exll
sleep 5
python3 client.py 1 foreground 0 1 exll
#pcc
sleep 5
python3 client.py 1 foreground 0 1 pcc
#westwood
# sleep 5
# python3 client.py 1 foreground 0 0
# sleep 5
# python3 client.py 1 foreground 1 0
# sleep 5
# python3 client.py 1 foreground 2 1