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
print("plot.py started")

# TODO: make a configure file
duration = int(sys.argv[1])    # str(duration)
ClientState = sys.argv[2]    # ClientState
ClientStreams = int(sys.argv[3])
exp_count = int(sys.argv[4])
proto= sys.argv[5]
resultData = [] # [port, delay, throughput]*

y = glob.glob(data_dir+'/'+'*.txt') # after checking, enable this
print(interval)
server_and_client_list = []
cellinfo_file_list = []
temperature_file_list = []
cellfile = ''
temperature_file= ''
for j in y:
    if j.find("CellInfoClient")>=0 and j.find("_temp.txt") < 0: # add tempurture
        cellinfo_file_list.append(j)
for g in y:
    if g.find("CellInfoClient")>=0 and g.find("_temp.txt")>=0: # add tempurture
        temperature_file_list.append(g)
for p in y:
    if p.find("pServer")>=0 or p.find("pClient")>=0:
        server_and_client_list.append(p)

print(cellinfo_file_list)
print(temperature_file_list)
print(server_and_client_list)

# for Steam in range(ClientStreams):
# read from the txt file one by one
for i in server_and_client_list:
    print("filename is", i)
    # filename = i[33:-4] # ../../../plot_git_5g/bbr/data/
    filename = i[len_dir:-4] # ../../data/

    temp_x = filename.split('_')
    # # Structure
    print(temp_x)
  

    if i.find("pServer")>=0:
        # filename="Server_"+HOST+"_"+str(PORT)+"_"+addr[0]+"_"+str(addr[1])+"_download_"+str(proto)+"_"+str(x)+"_"+str(exp_count)+".txt"
        # write_file="pClient_"+HOST+"_"+str(PORT)+"_"+addr[0]+"_"+str(addr[1])+"_"+direction+"_"+proto+"_"+str(x)+"_"+str(exp_count)+".txt"
        # server_order=server_order+1
        Service = 'Server' #'Server' or 'Client'
        sIP = temp_x[1]
        sPort = temp_x[2]
        cIP = temp_x[3]
        cPort = temp_x[4] 
        direction = temp_x[5] # 'download' or 'upload'
        ClientState = temp_x[7]
        ClientStreams = temp_x[6]
        startTime = temp_x[8] # str(x)
        exp_num = temp_x[9]
        filename=result_dir+'/'+filename+"_server_"+str(exp_num)
        # 128.105.145.245_9001_download_1592423414_0
        # server_file_list.append(filename)

    elif i.find("pClient")>=0:
        # client_order=client_order+1
        Service = 'Client' #'Server' or 'Client'
        sIP = temp_x[1]
        sPort = temp_x[2]
        cIP = temp_x[3]
        cPort = temp_x[4]
        direction = temp_x[5] # 'download' or 'upload'
        ClientState = temp_x[7]
        ClientStreams = temp_x[6]
        startTime = temp_x[8] # str(x)
        exp_num = temp_x[9]
        filename=result_dir+'/'+filename+"_client_"+str(exp_num)

    elif i.find("CellInfoClient")>=0:
        # TODO
        print("skip")
        continue
    print("keep going")
    print('exp_num is '+str(exp_num))

    
    print(cellinfo_file_list)
    if cellinfo_file_list[0].find('_'+str(exp_num)+'.txt')>=0:
        cellfile = cellinfo_file_list[0]
        print("h is "+str(0))
        print("cellfile is "+cellfile)
        temperature_file = temperature_file_list[0]
        print(temperature_file)
            # continue
    # print("cellfile is "+cellfile)
    # ClientState="cubic"
    #TODO
    # if i.find("cubic")>=0:
    #     proto="cubic"
    # elif i.find("reno")>=0:
    #     proto="reno"
    # elif i.find("ulsan") or i.find("Ulsan")>=0:
    #     proto="ulsan"
    f = open('tmpDataFile', 'w')
    f_t = open('tmpDataFile_for_tempurature', 'w')
    with open(i, 'r') as fout:
        lines = fout.read().splitlines()
        print('fout here')
    fout.close()

    # cellfile="CellInfoClient_"+ClientIP+'_'+ClientPORT+'_'+HOST+"_"+str(PORT)+"_"+direction+'_'+str(x)+'_'+str(exp_id)+".txt"
    with open(cellfile, 'r') as fout_2:
        cellinfo_lines = fout_2.read().splitlines()
    fout_2.close()

    with open(temperature_file, 'r') as fout_3:
        temperature_lines = fout_3.read().splitlines()
    fout_3.close()
    
    print(len(lines))
    print(len(cellinfo_lines))
    print(len(temperature_lines))
    # remove this

    t=0
    mss = 0
    cwnd = 0
    KB_cwnd = 0
    check = 0

    for line in lines:
        s = line.split()
        mss = int(s[2])
        cwnd = int(s[6])
        # Size_cwnd = cwnd 
        Size_cwnd = (cwnd * mss)/1024
        rtt = int(s[11])/1000
        rtt_var = int(s[13])/1000
        
        # format: 1time, 2mss, 3cwnd, 4(cwnd * mss)/1024, 5s ssth, 6r ssth, 7rtt, 8rtt_var, 9unacked, 10throghtput, //// remove 11 cell seevice, 12rsrp, 13pci
        f.write(str(t)+"\t"+s[2]+"\t"+s[6]+"\t"+str(Size_cwnd)+"\t"+s[8]+"\t"+s[9]+"\t"+str(rtt)+"\t"+str(rtt_var)+"\t"+s[15]+"\t"+s[22]+"\n" )
        t = t+interval # every interval ms

        # check = check + 1
        # TODO
        # change s[0] to time
        # f.write( s[0]+"\t"+s[5]+"\t"+s[7]+"\t"+s[8]+"\t"+s[10]+"\t"+s[12]+"\t"+s[14]+"\n" )
    f.close()
    check = 0
    t=0
    for cell_line in cellinfo_lines:
        
        tmpCellinfo = cell_line.split(' ')
        t = tmpCellinfo[3]
        try:
            cell_service = tmpCellinfo[1]
            if cell_service == 'LTE':
                cell_service_num = 0
            elif cell_service == '5G':
                cell_service_num = 1
            rsrp = tmpCellinfo[7]
            pci = tmpCellinfo[15]
        except:
            cell_service_num = -1
            rsrp = 0
            pci = 0

        # TODO : need to add to graph temperature
        tmpTemperature_info = temperature_lines[check].split('\t')
        # print(tmpTemperature_info)
        t_Temperature = tmpTemperature_info[0]
        t_1 = tmpTemperature_info[77]
        t_2 = tmpTemperature_info[39]
        t_3= tmpTemperature_info[40]
        t_4 = tmpTemperature_info[41]
        t_5 = tmpTemperature_info[42]
        t_6 = tmpTemperature_info[23]
        t_7 = tmpTemperature_info[25]
        t_8 = tmpTemperature_info[37]
        t_9 = tmpTemperature_info[38]
        t_10 = tmpTemperature_info[47]
        t_11 = tmpTemperature_info[48]
        print(str(t)+"\t"+str(t_1)+"\t"+str(t_2)+"\t"+str(t_3)+"\t"+str(t_4)+"\t"+str(t_5)+"\t"+str(t_6)+"\t"+str(t_7)+"\t"+str(t_8)+"\t"+str(t_9)+"\t"+str(t_10)+"\t"+str(t_11)+"\t"+str(t)+"\t"+str(cell_service_num)+"\t"+str(rsrp)+"\t"+str(pci)+"\n" )
        
        f_t.write(str(t)+"\t"+str(t_1)+"\t"+str(t_2)+"\t"+str(t_3)+"\t"+str(t_4)+"\t"+str(t_5)+"\t"+str(t_6)+"\t"+str(t_7)+"\t"+str(t_8)+"\t"+str(t_9)+"\t"+str(t_10)+"\t"+str(t_11)+"\t"+str(t)+"\t"+str(cell_service_num)+"\t"+str(rsrp)+"\t"+str(pci)+"\n" )
        check = check + 1
    f_t.close()
    
    file_to_numpy = np.loadtxt('tmpDataFile', delimiter='\t')
    # print(file_to_numpy)
    tput = file_to_numpy[:,9]
    rtt = file_to_numpy[:,6]
    tmp_tput_mean = np.mean(tput, axis=0)
    tmp_rtt_mean = np.mean(rtt, axis=0)

    tput_mean = int(tmp_tput_mean)
    rtt_mean = int(tmp_rtt_mean)
    tput_mean = round(tput_mean, 2)
    rtt_mean = round(rtt_mean, 2)
    # rtt_mean = rtt_mean/1000
    # plot througput and cwnd
    f2 = open('tmpPltFile', 'w')
    f2.write( "reset;\n" )
    f2.write( "set terminal unknown;\n" )
    f2.write( "plot 'tmpDataFile' using 1:2;\n" ) 
    f2.write( "set terminal gif font 'Arial' 12;\n" )
    f2.write( "set output '"+filename+"_"+ClientState+"_cwnd.png';\n" )
    f2.write( "set term png size 1000, 400;\n" )
    f2.write( "set title '"+ClientState+"' font 'Arial-Bold, 19';\n" )
    f2.write( "set key top horizontal left;\n" )
    f2.write( "set xlabel 'Time (Seconds)';\n" )
    f2.write( "set ylabel 'Throghtput (Mbps)';\n" )
    f2.write( "set y2label 'Congestion window';\n" )
    f2.write( "set ytics nomirror;\n" )
    f2.write( "set ytics textcolor rgb 'red';\n" )
    f2.write( "set y2tics nomirror;\n" )
    f2.write( "set y2tics textcolor rgb 'blue';\n" )
    f2.write( "set xrange [0:"+str(duration)+"];\n" )
    f2.write( "set y2range [0:];\n" )
    f2.write( "set yrange [0:];\n" )
    f2.write( "set boxwidth 0.9;\n" )
    f2.write( "set xtics scale 1 nomirror offset 1.5;\n" )
    f2.write( "set style line 1 lt 1 lw 0.5;\n" )
    f2.write( "set style fill solid border -1\n" )
    f2.write( "set style line 1 lt 1 pt 1 ps 1 lc rgb 'red' lw 1\n" )
    f2.write( "set style line 2 lt 1 pt 2 ps 1 lc rgb 'blue' lw 1\n" )
    f2.write( "set style line 3 lt 1 pt 3 ps 1 lc rgb 'forest-green' lw 1\n" )
    f2.write( "set style line 4 lt 1 pt 4 ps 1 lc rgb 'orange' lw 1\n" )
    f2.write( "set style line 5 lt 1 pt 4 ps 1 lc rgb 'violet' lw 1\n" )
    # format: 1time, 2mss, 3cwnd, 4(cwnd * mss)/1024, 5s ssth, 6r ssth, 7rtt, 8rtt_var, 9unacked, 10throghtput, 11cell_service, 12rsrp, 13pci
    f2.write( "plot 'tmpDataFile' using 1:10 ls 1 title 'Throughput (mean:"+str(tput_mean)+")' with linespoints,\\\n " )
    f2.write( " 'tmpDataFile' using 1:3 ls 2 title 'CWND (y2)' axes x1y2 with linespoints,\n " )
    # for i in range(ClientStreams-1):
    #     f2.write( " 'tmpDataFile' using 1:($3=="+str(i+2)+"?$2:NaN) ls "+str(i+2)+" title 'Flow "+str(i+1)+"' with linespoints")
    #     if i<ClientStreams-2:
    #         f2.write( ",\\\n " )
    # f2.write( " 'tmpDataFile' using 1:4 ls 3 title 'RTT' axes x1y2 with linespoints,\n " )
    
    cmd = "gnuplot tmpPltFile\n cp tmpDataFile probedata"
    f2.close()
    cmd_run(cmd)

    # draw rtt plot
    f3 = open('tmpPltFile', 'w')
    f3.write( "reset;\n" ) 
    f3.write( "set terminal unknown;\n" )
    f3.write( "plot 'tmpDataFile' using 1:2;\n" ) 
    f3.write( "set terminal gif font 'Arial' 12;\n" )
    f3.write( "set output '"+filename+"_"+ClientState+"_rtt.png';\n" )
    f3.write( "set term png size 1000, 400;\n" )
    f3.write( "set title '"+ClientState+"' font 'Arial-Bold, 19';\n" )
    f3.write( "set key top horizontal left;\n" )
    f3.write( "set xlabel 'Time (Seconds)';\n" )
    f3.write( "set ylabel 'RTT (ms)';\n" )
    f3.write( "set ytics nomirror;\n" )
    # f3.write( "set y2tics nomirror;\n" )
    # f3.write( "set xrange [0:20];\n" )
    f3.write( "set xrange [0:"+str(duration)+"];\n" )
    f3.write( "set yrange [0:];\n" )
    f3.write( "set boxwidth 0.9;\n" )
    f3.write( "set xtics scale 1 nomirror offset 1.5;\n" )
    f3.write( "set style line 1 lt 1 lw 0.5;\n" )
    f3.write( "set style fill solid border -1\n" )
    f3.write( "set style line 1 lt 1 pt 1 ps 1 lc rgb 'red' lw 1\n" )
    f3.write( "set style line 2 lt 1 pt 2 ps 1 lc rgb 'blue' lw 1\n" )
    f3.write( "set style line 3 lt 1 pt 3 ps 1 lc rgb 'forest-green' lw 1\n" )
    f3.write( "set style line 4 lt 1 pt 4 ps 1 lc rgb 'orange' lw 1\n" )
    f3.write( "set style line 5 lt 1 pt 4 ps 1 lc rgb 'violet' lw 1\n" )
    f3.write( "func(x)=x/1024\n" )
    f3.write( "func2(x)=x*4\n" )
    f3.write( "func4(x)=x/1000\n" )
    
    f3.write( "plot  'tmpDataFile' using 1:7 ls 2 title 'Smoothed RTT (mean:"+str(rtt_mean)+")' with linespoints,\\\n " )
    f3.write( " 'tmpDataFile' using 1:8 ls 3 title 'RTT var' with linespoints\n " )

    cmd = "gnuplot tmpPltFile\n cp tmpDataFile probedata"
    f.close()
    f3.close()
    cmd_run(cmd)

    # draw cwnd * mss plot
    f4 = open('tmpPltFile', 'w')
    f4.write( "reset;\n" )
    f4.write( "set terminal unknown;\n" )
    f4.write( "plot 'tmpDataFile' using 1:2;\n" ) 
    f4.write( "set terminal gif font 'Arial' 12;\n" )
    f4.write( "set output '"+filename+"_"+ClientState+"_ssth.png';\n" )
    f4.write( "set term png size 1000, 400;\n" )
    f4.write( "set title '"+ClientState+"' font 'Arial-Bold, 19';\n" )
    f4.write( "set key top horizontal left;\n" )
    f4.write( "set xlabel 'Time (Seconds)';\n" )
    f4.write( "set ylabel 'Congestion window';\n" )
    f4.write( "set ytics textcolor rgb 'blue';\n" )
    f4.write( "set y2label 'Sender ssthreshold';\n" )
    f4.write( "set y2tics textcolor rgb 'violet';\n" )
    # f4.write( "set ylabel 'ssthreshold';\n" )
    # f4.write( "set y2label 'Window size';\n" )
    # f4.write( "set logscale y2;\n" )
    # f4.write( "set y2range [0:6000];\n" )
    f4.write( "set y2tics nomirror;\n" )
    # f4.write( "set xrange [0:20];\n" )
    f4.write( "set xrange [0:"+str(duration)+"];\n" )
    # if proto=="ulsan":
    #     f4.write( "set yrange [0:250];\n" )
    # elif proto=="reno":
    #     f4.write( "set yrange [0:1000];\n" )
    # else:    
    #     f4.write( "set yrange [0:];\n" )
    f4.write( "set y2range [0:];\n" )
    f4.write( "set yrange [0:];\n" )
    f4.write( "set boxwidth 0.9;\n" )
    f4.write( "set xtics scale 1 nomirror offset 1.5;\n" )
    f4.write( "set style line 1 lt 1 lw 0.5;\n" )
    f4.write( "set style fill solid border -1\n" )
    f4.write( "set style line 1 lt 1 pt 1 ps 1 lc rgb 'red' lw 1\n" )
    f4.write( "set style line 2 lt 1 pt 2 ps 1 lc rgb 'blue' lw 1\n" )
    f4.write( "set style line 3 lt 1 pt 3 ps 1 lc rgb 'forest-green' lw 1\n" )
    f4.write( "set style line 4 lt 1 pt 1 ps 1 lc rgb 'orange' lw 1\n" )
    f4.write( "set style line 5 lt 1 pt 4 ps 1 lc rgb 'violet' lw 1\n" )
    f4.write( "func(x)=x/1024\n" )
    f4.write( "func2(x)=x*4\n" )
    f4.write( "func4(x)=x/1000\n" )
    # f4.write( "plot 'tmpDataFile' using 1:4 ls 2 title 'CWND' with linespoints,\\\n " )
    f4.write( "plot 'tmpDataFile' using 1:3 ls 2 title 'CWND'  with linespoints,\\\n " )
    # f4.write( " 'tmpDataFile' using 1:4 ls 3 title '(cwnd * mss)/1024' with linespoints,\\\n " )
    f4.write( " 'tmpDataFile' using 1:5 ls 4 title 'Sender ssthreshold' with linespoints,\\\n " )
    f4.write( " 'tmpDataFile' using 1:5 ls 5 title 'Sender ssthreshold (y2)' axes x1y2 with linespoints,\n " )
    # f4.write( " 'tmpDataFile' using 1:6 ls 5 title 'Receiver ssthreshold' axes x1y2 with linespoints,\n " )

    cmd = "gnuplot tmpPltFile\n cp tmpDataFile probedata"
    f.close()
    f4.close()
    cmd_run(cmd)

    # draw througput & rsrp plot
    f5 = open('tmpPltFile', 'w')
    f5.write( "reset;\n" )
    f5.write( "set terminal unknown;\n" )
    f5.write( "plot 'tmpDataFile' using 1:2;\n" ) 
    f5.write( "set terminal gif font 'Arial' 12;\n" )
    f5.write( "set output '"+filename+"_"+ClientState+"_rsrp.png';\n" )
    f5.write( "set term png size 1000, 400;\n" )
    f5.write( "set title '"+ClientState+"' font 'Arial-Bold, 19';\n" )
    f5.write( "set key top horizontal left;\n" )
    f5.write( "set xlabel 'Time (Seconds)';\n" )
    f5.write( "set ylabel 'Throghtput (Mbps)';\n" )
    f5.write( "set y2label 'RSRP (dBM)';\n" )
    f5.write( "set ytics nomirror;\n" )
    f5.write( "set ytics textcolor rgb 'red';\n" )
    f5.write( "set y2tics nomirror;\n" )
    f5.write( "set xrange [0:"+str(duration)+"];\n" )
    f5.write( "set y2range [-125:-50];\n" )
    f5.write( "set y2tics textcolor rgb 'forest-green';\n" )
    # f5.write( "set yrange [0:300];\n" )
    f5.write( "set boxwidth 0.9;\n" )
    f5.write( "set xtics scale 1 nomirror offset 1.5;\n" )
    f5.write( "set style line 1 lt 1 lw 0.5;\n" )
    f5.write( "set style fill solid border -1\n" )
    f5.write( "set style line 1 lt 1 pt 1 ps 1 lc rgb 'red' lw 1\n" )
    f5.write( "set style line 2 lt 1 pt 2 ps 1 lc rgb 'blue' lw 1\n" )
    f5.write( "set style line 3 lt 1 pt 3 ps 1 lc rgb 'forest-green' lw 1\n" )
    f5.write( "set style line 4 lt 1 pt 4 ps 1 lc rgb 'orange' lw 1\n" )
    f5.write( "set style line 5 lt 1 pt 5 ps 1 lc rgb 'violet' lw 1\n" )
    f5.write( "func(x)=x/1024\n" )
    f5.write( "func2(x)=x*4\n" )
    f5.write( "func4(x)=x/1000\n" )
    f5.write( "plot 'tmpDataFile' using 1:10 ls 1 title 'Throughput (mean:"+str(tput_mean)+")' with linespoints,\\\n " )
    # f5.write( " 'tmpDataFile' using 1:11 ls 5 title 'Service[LTE(0), 5G(1)]' axes x1y2 with linespoints,\\\n " )
    f5.write( "    'tmpDataFile_for_tempurature' using 1:15 ls 3 title 'RSRP' axes x1y2 with linespoints,\n " )
# print(str(t)+"\t"+str(t_1)+"\t"+str(t_2)+"\t"+str(t_3)+"\t"+str(t_4)+"\t"+str(t_5)+"\t"+str(t_6)+"\t"+str(t_7)+"\t"+str(t_8)+
# "\t"+str(t_9)+"\t"+str(t_10)+"\t"+str(t_11)+"\t"+str(t)+"\t"+str(cell_service_num)+"\t"+str(rsrp)+"\t"+str(pci)+"\n" )
        
    cmd = "gnuplot tmpPltFile\n cp tmpDataFile probedata"
    f.close()
    f5.close()
    cmd_run(cmd)

    # draw througput & rsrp plot
    f6 = open('tmpPltFile', 'w')
    f6.write( "reset;\n" )
    f6.write( "set terminal unknown;\n" )
    f6.write( "plot 'tmpDataFile' using 1:2;\n" ) 
    f6.write( "set terminal gif font 'Arial' 12;\n" )
    f6.write( "set output '"+filename+"_"+ClientState+"_service.png';\n" )
    f6.write( "set term png size 1000, 400;\n" )
    f6.write( "set multiplot layout 2, 1 title '"+ClientState+"' font 'Arial-Bold, 19';\n" )
    f6.write( "set key top horizontal left;\n" )
    f6.write( "set xlabel 'Time (Seconds)';\n" )
    f6.write( "set ylabel 'Throghtput (Mbps)';\n" )
    f6.write( "set y2label 'Service[LTE(0), 5G(1)]';\n" )
    f6.write( "set ytics nomirror;\n" )
    f6.write( "set ytics textcolor rgb 'red';\n" )
    f6.write( "set y2tics nomirror;\n" )
    f6.write( "set xrange [0:"+str(duration)+"];\n" )
    # f6.write( "set y2range [-1:2];\n" )
    f6.write( "set y2tics textcolor rgb 'violet';\n" )
    # f6.write( "set yrange [0:300];\n" )
    f6.write( "set boxwidth 0.9;\n" )
    f6.write( "set xtics scale 1 nomirror offset 1.5;\n" )
    f6.write( "set style line 1 lt 1 lw 0.5;\n" )
    f6.write( "set style fill solid border -1\n" )
    f6.write( "set style line 1 lt 1 pt 1 ps 1 lc rgb 'red' lw 1\n" )
    f6.write( "set style line 2 lt 1 pt 2 ps 1 lc rgb 'blue' lw 1\n" )
    f6.write( "set style line 3 lt 1 pt 3 ps 1 lc rgb 'forest-green' lw 1\n" )
    f6.write( "set style line 4 lt 1 pt 4 ps 1 lc rgb 'orange' lw 1\n" )
    f6.write( "set style line 5 lt 1 pt 5 ps 1 lc rgb 'violet' lw 1\n" )
    f6.write( "func(x)=x/1024\n" )
    f6.write( "func2(x)=x*4\n" )
    f6.write( "func4(x)=x/1000\n" )
    f6.write( "plot 'tmpDataFile' using 1:10 ls 1 title 'Throughput (mean:"+str(tput_mean)+")' with line,\\\n " )
    f6.write( "    'tmpDataFile_for_tempurature' using 1:14 ls 5 title 'Service[LTE(0), 5G(1)]' axes x1y2 with line,\n " )
    f6.write( "set ylabel 'Throghtput (Mbps)';\n" )
    f6.write( "set y2label 'CellID';\n" )
    f6.write( "set ytics nomirror;\n" )
    f6.write( "set ytics textcolor rgb 'red';\n" )
    f6.write( "set y2tics nomirror;\n" )
    f6.write( "set y2tics textcolor rgb 'blue';\n" )
    f6.write( "plot 'tmpDataFile' using 1:10 ls 1 title 'Throughput (mean:"+str(tput_mean)+")' with line,\\\n " )
    f6.write( "    'tmpDataFile_for_tempurature' using 1:16 ls 5 title 'CellID' axes x1y2 with linespoints,\n " )
    # f6.write( " 'tmpDataFile' using 1:12 ls 3 title 'RSRP' axes x1y2 with linespoints,\n " )

    cmd = "gnuplot tmpPltFile\n cp tmpDataFile probedata"
    f.close()
    f6.close()
    cmd_run(cmd)

    # plot througput and cwnd
    f7 = open('tmpPltFile', 'w')
    f7.write( "reset;\n" )
    f7.write( "set terminal unknown;\n" )
    f7.write( "plot 'tmpDataFile' using 1:2;\n" ) 
    f7.write( "set terminal gif font 'Arial' 12;\n" )
    f7.write( "set output '"+filename+"_"+ClientState+"_total.png';\n" )
    f7.write( "set term png size 1000, 600;\n" )
    f7.write( "set multiplot layout 2, 1 title '"+ClientState+"' font 'Arial-Bold, 19';\n" )
    f7.write( "set key top horizontal left;\n" )
    f7.write( "set xlabel 'Time (Seconds)';\n" )
    f7.write( "set tmargin 0.5;\n" )
    f7.write( "set style line 1 lt 1 pt 1 ps 1 lc rgb 'red' lw 1\n" )
    f7.write( "set style line 2 lt 1 pt 2 ps 1 lc rgb 'blue' lw 1\n" )
    f7.write( "set style line 3 lt 1 pt 3 ps 1 lc rgb 'forest-green' lw 1\n" )
    f7.write( "set style line 4 lt 1 pt 4 ps 1 lc rgb 'orange' lw 1\n" )
    f7.write( "set style line 5 lt 1 pt 4 ps 1 lc rgb 'violet' lw 1\n" )

    # f7.write( "set title 'Throughput & Cwnd';\n" )
    f7.write( "set ylabel 'Throghtput (Mbps)';\n" )
    f7.write( "set y2label 'Congestion window';\n" )
    f7.write( "set ytics nomirror;\n" )
    f7.write( "set ytics textcolor rgb 'red';\n" )
    f7.write( "set y2tics nomirror;\n" )
    f7.write( "set y2tics textcolor rgb 'blue';\n" )
    # f7.write( "unset key;\n" )
    f7.write( "plot 'tmpDataFile' using 1:10 ls 1 title 'Throughput (mean:"+str(tput_mean)+")' with line,\\\n " )
    f7.write( "  'tmpDataFile' using 1:3 ls 2 title 'CWND (y2)' axes x1y2 with line,\n " )
    # f7.write( "set title 'RTT';\n" )
    f7.write( "set ylabel 'RTT (ms)';\n" )
    f7.write( "set ytics textcolor rgb 'forest-green';\n" )
    f7.write( "set y2label '';\n" )
    f7.write( "set ytics textcolor rgb 'black';\n" )
    # f7.write( "unset key;\n" )
    # f7.write( "plot 'tmpDataFile' using 1:10 ls 1 title 'Throughput' with line,\\\n " )
    f7.write( "plot  'tmpDataFile' using 1:7 ls 3 title 'Smoothed RTT (mean:"+str(rtt_mean)+")' with line,\n " )

    cmd = "gnuplot tmpPltFile\n cp tmpDataFile probedata"
    f.close()
    f7.close()
    cmd_run(cmd)

    # index for iperf3 - Sandesh version
    # idx 1: mss (title) -> time
    # idx 2: tcpi_snd_mss
    # idx 3: tcpi_last_data_sent
    # idx 4: tcpi_last_data_recv
    # idx 5: cwnd (title)
    # idx 6: tcpi_snd_cwnd
    # idx 7: ssthresh (title)
    # idx 8: tcpi_snd_ssthresh
    # idx 9: tcpi_rcv_ssthresh
    # idx 10: rtt (title)
    # idx 11: tcpi_rtt
    # idx 12: rttv (title)
    # idx 13: tcpi_rttvar
    # idx 14: unacked (title)
    # idx 15: tcpi_unacked
    # idx 16: tcpi_sacked
    # idx 17: tcpi_lost
    # idx 18: tcpi_retrans
    # idx 19: tcpi_fackets
    # idx 20: totalretx (title)
    # idx 21: tcpi_total_retrans           

    # tmpDataFile_for_tempurature

        # plot througput and cwnd3
    f8 = open('tmpPltFile', 'w')
    f8.write( "reset;\n" )
    f8.write( "set terminal unknown;\n" )
    f8.write( "plot 'tmpDataFile_for_tempurature' using 1:10;\n" ) 
    f8.write( "plot 'tmpDataFile' using 1:2;\n" ) 
    f8.write( "set terminal gif font 'Arial' 12;\n" )
    f8.write( "set output '"+filename+"_"+ClientState+"_temperature.png';\n" )
    f8.write( "set term png size 1000, 600;\n" )
    f8.write( "set multiplot layout 2, 1 title '"+ClientState+"' font 'Arial-Bold, 19';\n" )
    f8.write( "set key top horizontal left;\n" )
    f8.write( "set xlabel 'Time (Seconds)';\n" )
    f8.write( "set tmargin 0.5;\n" )
    f8.write( "set style line 1 lt 1 pt 1 ps 1 lc rgb 'red' lw 1\n" )
    f8.write( "set style line 2 lt 1 pt 2 ps 1 lc rgb 'blue' lw 1\n" )
    f8.write( "set style line 3 lt 1 pt 3 ps 1 lc rgb 'forest-green' lw 1\n" )
    f8.write( "set style line 4 lt 1 pt 4 ps 1 lc rgb 'orange' lw 1\n" )
    f8.write( "set style line 5 lt 1 pt 4 ps 1 lc rgb 'violet' lw 1\n" )
    f8.write( "set ylabel 'Throghtput (Mbps)';\n" ) 
    f8.write( "set y2label 'Temp (C)';\n" )
    f8.write( "set ytics nomirror;\n" )
    f8.write( "set ytics textcolor rgb 'red';\n" )
    f8.write( "set y2tics nomirror;\n" )
    f8.write( "set y2tics textcolor rgb 'blue';\n" )
    # f8.write( "unset key;\n" )
    f8.write( "plot 'tmpDataFile' using 1:10 ls 1 title 'Throughput (mean:"+str(tput_mean)+")' with line,\\\n " ) 
    f8.write( "  'tmpDataFile_for_tempurature' using 1:2 ls 1 title 'modem-mmw0-usr' axes x1y2 with line,\\\n " )
    f8.write( "  'tmpDataFile_for_tempurature' using 1:3 ls 2 title 'modem-mmw1-usr' axes x1y2 with line,\\\n " )
    f8.write( "  'tmpDataFile_for_tempurature' using 1:4 ls 3 title 'modem-mmw2-usr' axes x1y2 with line,\\\n" )
    f8.write( "  'tmpDataFile_for_tempurature' using 1:9 ls 4 title 'modem-lte-sub6-pa1' axes x1y2 with line,\\\n" )
    f8.write( "  'tmpDataFile_for_tempurature' using 1:10 ls 5 title 'modem-lte-sub6-pa2' axes x1y2 with line,\n" )
    f8.write( "set ylabel 'Temp (C)';\n" ) 
    f8.write( "set y2tics textcolor rgb 'blue';\n" )
    # f8.write( "unset key;\n" )
    f8.write( "plot 'tmpDataFile_for_tempurature' using 1:2 ls 1 title 'Battery' with line,\\\n " )
    f8.write( "  'tmpDataFile_for_tempurature' using 1:7 ls 2 title 'cpu-0-0-step' with line,\\\n " )
    f8.write( "  'tmpDataFile_for_tempurature' using 1:8 ls 3 title 'cpu-0-1-step' with line,\n" )
    # f8.write( "set ylabel 'Temp (C)';\n" ) 
    # f8.write( "set ytics textcolor rgb 'forest-green';\n" )
    # # f8.write( "set y2label '';\n" )
    # f8.write( "set ytics textcolor rgb 'black';\n" )
    # # f8.write( "unset key;\n" )
    # f8.write( "plot 'tmpDataFile_for_tempurature' using 1:2 ls 1 title 'Battery' with linespoints,\\\n " )
    # f8.write( "    'tmpDataFile_for_tempurature' using 1:7 rgb 'red' title 'cpu-0-0-step' with linespoints,\\\n " )
    # f8.write( "    'tmpDataFile_for_tempurature' using 1:8 rgb 'red' title 'cpu-0-1-step' with linespoints,\n" )
        # f7.write( "unset key;\n" )
#     f7.write( "plot 'tmpDataFile' using 1:10 ls 1 title 'Throughput (mean:"+str(tput_mean)+")' with linespoints,\\\n " )
#     f7.write( "  'tmpDataFile' using 1:3 ls 2 title 'CWND (y2)' axes x1y2 with linespoints,\n " )
# plot 'tmpDataFile_for_tempurature' using 1:2 rgb 'violet' title 'modem-mmw0-usr' with linespoints,     
# 'tmpDataFile_for_tempurature' using 1:3 rgb 'forest-green' title 'modem-mmw1-usr' with linespoints,     
# 'tmpDataFile_for_tempurature' using 1:4 rgb 'gray' title 'modem-mmw2-usr' with linespoints,
#     cmd = "gnuplot tmpPltFile\n cp tmpDataFile_for_tempurature probedata"
    f.close()
    f8.close()
    cmd_run(cmd)
#  time :1 
                # battery_t = tmpTemperature_info[77] 2
            # modem-mmw0-usr = tmpTemperature_info[39] 3
            # modem-mmw1-usr = tmpTemperature_info[40] 4
            # modem-mmw2-usr = tmpTemperature_info[41] 5
            # modem-mmw3-usr = tmpTemperature_info[42] 6
            # cpu-0-0-step = tmpTemperature_info[23] 7
            # cpu-0-1-step = tmpTemperature_info[25] 8
            # modem-lte-sub6-pa1 = tmpTemperature_info[37] 9
            # modem-lte-sub6-pa2 = tmpTemperature_info[38] 10
            # modem-0-usr = tmpTemperature_info[47] 11
            # modem-1-usr = tmpTemperature_info[48]12 

        #             t_1 = tmpTemperature_info[77]
        # t_2 = tmpTemperature_info[39]
        # t_3= tmpTemperature_info[40]
        # t_4 = tmpTemperature_info[41]
        # t_5 = tmpTemperature_info[42]
        # t_6 = tmpTemperature_info[23]
        # t_7 = tmpTemperature_info[25]
        # t_8 = tmpTemperature_info[37]
        # t_9 = tmpTemperature_info[38]
        # t_10 = tmpTemperature_info[47]
        # t_11 = tmpTemperature_info[48]