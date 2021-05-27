#!/usr/bin/env python3
import socket
import os, sys, time
import _thread as thread
from yattag import Doc
import sys
sys.path.append("../config/")
from setup import * 
from os import path
from datetime import date
import subprocess
import pexpect

exp_count = 0
x="%.0f"%time.time()
sprout_name="Sprout_"+str(today)+"_"+str(x)
proto = 'sprout'

cc_repo = path.join(base_dir, 'sprout')
model = path.join(cc_repo, 'src', 'examples', 'sprout.model')
src = path.join(cc_repo, 'src', 'examples', 'sproutbt2')
new_result_dir = path.join(data_dir, sprout_name)

cmd = 'mkdir ' + new_result_dir
os.system(cmd)

s_time = "%.0f"%time.time()
# sproutbt2
# ./sproutbt2 128.105.145.173 60001
# tmp_file_name = data_dir+'/'+rtt_filename
# '/users/"+username+"/sprout/src/example/sproutbt2 2>&1 | tee ../../data/timeout_test.txt'
# client_command = src+' '+HOST+' 60001'
# print('client_command is '+client_command)
# p2 = subprocess.Popen(client_command, stderr = subprocess.PIPE, shell=True)
# var_command = "scp "+new_result_dir+'/'+cellfilename+" "+username+"@"+HOST+":"+workspace+"/5G_measurement_tool/data/"
# print(var_command)
# upload_file(var_command)
# try:
#     download_file(var_command)
# except:
#     os.system(var_command)

# tar_cmp = 'tar -xvf '+new_result_dir+'/sprout.tar.gz -C '+new_result_dir+'/'+' --strip-components=3'
# os.system(tar_cmp)

# plot_file = 'new_plot_from_udp.py'
# dir_list = os.listdir(new_result_dir)
# # dir = dir_list[0]
# for dir in dir_list:
#     if dir.find('tput') >= 0:
#         tput = dir
#     if dir.find('rtt')>=0:
#         rtt = dir

# # python3 new_plot_from_udp.py readfilename filename(wrt) CCA_name
# cmd = 'python3 '+plot_file+' '+new_result_dir+'/'+tput+' '+new_result_dir+'/'+rtt+' '+new_result_dir+'/sprout_figure'+' '+'sprout'
# print(cmd)
# os.system(cmd)

# tar_cmd = 'tar -cvf '+new_result_dir+'.tar.gz '+new_result_dir
# os.system(tar_cmd)

# var_command = "scp  "+new_result_dir+".tar.gz " +username+"@"+HOST+":/var/www/html/tmp/"
# print(var_command)
# upload_file(var_command)

# # Client 
# cd ~5g/sprout/build/src/examples
# ./sproutbt2 128.105.145.173 60001