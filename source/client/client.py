#!/usr/bin/env python3
import socket
import os, sys, time
import subprocess
import _thread as thread
from yattag import Doc
import sys
sys.path.append("../config/")
from setup import * 

cmd = 'mkdir ../../data ../../plot ../../tmpData'
os.system(cmd)
cmd = 'chmod 600 ../../ssh_key/*'
os.system(cmd)

if(len(sys.argv)<4):
	print ("Usage error: --#streams --background|foreground --exp_count --finish_num(0:keepgoing, 1:finish)")
	exit()

streams=sys.argv[1]
state=sys.argv[2] # background|foreground
exp_count=sys.argv[3]
finish_num=sys.argv[4]
proto=sys.argv[5]

if not os.path.exists(data_dir+'/'):
    os.makedirs(data_dir+'/')
if not os.path.exists(result_dir+'/'):
    os.makedirs(result_dir+'/')
if not os.path.exists(tmp_dir+'/'):
    os.makedirs(tmp_dir+'/')

today = date.today()
x="%.0f"%time.time()
filename=""
x=""
cellfilename=""
tcp_cc_list = ['reno','cubic','bbr','vegas','westwood','exll','pcc']

if tcp_cc_list.count(proto) > 0 :
	cmd = 'python3 client_tcp_cc.py '+streams+' '+state+' '+str(exp_count)+' '+str(finish_num)
	os.system(cmd)
else:
	if proto == 'sprout':
		# run client
		cmd = 'python3 run_sprout.py'
		os.system(cmd)
	elif proto == 'verus':
		# run client
		cmd = 'python3 run_verus_app.py'
		os.system(cmd)
	elif proto == 'copa':
		# run client
		cmd = 'python3 run_copa.py'
		os.system(cmd)
	elif proto == 'c2tcp':
		# run client
		cmd = 'python3 run_c2tcp.py'
		os.system(cmd)