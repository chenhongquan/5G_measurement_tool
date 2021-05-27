import os 
import time
import sys
import sqlite3 as lite
import glob
import subprocess 
from yattag import Doc
from threading import Thread
sys.path.append("../config/")
from setup import *
import numpy as np 

# work done by syslabshare1
# before run this file, need to install "sudo apt install plotutils"
# This is for plotting tcpprobe
print("re_plot_for_koea.py started")

# TODO: make a configure file
# duration = 70	# str(duration)
# ClientState = 'foreground'	# ClientState
# ClientStreams = 1
# exp_count = 1
# proto= 'none'
tcp_cc_list = ['reno','cubic','bbr','vegas','westwood','exll','pcc']
c2tcp_list = ['c2tcp']
tmp_dir = '/mydata/www/html/tmp'
dir_list = os.listdir(tmp_dir)
# dir_list = ['server_1-2020-10-17-1602868444-reno']

for dir in dir_list:
    three_flows_set = os.listdir(tmp_dir+'/'+dir)
    print(three_flows_set)
    proto= dir.split("-")[5]
    print(proto)

    if c2tcp_list.count(proto) > 0 :
        for i in range(3):
            data_files=os.listdir(tmp_dir+'/'+dir+'/'+three_flows_set[i]+'/')
            data_dir = tmp_dir+'/'+dir+'/'+three_flows_set[i]
            
            # os.system('python3 plot_tcp_other.py 70 foreground 1 1 '+proto+' '+data_dir+' '+data_dir)
            #  data_files = os.listdir(data_dir+'/'+dir+'/'+three_flows_set[i]+'/')
            #  print(three_flows)
            #  print(data_dir+'/'+dir_case[i]+'/')


###### when you want to re-draw tcp_probe figure #####
# for dir in dir_list:
#     three_flows_set = os.listdir(tmp_dir+'/'+dir)
#     print(three_flows_set)
#     proto= dir.split("-")[5]
#     print(proto)
#     if tcp_cc_list.count(proto) > 0 :
#         for i in range(3):
#             data_files=os.listdir(tmp_dir+'/'+dir+'/'+three_flows_set[i]+'/data/data/')
#             data_dir = tmp_dir+'/'+dir+'/'+three_flows_set[i]+'/data/data'
#             result_dir = tmp_dir+'/'+dir+'/'+three_flows_set[i]+'/plot'
#             os.system('python3 plot_tcp_other.py 70 foreground 1 1 '+proto+' '+data_dir+' '+result_dir)
#     else:
#         for i in range(3):
#             data_files=os.listdir(tmp_dir+'/'+dir+'/'+three_flows_set[i]+'/')
#             data_dir = tmp_dir+'/'+dir+'/'+three_flows_set[i]
#             os.system('python3 plot_tcp_other.py 70 foreground 1 1 '+proto+' '+data_dir+' '+data_dir)
#             #  data_files = os.listdir(data_dir+'/'+dir+'/'+three_flows_set[i]+'/')
#             #  print(three_flows)
#             #  print(data_dir+'/'+dir_case[i]+'/')