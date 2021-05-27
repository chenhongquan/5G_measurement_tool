#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib as mtp
import os
import argparse
import re
import time
import sys
import sqlite3 as lite
import glob
import subprocess 
from threading import Thread
import numpy as np
from datetime import datetime
sys.path.append("../config/")
from setup import * 
from statistics import variance

folder_list = ['/home/lte-1/5G_measurement_tool/data/']
proto = 'copa'
for folder in folder_list:
    y = glob.glob(folder+'*')
    for i in y:
        client_file = glob.glob(i+'/'+proto+'_tput*.txt')
        tcp_probe_file = glob.glob(i+'/tcp*.txt')
        if proto == 'copa':
            rtt_file = glob.glob(i+'/'+proto+'_rtt*.txt')
        # server_file = glob.glob(i+'/Receiver.out')
        output_file = i+'/'+proto
        # print(client_file[0])
        # print(tcp_probe_file[0])
        if proto == 'copa':
            print(client_file)
            if client_file == []:
                client_file = glob.glob(i+'/'+proto+'*.txt')
                cmd = 'python3 new_plot_from_udp.py '+client_file[0]+' '+client_file[0][:-4]+' '+output_file+' '+proto
            else:
                cmd = 'python3 new_plot_from_udp.py '+client_file[0]+' '+rtt_file[0]+' '+output_file+' '+proto
        else:
            cmd = 'python3 new_plot_from_tcp.py '+client_file[0]+' '+tcp_probe_file[0]+' '+output_file+' '+proto
        print(cmd)
        os.system(cmd)

        # # print(server_file[0])
        # print(output_file)

        # cmd = 'python3 new_plot_from_tcp.py '+client_file[0]+' '+output_file+' '+proto
        # print(cmd)
        # os.system(cmd)