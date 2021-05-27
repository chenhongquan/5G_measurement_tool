#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib as mtp
import os
import argparse
import re
import os 
import time
import sys
import sqlite3 as lite
import glob
import subprocess 
from threading import Thread
import numpy as np
from datetime import datetime
import sys
sys.path.append("../config/")
from setup import * 
from statistics import variance


folder_list = ['/home/lte-1/DATA/5g-single/CommonsPark/Good/', '/home/lte-1/DATA/5g-single/CommonsPark/Medium/', '/home/lte-1/DATA/5g-single/SloanLake/Good/', '/home/lte-1/DATA/5g-single/SloanLake/Medium/']

for folder in folder_list:

    y = glob.glob(folder+'sprout/*')
    for i in y:
        client_file = glob.glob(i+'/sprout_tput_*')
        server_file = glob.glob(i+'/sprout_rtt_*')
        output_file = i
        print(client_file[0])
        print(server_file[0])
        print(output_file)

        cmd = 'python3 plot_verus.py '+client_file[0]+' '+server_file[0]+' -o '+output_file
        print(cmd)
        os.system(cmd)