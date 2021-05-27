#!/usr/bin/env python3
import socket
import time
import os
import sys
import pexpect
import subprocess as sp
import sys
sys.path.append("../config/")
from setup import * 
try:
	cmd = 'mkdir ../../data ../../plot ../../tmpData'
	os.system(cmd)
	cmd = 'chmod 600 ../../ssh_key/*'
	os.system(cmd)
except:
	print("all directory ready")

if(len(sys.argv)<4):
	print ("Usage error: --#streams --background|foreground --exp_count --finish_num(0:keepgoing, 1:finish)")
	exit()

streams=sys.argv[1]
state=sys.argv[2] # background|foreground
exp_count=sys.argv[3]
finish_num=sys.argv[4]
filename=""
x=""
cellfilename=""

# Get IP address from the phone : need to be connected to internet
setting_ip_cmd = "adb -s "+device+" shell ip addr show rmnet_data1 | grep 'inet' | cut -d' ' -f6|cut -d/ -f1 > client_ip_addr.txt"
os.system(setting_ip_cmd)

f = open('client_ip_addr.txt', 'r')
lines = f.read().splitlines()
f.close()
# print(lines)
try: # rmnet_data1 
	ClientIP = lines[0]
except:
	try: # rmnet_data2
		setting_ip_cmd = "adb -s "+device+" shell ip addr show rmnet_data2 | grep 'inet' | cut -d' ' -f6|cut -d/ -f1 > client_ip_addr.txt"
		os.system(setting_ip_cmd)
		f = open('client_ip_addr.txt', 'r')
		lines = f.read().splitlines()
		f.close()
		# print(lines)
		ClientIP = lines[0]
	except: # wifi wlan0, for debugging
		setting_ip_cmd = "adb -s "+device+" shell ip addr show wlan0 | grep 'inet' | cut -d' ' -f6|cut -d/ -f1 > client_ip_addr.txt"
		os.system(setting_ip_cmd)
		f = open('client_ip_addr.txt', 'r')
		lines = f.read().splitlines()
		f.close()
		# print(lines)
		ClientIP = lines[0]
		print("This is wifi")
	# continue

print("Check the server is on")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, 5000))
	addr=s.getsockname()
	while True:
		print("Ready for starting iperf3")
		if("download" in direction):
			msg='Can I start download '+state+' '+ClientIP+' '+str(streams)+' '+str(exp_count)+' '+str(finish_num) 
			s.send(bytes(msg, 'utf-8'))
		else:
			msg='Can I start upload '+state+' '+ClientIP+' '+str(streams)+' '+str(exp_count)+' '+str(finish_num) 
			s.send(bytes(msg, 'utf-8'))
		data = s.recv(1024)
		print('Received', repr(data))
		if("no: change the port" in data.decode("utf-8")):
			print ("Use different port for iperf as port being in use")
			exit()
		if("yes" in data.decode("utf-8")):
			x="%.0f"%time.time()
			filename="Client_"+ClientIP+'_'+ClientPORT+'_'+HOST+"_"+str(PORT)+"_"+direction+"_"+str(streams)+"_"+str(state)+"_"+str(x)+"_"+str(exp_count)+".txt"			
			cellfilename="CellInfoClient_"+ClientIP+'_'+ClientPORT+'_'+HOST+"_"+str(PORT)+"_"+direction+"_"+str(streams)+"_"+str(state)+"_"+str(x)+"_"+str(exp_count)+".txt"
			# if(state in "background"):
			# 	filename="Client_"+ClientIP+'_'+ClientPORT+'_'+HOST+"_"+str(PORT)+"_"+direction+"_bg.txt"
			# 	cellfilename="CellInfoClient_"+ClientIP+'_'+ClientPORT+'_'+HOST+"_"+str(PORT)+"_"+direction+'_'+str(x)+'_'+str(exp_count)+"_bg.txt"
			if("download" in direction):
				# print(proto)
				# cmd='adb -s '+device+' shell "/data/local/tmp/iperf3 -c 128.105.145.173 -p 9001 -V -R -t 10 -i 0.5  > /sdcard/test.txt"
				cmd='adb -s '+device+' shell '+dqote+'/data/local/tmp/iperf3 -c '+HOST+' -p '+str(PORT)+'  -V -R -t '+str(duration)+' -i '+str(interval)+' -P '+str(streams)+' -f m > /sdcard/'+filename+dqote
			else:
				cmd='adb -s '+device+' shell '+dqote+'/data/local/tmp/iperf3 -c '+HOST+' -p '+str(PORT)+'  -V -t '+str(duration)+' -i '+str(interval)+' -P '+str(streams)+' -f m > /sdcard/'+filename+dqote
			#cmd="ls"
			#print (cmd)
			# cellfilename="CellInfoClient_"+ClientIP+'_'+ClientPORT+'_'+HOST+"_"+str(PORT)+"_"+direction+"_"+str(streams)+"_"+str(state)+"_"+str(x)+"_"+str(exp_count)+".txt"
			print("Run cellinfo.py")
			cellInfo_cmd='python3 cellinfo.py '+str(interval)+'  '+str(duration)+'  '+data_dir+'/'+cellfilename+'  '+str(exp_count)+' &'
			os.system(cellInfo_cmd)
			print("Run iperf3")
			pipe=sp.Popen(cmd,shell=True)
			res = pipe.communicate()
			# print ("stderr:",res[1])		
			# print ("stdout:",res[0])
			# print (data)
			# if(res[1]!=None):
			# 	s.close()
			# 	exit()
			# else:
			print("iperf complete")
			#write_file="pClient_"+HOST+"_"+str(PORT)+"_"+str(x)+"_"+str(exp_count)+".txt"
			cmd_get_file_from_phone='adb -s '+device+' pull /sdcard/'+filename+' '+tmp_dir+'/'				
			os.system(cmd_get_file_from_phone)
			# Client_100.125.111.130_9001_128.105.145.173_9001_download_1_foreground_1595651931_0.txt
			write_file="pClient_"+HOST+"_"+str(PORT)+"_"+ClientIP+"_"+str(ClientPORT)+"_"+direction+"_"+str(streams)+"_"+str(state)+"_"+str(x)+"_"+str(exp_count)+".txt"
			if(state in "background"):
				write_file="pClient_"+HOST+"_"+str(PORT)+"_"+ClientIP+"_"+str(ClientPORT)+"_"+direction+"_"+str(streams)+"_"+str(state)+"_"+str(x)+"_"+str(exp_count)+".txt"
			cmd="python3 parser.py "+tmp_dir+'/'+filename+" "+str(interval)+" "+data_dir+'/'+write_file+" "+str(streams)
			print("run parser.py")
			os.system(cmd)
			# exp_count+=1
			# Upload the tmpData files onto the server	
			var_command = id_rsa+" "+tmp_dir+'/'+filename+" "+username+"@"+HOST+":"+workspace+"/5G_measurement_tool/tmpData/"	
			print(var_command)
			upload_file(var_command)
			# Upload the files onto the server	
			var_command = id_rsa+" "+data_dir+'/'+write_file+" "+username+"@"+HOST+":"+workspace+"/5G_measurement_tool/data/"	
			print(var_command)
			upload_file(var_command) 
			#Upload cellinfo file
			var_command = id_rsa+" "+data_dir+'/'+cellfilename+" "+username+"@"+HOST+":"+workspace+"/5G_measurement_tool/data/"
			print(var_command)
			upload_file(var_command)
			var_command = id_rsa+" "+data_dir+'/'+cellfilename[:-4]+"_temp.txt "+username+"@"+HOST+":"+workspace+"/5G_measurement_tool/data/"
			print(var_command)
			upload_file(var_command)
			s.send(b'Done')
			exit()
				
	s.close()
