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
c2tcp_name="c2tcp_"+str(today)+"_"+str(x)
proto = 'c2tcp'
# cc_repo = path.join(base_dir, 'sprout')
# model = path.join(cc_repo, 'src', 'examples', 'sprout.model')
# src = path.join(cc_repo, 'src', 'examples', 'sproutbt2')
# src = path.join(cc_repo, 'src', 'examples', 'sproutbt2')
new_result_dir = path.join(data_dir, c2tcp_name)

cmd = 'mkdir ' + new_result_dir
os.system(cmd)

s_time = "%.0f"%time.time()

client_command = 'adb -s '+device+' shell /data/local/tmp/client '+HOST+' 1 '+str(PORT)
print('client_command is '+client_command)
p2 = subprocess.Popen(client_command, stderr = subprocess.PIPE, shell=True)

cellfilename="CellInfoClient_"+proto+"_"+str(today)+"_"+str(x)+".txt"
print("Run cellinfo.py")
cellInfo_cmd='python3 cellinfo.py '+str(interval)+'  '+str(duration)+'  '+new_result_dir+'/'+cellfilename+'  '+str(exp_count)+' &'
p3 = subprocess.Popen(cellInfo_cmd, stderr = subprocess.PIPE, shell=True)

c_time = "%.0f"%time.time()
while(1):
    # print(float(c_time)-float(s_time))
    if float(c_time)-float(s_time) > float(duration+30):
        # print(float(c_time)-float(s_time))
        os.system('killall -9 adb')
        # os.system('killall -9 tcpdump')
        break
    else:
        c_time = "%.0f"%time.time()


var_command = "scp "+new_result_dir+'/'+cellfilename+" "+username+"@"+HOST+":"+workspace+"/5G_measurement_tool/data/"
print(var_command)
upload_file(var_command)
# try:
#     download_file(var_command)
# except:
#     os.system(var_command)

# tar_cmp = 'tar -xvf '+new_result_dir+'/c2tcp.tar.gz -C '+new_result_dir+'/'+' --strip-components=3'
# os.system(tar_cmp)

# plot_file = 'new_plot_from_tcp.py'
# dir_list = os.listdir(new_result_dir)
# # dir = dir_list[0]
# tcpprobe = ''
# for dir in dir_list:
#     if dir.find('c2tcp_2020') >= 0 and dir.find('Cell') < 0 :
#         tput = dir
#     elif  dir.find('tcpprobe_') >= 0 and dir.find('png') < 0 :
#         tcpprobe = dir

# # cmd = 'python3 '+plot_file+' '+new_result_dir+'/'+dir+' '+ new_result_dir+'/figire'
# # os.system(cmd)

# # python3 new_plot_from_udp.py readfilename filename(wrt) CCA_name
# cmd = 'python3 '+plot_file+' '+new_result_dir+'/'+tput+' '+new_result_dir+'/'+tcpprobe+' '+new_result_dir+'/ '+proto
# print(cmd)
# os.system(cmd)

# if tcpprobe !='':
#     print('python3 ../server/plot_tcp_other.py '+str(duration)+' foreground 1 1 c2tcp')
#     os.system('python3 ../server/plot_tcp_other.py '+str(duration)+' foreground 1 1 c2tcp')
#     os.system('mv ../../plot/* '+new_result_dir)

# tar_cmd = 'tar -cvf '+new_result_dir+'.tar.gz '+new_result_dir
# os.system(tar_cmd)

# var_command = "scp  "+new_result_dir+".tar.gz " +username+"@"+HOST+":/var/www/html/tmp/"
# print(var_command)
# upload_file(var_command)

# # Client 
# cd ~5g/sprout/build/src/examples
# ./sproutbt2 128.105.145.173 60001
