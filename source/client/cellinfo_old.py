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
from adbutils import adb

if(len(sys.argv)<5):
	print("--interval --duration --filename --exp_id")
	exit()
# cellInfo_cmd='python3 cellinfo.py '+str(interval)+'  '+str(duration)+'  '+data_dir+'/'+cellfilename+'  '+str(exp_count)+' &'
# interval=float(sys.argv[1])
# interval = 1 
duration=int(sys.argv[2])
filename=sys.argv[3]
exp_id=sys.argv[4]
starttime=int("%.0f"%time.time())
index=0
pindex=0
mnc = 0
mcc = 0
# cellfilename="CellInfoClient_"+ClientIP+'_'+ClientPORT+'_'+HOST+"_"+str(PORT)+"_"+direction+"_"+str(streams)+"_"+str(state)+"_"+str(x)+"_"+str(exp_count)+".txt"
for d in adb.devices():
	d = adb.device(serial='R3CN30C4XGP')
	# d = adb.device(serial=device)
fd=open(filename,"w")
while(True):
	curtime=int("%.0f"%time.time())



	# You do not need to offer serial if only one device connected
	# RuntimeError will be raised if multi device connected
	d = adb.device()
	serial_type = d.shell(["cat", "sys/class/thermal/thermal_zone*/type"])
	serial_temp = d.shell(["cat", "sys/class/thermal/thermal_zone*/temp"])
	serial_mode = d.shell(["cat", "sys/class/thermal/thermal_zone*/mode"])
	dumpsys = d.shell("dumpsys telephony.registry | grep -i CellSignalStrength")

	d.shell("sleep interval", timeout=interval)

	# p=sp.Popen("adb -s "+device+" shell dumpsys telephony.registry | grep -i CellSignalStrength",shell=True,stdout=sp.PIPE)	
	# out,err=p.communicate()
	# # print (out,err)
	# param=out.decode("utf-8").split('\n')
	
	out = dumpsys
	param=out.decode("utf-8").split('\n')

	ss_param = param[0].split(',')  #  mSignalStrength=SignalStrength: ....
	ci_param = param[1]  #	mCellInfo=[CellInfoLte:{mRegistered=YES ....
	# print(ci_param)
	# print(ss_param[4])
	# print(ss_param[5])
	if ss_param[4].find("Lte")>=0:
		# Serving service is LTE
		# print('lte')
		cell_service = 'LTE'
		signal = ss_param[4].split()
		rssi=int(signal[1].split("=")[1])
		rsrp=int(signal[2].split("=")[1])
		rsrq=int(signal[3].split("=")[1])
		rssnr=int(signal[4].split("=")[1])
		cqi=int(signal[5].split("=")[1])

		registered_ci_param=ci_param.split(',')[0]
		try:
			registered_ci_param_1=ci_param.split(',')[1]
			registered_ci_param_1_new = registered_ci_param_1.split()
		except:
			# print('lte')
			registered_ci_param_1 = 0
		registered_ci_param_new = registered_ci_param.split()

		# print(registered_ci_param_1)
		pci=int(registered_ci_param_new[5].split("=")[1])
		Tac=int(registered_ci_param_new[6].split("=")[1])
		earfcn=int(registered_ci_param_new[7].split("=")[1])
		bandwidth=int(registered_ci_param_new[8].split("=")[1])
		if registered_ci_param_new[9].split("=")[1] == None:
			try:
				mcc=int(registered_ci_param_new_1[9].split("=")[1])
				mnc=int(registered_ci_param_new_1[10].split("=")[1])
			except:
				mcc = 0
				mnc = 0
				# print("Can't get mcc and mnc")
		else:
			try:
				mcc=int(registered_ci_param_new[9].split("=")[1])
				mnc=int(registered_ci_param_new[10].split("=")[1])
			except:
				mcc = 0
				mnc = 0
		
		# print ("Time in ms",float(curtime-starttime),"RSSI:",rssi,"RSRP:",rsrp,"RSRQ:",rsrq,"SNR:",rssnr,"CQI:",cqi,"PCI:",pci,"EARFCN:",earfcn)
		wstr="Service: "+cell_service+" Time: "+str(float(curtime-starttime))+" RSSI: "+str(rssi)+" RSRP: "+str(rsrp)+" RSRQ: "+str(rsrq)+" SNR: "+str(rssnr)+" CQI: "+str(cqi)+" PCI: "+str(pci)+" TAC: "+str(Tac)+" EARFCN: "+str(earfcn)+" Bandwidth: "+str(bandwidth)+" mcc: "+str(mcc)+" mnc: "+str(mnc)+"\n"

	# mLte=CellSignalStrengthLte: rssi=-51 rsrp=-64 rsrq=-10 rssnr=246 cqi=2147483647 ta=2147483647 level=4
	# mNr=CellSignalStrengthNr:{ csiRsrp = 2147483647 csiRsrq = 2147483647 csiSinr = 2147483647 ssRsrp = -92 ssRsrq = -11 ssSinr = 14 level = 0 }


	if ss_param[5].find("Invalid")<0:
		# Serving service is NR, 5G
		# print('5G')
		
		signal = ss_param[5].split()
		# [1'mNr=CellSignalStrengthNr:{', 2'csiRsrp', 3'=', 4'2147483647', 5'csiRsrq', 6'=', 7'2147483647', 8'csiSinr', 9'=', 10'2147483647', 
		# 11'ssRsrp', 12'=', 13'-92', 14'ssRsrq', 15'=', 16'-11', 17'ssSinr',18 '=', 19'14', 20'level', 21'=', 22'0', 23'}']
		try:
			rssi=signal[3] # csiRsrp
			rsrp=signal[12]  # ssRsrp
			rsrq=signal[15]  # ssRsrq
			rssnr=signal[18]  # ssSinr
			cqi=0 #signal[22] # leve
			cell_service = '5G'
			wstr="Service: "+cell_service+" Time: "+str(float(curtime-starttime))+" RSSI: "+str(rssi)+" RSRP: "+str(rsrp)+" RSRQ: "+str(rsrq)+" SNR: "+str(rssnr)+" CQI: "+str(cqi)+" PCI: "+str(pci)+" TAC: "+str(Tac)+" EARFCN: "+str(earfcn)+" Bandwidth: "+str(bandwidth)+" mcc: "+str(mcc)+" mnc: "+str(mnc)+"\n"
		except:
			rsrp=signal[12]
			cell_service = '5G'
	# print(wstr)
	fd.write(wstr)

	# print(float(duration-curtime+starttime))
	if(curtime-starttime>duration):
		break
	
	time.sleep(interval)

fd.close()