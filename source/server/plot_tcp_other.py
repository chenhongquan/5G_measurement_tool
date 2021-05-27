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
print("plot_tcp_other.py started")

# TODO: make a configure file
duration = int(sys.argv[1])	# str(duration)
ClientState = sys.argv[2]	# ClientState
ClientStreams = int(sys.argv[3])
exp_count = int(sys.argv[4])
proto= sys.argv[5]

probe_file_list = []

if proto == 'c2tcp':
    dir_list = os.listdir(data_dir)
    for dir in dir_list:
        y = glob.glob(data_dir+'/*.txt')
        print(y)
else:        
    y = glob.glob(data_dir+'/'+'*.txt') # after checking, enable this

for n in y:
    if n.find("tcpprobe_")>=0:
        probe_file_list.append(n)

for i in probe_file_list:
    print("filename is", i)
    if proto == 'c2tcp':
        temp_filesplit = i.split('/')
        len_file = len(temp_filesplit)
        len_filename = len(temp_filesplit[len_file-1])
        filename = temp_filesplit[len_file-1]
        filename_fig =i[:-len_filename]+filename
        print(filename_fig)
        ca_name = 'c2tcp'  
        rtt_file=filename[:-4]+'.log'
    else:
        filename = i[len_dir:-4] # ../../data/
        # filename_fig = result_dir+'/'+filename+"_tcpprbe_"+str(exp_num)
        rtt_file=filename+'.log'
    temp_x = filename.split('_')
    # # Structure
    # print(temp_x)



    if i.find("tcpprobe_")>=0:
        Service = 'TCP_PROBE'
        sIP = temp_x[1]
        sPort = temp_x[2]
        cIP = temp_x[3]
        cPort = temp_x[4] 
        direction = temp_x[5] # 'download' or 'upload'
        ClientState = temp_x[7]
        ClientStreams = temp_x[6]
        startTime = temp_x[8] # str(x)
        exp_num = temp_x[9]
        filename=result_dir+'/'+filename+"_tcpprbe_"+str(exp_num)
        if proto != 'c2tcp':
            filename_fig = result_dir+'/'+filename+"_tcpprbe_"+str(exp_num)


    f_rtt = open(data_dir+'/'+rtt_file, 'w')
    f = open('tmpDataFile', 'w')
    with open(i, 'r') as fout:
        lines = fout.read().splitlines()
        # print('fout here')
    fout.close()

    # remove this
    t=0
    mss = 0
    cwnd = 0
    KB_cwnd = 0
    check = 0

    if i.find("tcpprobe_")>=0 and i.find(".txt"):
        for line in lines[1:-1]:
            s = line.split()
            # print(s)
            if t == 0:
                init_t = float(s[0])
            t = float(s[0])
            rtt = int(s[9])/1000
            ca_name = s[26]
            f_rtt.write(str(t-init_t)+"\t"+str(rtt)+"\t"+str(s[6])+"\t"+str(s[8])+"\t"+str(s[10])+"\t"+str(s[23])+"\n") # time rtt cwnd snd_wnd rcv_wnd mss
            f.write(str(t)+"\t"+str(s[6])+"\t"+str(s[7])+"\t"+str(s[8])+"\t"+str(rtt)+"\t"+str(s[10])+"\t"+str(s[11])+"\t"+str(s[12])+"\t"+str(s[13])+"\t"+str(s[14])+"\t"+str(s[15])+"\t"+str(s[16])+"\t"+str(s[17])+"\t"+str(s[18])+"\t"+str(s[19])+"\t"+str(s[20])+"\t"+str(s[21])+"\t"+str(s[22])+"\t"+str(s[23])+"\t"+str(s[24])+"\t"+str(s[25])+"\n")
        f.close()
        f_rtt.close()

        file_to_numpy = np.loadtxt('tmpDataFile', delimiter='\t')
        # print(file_to_numpy)
        # tput = file_to_numpy[:,9]
        rtt = file_to_numpy[:,4]
        # tmp_tput_mean = np.mean(tput, axis=0)
        tmp_rtt_mean = np.mean(rtt, axis=0)

        # tput_mean = int(tmp_tput_mean)
        rtt_mean = int(tmp_rtt_mean)
        # tput_mean = round(tput_mean, 2)
        rtt_mean = round(rtt_mean, 2)

        # plot througput and cwnd
        f7 = open('tmpPltFile', 'w')
        f7.write( "reset;\n" )
        f7.write( "set terminal gif font 'Arial' 12;\n" )
        f7.write( "set output '"+filename+"_"+ClientState+"_total_tp1.png';\n" )
        f7.write( "set term png size 1000, 600;\n" )
        f7.write( "set multiplot layout 2, 1 title '"+str(ca_name)+"_"+str(exp_num)+"' font 'Arial-Bold, 19';\n" )
        f7.write( "set key top horizontal left;\n" )
        f7.write( "set xlabel 'Time (Seconds)';\n" )
        f7.write( "set tmargin 0.5;\n" )
        f7.write( "set style line 1 lt 1 pt 1 ps 1 lc rgb 'red' lw 1\n" )
        f7.write( "set style line 2 lt 1 pt 2 ps 1 lc rgb 'blue' lw 1\n" )
        f7.write( "set style line 3 lt 1 pt 3 ps 1 lc rgb 'forest-green' lw 1\n" )
        f7.write( "set style line 4 lt 1 pt 4 ps 1 lc rgb 'orange' lw 1\n" )
        f7.write( "set style line 5 lt 1 pt 4 ps 1 lc rgb 'violet' lw 1\n" )
        f7.write( "set ylabel 'CWND';\n" )
        f7.write( "set y2label 'ssth';\n" )
        f7.write( "set ytics nomirror;\n" )
        f7.write( "set ytics textcolor rgb 'blue';\n" )
        f7.write( "set y2tics nomirror;\n" )
        f7.write( "set y2tics textcolor rgb 'black';\n" )
        f7.write( "plot 'tmpDataFile' using 1:2 ls 2 title 'CWND' with line,\\\n " )
        f7.write( "  'tmpDataFile' using 1:3 ls 3 title 'ssth' axes x1y2 with line,\n " )
        f7.write( "set ylabel 'RTT mean:"+str(rtt_mean)+" (ms)';\n" )
        f7.write( "set ytics textcolor rgb 'forest-green';\n" )
        f7.write( "set y2label '"+str(proto)+"';\n" )
        f7.write( "set y2tics nomirror;\n" )
        f7.write( "set y2tics textcolor rgb 'blue';\n" )
        f7.write( "set ytics textcolor rgb 'black';\n" )
        f7.write( "plot  'tmpDataFile' using 1:5 ls 3 title 'rtt' with line,\n " )

        cmd = "gnuplot tmpPltFile\n cp tmpDataFile probedata"
        f.close()
        f7.close()
        cmd_run(cmd)

        f3 = open('tmpPltFile', 'w')
        f3.write( "reset;\n" )
        f3.write( "set terminal gif font 'Arial' 12;\n" )
        f3.write( "set output '"+filename+"_"+ClientState+"_total_tp2.png';\n" )
        f3.write( "set term png size 1000, 600;\n" )
        f3.write( "set multiplot layout 3, 1 title '"+str(ca_name)+"_"+str(exp_num)+"' font 'Arial-Bold, 19';\n" )
        f3.write( "set key top horizontal left;\n" )
        f3.write( "set xlabel 'Time (Seconds)';\n" )
        f3.write( "set tmargin 0.5;\n" )
        f3.write( "set style line 1 lt 1 pt 1 ps 1 lc rgb 'red' lw 1\n" )
        f3.write( "set style line 2 lt 1 pt 2 ps 1 lc rgb 'blue' lw 1\n" )
        f3.write( "set style line 3 lt 1 pt 3 ps 1 lc rgb 'forest-green' lw 1\n" )
        f3.write( "set style line 4 lt 1 pt 4 ps 1 lc rgb 'orange' lw 1\n" )
        f3.write( "set style line 5 lt 1 pt 4 ps 1 lc rgb 'violet' lw 1\n" )
        f3.write( "set ylabel 'Rwnd (Bytes)';\n" )
        f3.write( "set ytics nomirror;\n" )
        f3.write( "set ytics textcolor rgb 'red';\n" )
        f3.write( "plot 'tmpDataFile' using 1:4 ls 1 title 'snd wnd' with line,\\\n " )
        f3.write( "  'tmpDataFile' using 1:6 ls 2 title 'rcv wnd' with line,\n " )
        f3.write( "set ylabel 'bytes acked';\n" )
        f3.write( "set ytics textcolor rgb 'forest-green';\n" )
        f3.write( "set ytics nomirror;\n" )
        f3.write( "set y2label 'mss';\n" )
        f3.write( "set y2tics textcolor rgb 'black';\n" )
        f3.write( "set y2tics nomirror;\n" )
        f3.write( "plot  'tmpDataFile' using 1:18 ls 3 title 'bytes acked' with line,\\\n " )
        f3.write( "  'tmpDataFile' using 1:19 ls 2 title 'mss' with line,\n " )
        f3.write( "set ylabel 'Inflight Pkts';\n" )
        f3.write( "set ytics textcolor rgb 'forest-green';\n" ) 
        f3.write( "set ytics nomirror;\n" )
        f3.write( "set y2label 'Lost Pks';\n" )
        f3.write( "set y2tics textcolor rgb 'black';\n" )
        f3.write( "set y2tics nomirror;\n" )
        # f3.write( "set y2range [0:100];\n" )
        f3.write( "plot  'tmpDataFile' using 1:20 ls 3 title 'inflight pkts' with line,\\\n " )
        f3.write( "  'tmpDataFile' using 1:21 ls 1 lw 3 title 'lost pks' axes x1y2 with line,\n " )

        cmd = "gnuplot tmpPltFile\n cp tmpDataFile probedata"
        f.close()
        f3.close()
        cmd_run(cmd)
        # bbr additional figures
        if proto == 'bbr':
            f1 = open('tmpPltFile', 'w')
            f1.write( "reset;\n" )
            f1.write( "set terminal gif font 'Arial' 12;\n" )
            f1.write( "set output '"+filename+"_"+ClientState+"_bbr_1.png';\n" )
            f1.write( "set term png size 1000, 600;\n" )
            f1.write( "set multiplot layout 2, 1 title '"+str(ca_name)+"_"+str(exp_num)+"'  font 'Arial-Bold, 19';\n" )
            f1.write( "set key top horizontal left;\n" )
            f1.write( "set xlabel 'Time (Seconds)';\n" )
            f1.write( "set tmargin 0.5;\n" )
            f1.write( "set style line 1 lt 1 pt 1 ps 1 lc rgb 'red' lw 1\n" )
            f1.write( "set style line 2 lt 1 pt 2 ps 1 lc rgb 'blue' lw 1\n" )
            f1.write( "set style line 3 lt 1 pt 3 ps 1 lc rgb 'forest-green' lw 1\n" )
            f1.write( "set style line 4 lt 1 pt 4 ps 1 lc rgb 'orange' lw 1\n" )
            f1.write( "set style line 5 lt 1 pt 4 ps 1 lc rgb 'violet' lw 1\n" )
            f1.write( "set ylabel 'bbr pacing rate';\n" )
            f1.write( "set ytics nomirror;\n" )
            f1.write( "set ytics textcolor rgb 'red';\n" )
            f1.write( "plot 'tmpDataFile' using 1:15 ls 1 title 'bbr pacing gain' with line,\\\n " )
            f1.write( "  'tmpDataFile' using 1:16 ls 2 title 'bbr cwnd gain' with line,\n " )
            f1.write( "set ylabel 'bbr bw';\n" )
            f1.write( "set ytics textcolor rgb 'forest-green';\n" )
            f1.write( "set ytics textcolor rgb 'black';\n" )
            f1.write( "plot  'tmpDataFile' using 1:12 ls 3 title 'bbr lt use bw' with line,\\\n " )
            f1.write( "  'tmpDataFile' using 1:13 ls 4 title 'bbr lt bw' with line,\\\n " )
            f1.write( "  'tmpDataFile' using 1:17 ls 4 title 'bbr full bw' with line,\n " )

            cmd = "gnuplot tmpPltFile\n cp tmpDataFile probedata"
            f.close()
            f1.close()
            cmd_run(cmd)

            f2 = open('tmpPltFile', 'w')
            f2.write( "reset;\n" )
            f2.write( "set terminal gif font 'Arial' 12;\n" )
            f2.write( "set output '"+filename+"_"+ClientState+"_bbr_2.png';\n" )
            f2.write( "set term png size 1000, 600;\n" )
            f2.write( "set multiplot layout 3, 1 title '"+str(ca_name)+"_"+str(exp_num)+"' font 'Arial-Bold, 19';\n" )
            f2.write( "set key top horizontal left;\n" )
            f2.write( "set xlabel 'Time (Seconds)';\n" )
            f2.write( "set tmargin 0.5;\n" )
            f2.write( "set style line 1 lt 1 pt 1 ps 1 lc rgb 'red' lw 1\n" )
            f2.write( "set style line 2 lt 1 pt 2 ps 1 lc rgb 'blue' lw 1\n" )
            f2.write( "set style line 3 lt 1 pt 3 ps 1 lc rgb 'forest-green' lw 1\n" )
            f2.write( "set style line 4 lt 1 pt 4 ps 1 lc rgb 'orange' lw 1\n" )
            f2.write( "set style line 5 lt 1 pt 4 ps 1 lc rgb 'violet' lw 1\n" )
            f2.write( "set ylabel 'bbr min rtt us';\n" )
            f2.write( "set ytics nomirror;\n" )
            f2.write( "set ytics textcolor rgb 'red';\n" )
            f2.write( "plot 'tmpDataFile' using 1:10 ls 1 title 'bbr min rtt us' with line,\n " )
            f2.write( "set ylabel 'bbr mode';\n" )
            f2.write( "set ytics textcolor rgb 'forest-green';\n" )
            f2.write( "set ytics textcolor rgb 'black';\n" )
            f2.write( "plot  'tmpDataFile' using 1:11 ls 3 title 'bbr mode' with line,\n " )
            f2.write( "set ylabel 'bbr cycle idx';\n" )
            f2.write( "set ytics textcolor rgb 'forest-green';\n" )
            f2.write( "set ytics textcolor rgb 'black';\n" )
            f2.write( "plot  'tmpDataFile' using 1:14 ls 3 title 'bbr cycle idx' with line,\n " )

            cmd = "gnuplot tmpPltFile\n cp tmpDataFile probedata"
            f.close()
            f2.close()
            cmd_run(cmd)


# TODO: check number of colum and match for graph.
# 6 p->snd_cwnd, 7 p->ssthresh, 8 p->snd_wnd, 9 p->srtt, 10 p->rcv_wnd,
# 11 p->rcv_tsval,12 p->now,13 p->rcv_nxt, 
# 14 p->bbr_min_rtt_us,15 p->bbr_mode,16 p->bbr_lt_use_bw,17 p->bbr_lt_bw,
# 18 p->bbr_cycle_idx,19 p->bbr_pacing_gain,20 p->bbr_cwnd_gain,21 p->bbr_full_bw, 
# 22 p->bytes_acked, 23 p->mss, 24 p->snd_pair,25 p->snd_plost,26 p->ca_name);
        
# 2 p->snd_cwnd, 3 p->ssthresh, 4 p->snd_wnd, 5 p->srtt,  6 p->rcv_wnd, 7 p->rcv_tsval, 8 p->now, 9 p->rcv_nxt, 
# 10 p->bbr_min_rtt_us,11 p->bbr_mode,12 p->bbr_lt_use_bw,13 p->bbr_lt_bw,14 p->bbr_cycle_idx,
# 15 p->bbr_pacing_gain,16 p->bbr_cwnd_gain,17 p->bbr_full_bw, 18 p->bytes_acked, 19 p->mss, 20 p->snd_pair,
# 21 p->snd_plost,p->ca_name      
# str(t)+"\t"+str(s[6])+"\t"+str(s[7])+"\t"+str(s[8])+"\t"+str(int(s[9]/1000)+"\t"+str(s[10])+"\t"+str(s[11])+"\t"+str(s[12])+"\t"+str(s[13])+"\t"+str(s[14])+"\t"+str(s[15])+"\t"+str(s[16])+"\t"+str(s[17])+"\t"+str(s[18])+"\t"+str(s[19])+"\t"+str(s[20])+"\t"+str(s[21])+"\t"+str(s[22])+"\t"+str(s[23])+"\t"+str(s[24])+"\t"+str(s[25])+"\n")
        