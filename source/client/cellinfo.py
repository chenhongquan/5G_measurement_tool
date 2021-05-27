from adbutils import adb
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
import numpy as np

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
earfcn = 0
bandwidth = 0
pci =0


fd=open(filename,"w")

# for d in adb.devices():
#     print(d.serial) # print device serial

# d = adb.device(serial='R3CN607BYTL') 
# d = adb.device(serial='R3CN30C4XGP') 
d = adb.device(serial=device)

# You do not need to offer serial if only one device connected
# RuntimeError will be raised if multi device connected
# d = adb.device()
serial_type = d.shell(["cat", "sys/class/thermal/thermal_zone*/type"])
s_type = serial_type.split('\n')
s_type.insert(0, 'time')
a = np.empty([len(s_type),1])
a = np.array([s_type])
# a_trans = a.transpose()

while(True):
    curtime=int("%.0f"%time.time())
    t=int("%.0f"%time.time())

    serial_temp = d.shell(["cat", "sys/class/thermal/thermal_zone*/temp"])
    serial_mode = d.shell(["cat", "sys/class/thermal/thermal_zone*/mode"])
    # dumpsys = d.shell("dumpsys telephony.registry | grep -i CellSignalStrength")

    p=sp.Popen("adb -s "+device+" shell dumpsys telephony.registry | grep -i CellSignalStrength",shell=True,stdout=sp.PIPE)    
    out,err=p.communicate()
    # # print (out,err)
    param=out.decode("utf-8").split('\n')
    # print(param)
    ss_param = param[0].split(',')  #  mSignalStrength=SignalStrength: ....
    ci_param = param[1]  #    mCellInfo=[CellInfoLte:{mRegistered=YES ....
    # print(ss_param[4])
    # print(ss_param[5])
    if ss_param[4].find("Lte")>=0:
        # Serving service is LTE
        # print(ss_param[4])
        # mLte=CellSignalStrengthLte: rssi=-51 rsrp=-56 rsrq=-9 rssnr=300 cqi=2147483647 ta=2147483647 level=4

        cell_service = 'LTE'
        signal = ss_param[4].split()
        rssi=int(signal[1].split("=")[1])
        rsrp=int(signal[2].split("=")[1])
        rsrq=int(signal[3].split("=")[1])
        rssnr=int(signal[4].split("=")[1])
        cqi=int(signal[5].split("=")[1])
        ta=int(signal[6].split("=")[1])
        level=int(signal[7].split("=")[1])

        registered_ci_param=ci_param.split(',')[0]
        # print(registered_ci_param)
        try:
            registered_ci_param_1=ci_param.split(',')[1]
            registered_ci_param_1_new = registered_ci_param_1.split()
        except:
            # print('lte')
            registered_ci_param_1 = 0
        registered_ci_param_new = registered_ci_param.split()

        # print(registered_ci_param_new)
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
        
        wstr="Service: "+cell_service+" Time: "+str(float(curtime-starttime))+" RSSI: "+str(rssi)+" RSRP: "+str(rsrp)+" RSRQ: "+str(rsrq)+" SNR: "+str(rssnr)+" CQI: "+str(cqi)+" PCI: "+str(pci)+" TAC: "+str(ta)+" EARFCN: "+str(earfcn)+" Bandwidth: "+str(bandwidth)+" mcc: "+str(mcc)+" mnc: "+str(mnc)+"\n"

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
        except:
            rsrp=signal[12]
            cell_service = '5G'
        wstr="Service: "+cell_service+" Time: "+str(float(curtime-starttime))+" RSSI: "+str(rssi)+" RSRP: "+str(rsrp)+" RSRQ: "+str(rsrq)+" SNR: "+str(rssnr)+" CQI: "+str(cqi)+" PCI: "+str(pci)+" TAC: "+str(ta)+" EARFCN: "+str(earfcn)+" Bandwidth: "+str(bandwidth)+" mcc: "+str(mcc)+" mnc: "+str(mnc)+"\n"
    fd.write(wstr)
    print(cell_service+' rsrp:'+str(rsrp))
    # d.shell("sleep interval", timeout=interval)
    s_temp = serial_temp.split('\n')
    s_temp.insert(0, str(t))
    tmp = np.empty([len(s_temp),1])
    tmp = np.array([s_temp])
    # print(a.shape)
    # a = np.vstack(a, [[tmp]], axis=0)
    a = np.concatenate((a,tmp), axis=0)
    # print(a.shape)    
    
    if(curtime-starttime>duration):
        break

    time.sleep(interval)
a_del = np.delete(a, 0, 0)

fd.close()
with open(filename[:-4]+'_temp.txt', 'w') as f_2:
    for row in a_del:
        for el in row:
            if str(el).find('cat') >= 0 or str(el) == '-273000' or str(el) == '-274000' or str(el) == '-40000':
                f_2.write('0'+'\t')
            else:
                f_2.write(str(el)+'\t')
        f_2.write('\n')
