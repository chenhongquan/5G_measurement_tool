#!/usr/bin/env python3
import socket
import os, sys, time
import _thread as thread
from yattag import Doc
import subprocess
import pexpect
from os import path
from datetime import datetime
from datetime import date

multi = False # Ture: with 3 flows, False: with 1 flows

src_dir = path.abspath(path.join(path.dirname(__file__), os.pardir))
home_dir = path.abspath(path.join(src_dir, os.pardir))
base_dir = path.abspath(path.join(home_dir, os.pardir))

exe_dir = path.join(home_dir, 'source', 'server')
data_dir = path.join(home_dir, 'data')
result_dir = path.join(home_dir, 'plot')
tmp_dir = path.join(home_dir, 'tmpData')
backup_dir = path.join(base_dir, 'backup')

len_dir=len(data_dir)+1

# import socket
# S_HOST = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
# print([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])

import sh
ip_list = [ip.split()[1][5:] for ip in filter(lambda x: 'inet addr' in x, sh.ifconfig().split("\n"))]
S_HOST = ip_list[0]
print(ip_list)
print(S_HOST)

if S_HOST == '000.000.000.000': # 1st server
	HOST = '000.000.000.000' 
	username = 'user'   
	workspace = '/users/'+username # +'/5G_measurement_tool/'
	server_name = 'server_1'
	duration =60	 #(second)	
# elif S_HOST == '000.000.000.000': # 2nd server
# 	HOST = '000.000.000.000' # 
# 	username = 'user'   
# 	workspace = '/users/'+username # +'/5G_measurement_tool/'
# 	server_name = 'server_2'
# 	duration =60	 #(second)	
# elif S_HOST == '000.000.000.000': # 3rd server
# 	HOST = '000.000.000.0006' # 
# 	username = 'user'   
# 	workspace = '/users/'+username
# 	server_name = 'server_3'
# 	duration =60	 #(second)	
else:
	cwd = os.getcwd()
	print(cwd)
	if cwd == '/home/lte-1/5G_measurement_tool/source/client':
		HOST = '000.000.000.000' 
		username = 'user'   
		workspace = '/users/'+username # +'/5G_measurement_tool/'
		server_name = 'server_1'
		device = '[your device ID]' # find the ID with "adb devices"
		duration =60	 #(second)	

# server_name='server_1'
PORT = 9001        # Port to listen on (non-privileged ports are > 1023)
ClientPORT = '9001' 
interval= 0.2    #(second)
id_rsa = 'scp -i ../../ssh_key/id_rsa' # % if your server need to connect with ssh_key
copa_receiver_file_name = 'receiver_co'

# id_rsa = 'scp ' # purdue
# copa_receiver_file_name = 'receiver' # purdue

exp_id = 1		
direction= 'download' # or 'upload' if you want to test uplink
dqote = '"'
pqote = '<'
hqote = '>'

today = date.today()  
print("Today's date:", today)

def getPassword(): 
	return "password"  # change this with your password


def upload_file(comm):
	print("Start upload files")
	var_password  = "password"
	var_child = pexpect.spawn(comm)
	i = var_child.expect(["Enter passphrase for key", pexpect.EOF])
	var_child.sendline(var_password)
	var_child.expect(pexpect.EOF)

def download_file(comm):
	print("Start upload files")
	var_password  = "password"
	var_child = pexpect.spawn(comm)
	i = var_child.expect(["Enter passphrase for key", pexpect.EOF])
	var_child.sendline(var_password)
	var_child.expect(pexpect.EOF)

# if server_name=='server_3':
# 	def upload_file(comm):
# 		print("Start upload files")
# 		var_password  = "nxcmsnl"
# 		var_child = pexpect.spawn(comm)
# 		i = var_child.expect(["root@000.000.000.000's password:", pexpect.EOF])
# 		var_child.sendline(var_password)
# 		var_child.expect(pexpect.EOF)
		
def cmd_run(cmd):
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	process.wait()

def get_sec(time_str):
    """Get Seconds from time."""
    # h, m, s = time_str.split(':')
    # return float(m) * 60 + float(s)
    h= time_str.split(':')[0]
    m= time_str.split(':')[1]
    s= time_str.split(':')[2].split('.')[0]
    microsecond= time_str.split(':')[2].split('.')[1]
    return (int(m)*60) + int(s) + (int(microsecond)/1000000)

# from adbutils import adb

# for d in adb.devices():
#     print(d.serial) # print device serial

# d = adb.device(serial='R3CN30C4XGP')
# # d = adb.device(serial=device)

# # You do not need to offer serial if only one device connected
# # RuntimeError will be raised if multi device connected
# d = adb.device()
# serial_type = d.shell(["cat", "sys/class/thermal/thermal_zone*/type"])
# serial_temp = d.shell(["cat", "sys/class/thermal/thermal_zone*/temp"])
# serial_mode = d.shell(["cat", "sys/class/thermal/thermal_zone*/mode"])
# dumpsys = d.shell("dumpsys telephony.registry | grep -i CellSignalStrength")

# d.shell("sleep interval", timeout=interval)

# print(dumpsys)