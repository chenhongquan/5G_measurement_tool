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

proto = 'verus'
exp_count = 0
x="%.0f"%time.time()
result_dir_name="verus_"+str(today)+"_"+str(x)
result_filename="verus_"+str(today)+"_"+str(x)+'.txt'

cc_repo = path.join(base_dir, 'verus')
src = path.join(cc_repo, 'src', 'verus_client')

new_verus_result_dir = path.join(data_dir, result_dir_name)

cmd = 'mkdir ' + new_verus_result_dir
os.system(cmd)

s_time = "%.0f"%time.time()
client_command = 'adb -s '+device+' shell /data/local/tmp/verus_client '+HOST+' -p 9001'
print('client_command is '+client_command)
p2 = subprocess.Popen(client_command, stderr = subprocess.PIPE, shell=True) 
# verus_server result: Losses.out Receiver.out Verus.out
# rtt_command = src+' ' +HOST+' -p '+str(PORT)+' > ' + result_filename
# print(rtt_command)
# p1 = subprocess.Popen(rtt_command, stderr = subprocess.PIPE, shell=True) 

# cellfilename="CellInfoClient_"+proto+"_"+str(today)+"_"+str(x)+".txt"
# print("Run cellinfo.py")
# cellInfo_cmd='python3 cellinfo.py '+str(interval)+'  '+str(duration)+'  '+new_verus_result_dir+'/'+cellfilename+'  '+str(exp_count)+' &'
# p3 = subprocess.Popen(cellInfo_cmd, stderr = subprocess.PIPE, shell=True)

duration_1 = int(duration) + 10
time.sleep(duration_1)

# cp_cmp = 'adb pull /data/local/tmp/client_9001.out '+new_verus_result_dir
# os.system(cp_cmp)

# cp_cmp = 'cp '+result_filename+' '+new_verus_result_dir
# os.system(cp_cmp)

# var_command = "scp ./client_9001.out "+username+"@"+HOST+":"+workspace+"/5G_measurement_tool/data/"
# print(var_command)
# upload_file(var_command)

# cp_cmp = 'rm ./client_9001.out'
# os.system(cp_cmp)

# var_command = "scp  "+username+"@"+HOST+":"+workspace+"/verus.tar.gz "+ new_verus_result_dir
# print(var_command)
# upload_file(var_command)
# try:
#     download_file(var_command)
# except:
#     os.system(var_command)

# tar_cmp = 'tar -xvf '+new_verus_result_dir+"/verus.tar.gz -C "+new_verus_result_dir+" --strip-components=4"
# os.system(tar_cmp)

# verus_plot_file = 'plot_verus.py'

# cmd = 'python3 '+verus_plot_file+' '+new_verus_result_dir+'/Receiver.out  -o '+new_verus_result_dir
# os.system(cmd)

# plot_file = 'new_plot_from_udp.py'
# dir_list = os.listdir(new_verus_result_dir)
# # dir = dir_list[0]
# print(dir_list)
# for dir in dir_list:
#     if dir.find('verus_tput_')>= 0:
#         tput = dir
#     if dir.find('Receiver.out')>=0:
#         rtt = dir

# # python3 new_plot_from_udp.py readfilename filename(wrt) CCA_name
# cmd = 'python3 '+plot_file+' '+new_verus_result_dir+'/'+tput+' '+new_verus_result_dir+'/'+rtt+' '+new_verus_result_dir+'/verus_figure'+' '+'verus'
# print(cmd)
# os.system(cmd)

# tar_cmd = 'tar -cvf '+new_verus_result_dir+'.tar.gz '+new_verus_result_dir
# os.system(tar_cmd)

# var_command = "scp  "+new_verus_result_dir+".tar.gz " +username+"@"+HOST+":/var/www/html/tmp/"
# print(var_command)
# upload_file(var_command)

# python3 ~/verus/tools/plot.py client_9001.out Receiver.out  -o ./