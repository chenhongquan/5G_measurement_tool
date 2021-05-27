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
# interval = 1
# readfilename filename(wrt) CCA_name
# python3 new_plot_from_udp.py readfilename filename(wrt) CCA_name
if(len(sys.argv)<4):
	print ("Usage error: --tput_file --rtt_file --output_dir --cca_name")
	exit()

readfilename=sys.argv[1]
rtt_filename=sys.argv[2]
filename=sys.argv[3]
cca_name=sys.argv[4]
if cca_name == 'copa' and rtt_filename.find('.txt') >= 0:
    tput_log_file = readfilename[:-31]+'_tput.log'
    rtt_log_file = readfilename[:-31]+'_rtt.log'
elif cca_name == 'copa' and rtt_filename.find('.txt') < 0:
    tput_log_file = readfilename[:-26]+'_tput.log'
    rtt_log_file = readfilename[:-26]+'_rtt.log'
elif cca_name == 'verus':
    tput_log_file = readfilename[:-31]+'_tput.log'
    rtt_log_file = readfilename[:-31]+'_rtt.log'
else: # sprout
    tput_log_file = readfilename[:-4]+'_tput.log'
    rtt_log_file = readfilename[:-4]+'_rtt.log'

if cca_name == 'sprout':
    PORT = 60001

def get_sec(time_str):
    """Get Seconds from time."""
    # h, m, s = time_str.split(':')
    # return float(m) * 60 + float(s)
    h= time_str.split(':')[0]
    m= time_str.split(':')[1]
    s= time_str.split(':')[2].split('.')[0]
    microsecond= time_str.split(':')[2].split('.')[1]
    return (int(m)*60) + int(s) + (int(microsecond)/1000000)

def parse_filename(filename):
    path = filename
    head_tail = os.path.split(path) 
    return head_tail[0]

def parse_copa_rtt_file(rtt_filename):
    print('rtt')
    f_rtt = open(rtt_log_file, 'w')
    with open(rtt_filename, 'r') as fout:
        lines = fout.read().splitlines()
        print('fout here : parse_copa_rtt_file')
    fout.close()

    s_t = -1
    e_t = -1
    rtt, tmp_rtt, total_rtt = 0.0, 0.0, 0.0
    count, total_count =0, 0
    for line in lines[:-1]:
        s = line.split()
        # print(s)
        if s[0] == 'time=' and cca_name == 'copa':
            if cca_name == 'copa':
                t = int(s[1].split('.')[0])  #ms
                t = t / 1000 #second
                rtt = float(s[7])
            if s_t == -1:
                s_t = t
                e_t = t+(interval)
            if t - e_t < 0:
                # print(t-e_t)
                tmp_rtt+=rtt
                count+=1
            else:
                w_rtt = tmp_rtt / count
                t_rtt = (t-s_t) # ms to s
                f_rtt.write(str(round(t_rtt, 3))+"\t"+str(round(w_rtt, 1))+"\n")
                total_rtt +=w_rtt
                total_count += 1
                tmp_rtt = rtt
                e_t+=interval
                count = 1
        elif cca_name == 'verus':
            # print(s)
            s = line.split(',')
            t = float(s[0])
            if cca_name == 'verus':
                rtt = float(s[2])
            if s_t == -1:
                s_t = t
                e_t = t+(interval)
            if t - e_t < 0:
                # print(t-e_t)
                tmp_rtt+=rtt
                count+=1
            else:
                w_rtt = tmp_rtt / count
                t_rtt = (t-s_t) # ms to s
                f_rtt.write(str(round(t_rtt, 3))+"\t"+str(round(w_rtt, 1))+"\n")
                total_rtt +=w_rtt
                total_count += 1
                tmp_rtt = rtt
                e_t+=interval
                count = 1
    f_rtt.close()
    return (total_rtt/total_count)

def parse_sprout_rtt_file(rtt_filename):
    f_rtt = open(rtt_log_file, 'w')
    with open(rtt_filename, 'r') as fout:
        lines = fout.read().splitlines()
        print('fout here: parse_sprout_rtt_file')
    fout.close()

    t = 0.0
    w_rtt = 0.0
    rtt, tmp_rtt, total_rtt = 0.0, 0.0, 0.0
    count, total_count =0, 0
    tmp_byte, total_byte = 0.0, 0.0
    init_t, end_t = -1, -1
    for line in lines[:-1]:
        s = line.split(',')
        if line.find('Looping')<0 and line.find('Server')<0 and line.find('Starting')<0 and len(s)>4:
            # print(s)    
            rtt = float(s[4])
            byte = float(s[2])
            try:
                t=float(s[5])/1000
                new_tput = 1
                if end_t == -1:
                    init_t = t
                    end_t = t + interval
            except:
                new_tput = 0

            if new_tput == 0:
                # print('old version')
                if count < 10:
                    tmp_rtt+=rtt
                    count+=1
                else:
                    w_rtt = tmp_rtt / count
                    # print(str(t-init_t)+"\t"+str(round(w_rtt, 1))+"\n")
                    f_rtt.write(str(t-init_t)+"\t"+str(round(w_rtt, 1))+"\n")
                    total_rtt +=w_rtt
                    total_count += 1
                    tmp_rtt = rtt
                    t+=interval
                    count = 1
            elif new_tput > 0:
                # print('new version')
                # print(str(end_t)+'currnet'+str(t))
                # print(interval)
                # print(byte)
                # print(rtt)
                if end_t - t > 0:
                    # print(end_t-t)
                    # print(count)
                    tmp_rtt+=rtt
                    tmp_byte+=byte
                    count+=1
                else:
                    w_rtt = tmp_rtt / count
                    add_tput = tmp_byte*8 / interval /1000000
                    # print(str(t-init_t)+"\t"+str(round(w_rtt, 1))+"\t"+str(add_tput)+"\n")
                    f_rtt.write(str(t-init_t)+"\t"+str(round(w_rtt, 1))+"\t"+str(add_tput)+"\n")
                    total_rtt +=w_rtt
                    total_byte +=tmp_byte
                    total_count += 1
                    tmp_rtt = rtt
                    tmp_byte = byte
                    end_t+=interval
                    count = 1
    if new_tput == 1:
        tput_mean_1 = round(total_byte*8/(end_t-init_t)/1000000, 2)
    else:
        tput_mean_1 = 0
    rtt_mean_1 = round(total_rtt/(t-init_t), 2)
    f_rtt.close()
    return (tput_mean_1, rtt_mean_1)

def parse_file(readfilename):
    # re_resdfilename = re.compile(".*/(?P<ip>[\d.]*)-\d*-(?P<congalg>\w*)")
    # mtch_filename = re_filename.match(filename)
    # client_ip = '10.0.0.127' # get ip add freom phone
    # congalg = mtch_filename.group('congalg')

    f = open(tput_log_file, 'w') #tput
    # f_rtt = open(readfilename[:-4]+'_rtt.txt', 'w')
    with open(readfilename, 'r') as fout:
        lines = fout.read().splitlines()
        print('fout here : parse_file')
    fout.close()

    tmp_dir_path = parse_filename(readfilename)
    y = glob.glob(tmp_dir_path+'/'+'*.txt')
    
    for j in y:
        if j.find("CellInfoClient")>=0:
            cellfile = j
    try:
        with open(cellfile, 'r') as fout_2:
            cellinfo_lines = fout_2.read().splitlines()
        fout_2.close()
    except:
        print('error: no cellfile')
        cellinfo_lines = 0
    init_time, end_time, current_time, check_time = -1.0, -1.0, -1.0, -1.0
    num_bytes, tmp_byte = 0, 0
    rtt, rtt_sum, num_rtt_samples = 0.0, 0.0, 0
    sent_time = {}
    rtt_list = []
    tmp_rtt = 0
    count  = 0
    check = 0
    seq = '0'
    cell_service_num = 'IDK'
    rsrp = 0
    for line in lines[:-1]:
        s = line.split()
        # print(s)
        try:
            if check < len(cellinfo_lines):
                tmpCellinfo = cellinfo_lines[check].split(' ')
                # print(tmpCellinfo)
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
        if len(s) > 5 : #and line.find('UDP') > 0:
            # print(s)
            if s[1] == 'IP' and len(s) > 7 and s[3] != '>':# and (s[13] == 'UDP,' or s[13] == 'TCP,'):
                # print(s)
                ts = get_sec(s[0])
                seq = s[7].split(',')[0]
                if init_time == -1:
                    init_time = ts
                    end_time = ts + interval
                    check_time = end_time
                    check = 0
                # print(seq)
            elif s[1] == 'IP' and s[3] == '>' and s[2].find('.'+str(PORT))>=0: # for old version
                # 12:28:30.948828 IP 128.110.154.167.9001 > 174.248.154.114.2793: UDP, length 1440
                ts = get_sec(s[0])
                if init_time == -1:
                    init_time = ts
                    end_time = ts + interval
                    check_time = end_time
                    check = 0
                current_time = ts
                try:
                    num_bytes += int(s[s.index('length')+1])
                except:
                    continue    
                if end_time - current_time > 0:
                    tmp_byte += int(s[s.index('length')+1])
                else:
                    tpt = 8e-6 * tmp_byte / interval
                    # print(str(current_time) +' '+ str(tpt))
                    # write
                    f.write(str(round(current_time-init_time, 3))+"\t"+str(round(tpt, 3))+"\t"+str(cell_service_num)+"\t"+str(rsrp)+"\n")
                    # reset
                    tmp_byte = int(s[s.index('length')+1])
                    end_time += interval
                    check +=1
            elif s[0].find('.'+str(PORT))>=0:
                # print(s)
                direction == "data"
                current_time = ts
                try:
                    num_bytes += int(s[s.index('length')+1])
                except:
                    continue    
                if end_time - current_time > 0:
                    tmp_byte += int(s[s.index('length')+1])
                else:
                    tpt = 8e-6 * tmp_byte / interval
                    # print(str(current_time) +' '+ str(tpt))
                    # write
                    f.write(str(round(current_time-init_time, 3))+"\t"+str(round(tpt, 3))+"\t"+str(cell_service_num)+"\t"+str(rsrp)+"\n")
                    # reset
                    tmp_byte = int(s[s.index('length')+1])
                    end_time += interval
                    check +=1

    f.close()
    # f_rtt.close()
    rtt_mean = 0
    tput_mean = 8e-6 * num_bytes / (end_time - init_time)
    
    if cca_name == 'copa':
        if rtt_filename.find('.txt')>0:
            rtt_mean = int(parse_copa_rtt_file(rtt_filename))
            draw_copa_figure(round(tput_mean,3), rtt_mean)
        else:
            draw_copa_figure(round(tput_mean,3), 0)
    elif cca_name == 'verus':
        if rtt_filename.find('Receiver.out')>0:
            rtt_mean = int(parse_copa_rtt_file(rtt_filename))
            print("tput_mean : "+ str(tput_mean)+" rtt : " +str(rtt_mean))
            draw_copa_figure(round(tput_mean,3), rtt_mean)

    elif cca_name == 'sprout':
        tput_mean_new, rtt_mean = parse_copa_sprout_file(rtt_filename)
        if tput_mean_new == 0:
            draw_sprout_old_figure(round(tput_mean,3), rtt_mean)
        else:
            draw_sprout_new_figure(tput_mean_new, rtt_mean)

def parse_file_sprout(readfilename):
    # re_resdfilename = re.compile(".*/(?P<ip>[\d.]*)-\d*-(?P<congalg>\w*)")
    # mtch_filename = re_filename.match(filename)
    # client_ip = '10.0.0.127' # get ip add freom phone
    # congalg = mtch_filename.group('congalg')

    f = open(tput_log_file, 'w')
    # f_rtt = open(readfilename[:-4]+'_rtt.txt', 'w')
    with open(readfilename, 'r') as fout:
        lines = fout.read().splitlines()
        print('fout here : parse_file_sprout')
    fout.close()

    init_time, end_time, current_time, check_time = -1.0, -1.0, -1.0, -1.0
    num_bytes, tmp_byte = 0, 0
    rtt, rtt_sum, num_rtt_samples = 0.0, 0.0, 0
    sent_time = {}
    rtt_list = []
    tmp_rtt = 0
    count  = 0
    check = 0
    seq = '0'
    cell_service_num = 'IDK'
    rsrp = 0
    for line in lines[:-1]:
        s = line.split()
        if len(s) > 5 : #and line.find('UDP') > 0:
            # print(s)
            if s[1] == 'IP':# and (s[13] == 'UDP,' or s[13] == 'TCP,'):
                # print(s)
                ts = get_sec(s[0])
                seq = s[7].split(',')[0]
                if init_time == -1:
                    init_time = ts
                    end_time = ts + interval
                    check_time = end_time
                    check = 0
                # print(seq)
            elif s[0].find('.'+str(PORT))>=0:
                # print(s)
                direction == "data"
                current_time = ts
                try:
                    num_bytes += int(s[s.index('length')+1])
                except:
                    continue    
                if end_time - current_time > 0:
                    tmp_byte += int(s[s.index('length')+1])
                else:
                    tpt = 8e-6 * tmp_byte / interval
                    print(str(current_time) +' '+ str(tpt)+' '+str(check))
                    # write
                    if check == 0:
                        print('Starting...')
                    else:
                        f.write(str(round(current_time-init_time, 3))+"\t"+str(round(tpt, 3))+"\t"+str(-1)+"\t"+str(0)+"\n")
                    # reset
                    tmp_byte = int(s[s.index('length')+1])
                    end_time += interval
                    check +=1
    tput_mean = 8e-6 * num_bytes / (end_time - init_time)
    f.close()
    # f_rtt.close()
    rtt_mean = 0
    tput_mean_new, rtt_mean = parse_sprout_rtt_file(rtt_filename)
    print(round(tput_mean, 2), tput_mean_new, rtt_mean)
    if tput_mean_new == 0:
        draw_sprout_old_figure(round(tput_mean,3), rtt_mean)
    else:
        draw_sprout_new_figure(tput_mean_new, rtt_mean)

def draw_copa_figure(tput_mean, rtt_mean):
    f_tpt = open('tmpPltFile', 'w')
    f_tpt.write( "reset;\n" )
    f_tpt.write( "set terminal unknown;\n" )
    f_tpt.write( "set terminal gif font 'Arial' 12;\n" )
    f_tpt.write( "set output '"+filename+"_tput.png';\n" )
    f_tpt.write( "set term png size 1000, 400;\n" )
    f_tpt.write( "set title '"+cca_name+"' font 'Arial-Bold, 19';\n" )
    f_tpt.write( "set key top horizontal left;\n" )
    f_tpt.write( "set xlabel 'Time (Seconds)';\n" )
    f_tpt.write( "set ylabel 'Throghtput (Mbps) Avg:"+str(round(tput_mean,3))+";\n" )
    f_tpt.write( "set y2label 'RSRP';\n" )
    f_tpt.write( "set ytics nomirror;\n" )
    f_tpt.write( "set ytics textcolor rgb 'red';\n" )
    f_tpt.write( "set y2tics nomirror;\n" )
    f_tpt.write( "set y2tics textcolor rgb 'blue';\n" )
    f_tpt.write( "set xrange [0:];\n" )
    f_tpt.write( "set y2range [-125:-50];\n" )
    f_tpt.write( "set yrange [0:];\n" )
    f_tpt.write( "set boxwidth 0.9;\n" )
    f_tpt.write( "set xtics scale 1 nomirror offset 1.5;\n" )
    f_tpt.write( "set style line 1 lt 1 lw 0.5;\n" )
    f_tpt.write( "set style fill solid border -1\n" )
    f_tpt.write( "set style line 1 lt 1 pt 1 ps 1 lc rgb 'red' lw 1\n" )
    f_tpt.write( "set style line 2 lt 1 pt 2 ps 1 lc rgb 'blue' lw 1\n" )
    f_tpt.write( "set style line 3 lt 1 pt 3 ps 1 lc rgb 'green' lw 1\n" )
    f_tpt.write( "set style line 4 lt 1 pt 4 ps 1 lc rgb 'orange' lw 1\n" )
    f_tpt.write( "set style line 5 lt 1 pt 4 ps 1 lc rgb 'violet' lw 1\n" )
    # format: 1time, 2mss, 3cwnd, 4(cwnd * mss)/1024, 5s ssth, 6r ssth, 7rtt, 8rtt_var, 9unacked, 10throghtput, 11cell_service, 12rsrp, 13pci
    f_tpt.write( "plot '"+tput_log_file+"'  every ::1 using 1:2 ls 1 title 'Throughput' with lines,\\\n " )
    f_tpt.write("   '"+tput_log_file+"'  every ::1 using 1:4 ls 3 title 'RSRP' axes x1y2 with lines,\n " )

    cmd = "gnuplot tmpPltFile\n cp "+tput_log_file+" probedata"
    f_tpt.close()
    cmd_run(cmd)

    if rtt_mean != 0:
        f_rtt = open('tmpPltFile', 'w')
        f_rtt.write( "reset;\n" )
        f_rtt.write( "set terminal unknown;\n" )
        f_rtt.write( "set terminal gif font 'Arial' 12;\n" )
        f_rtt.write( "set output '"+filename+"_rtt.png';\n" )
        f_rtt.write( "set term png size 1000, 400;\n" )
        f_rtt.write( "set title '"+cca_name+"'  font 'Arial-Bold, 19';\n" )
        f_rtt.write( "set key top horizontal left;\n" )
        f_rtt.write( "set xlabel 'Time (Seconds)';\n" )
        # f_rtt.write( "set ylabel 'Throughput (Mbps)';\n" )
        f_rtt.write( "set ylabel 'RTT (ms)"+str(rtt_mean)+"';\n" )
        f_rtt.write( "set ytics nomirror;\n" )
        f_rtt.write( "set ytics textcolor rgb 'red';\n" )
        # f_rtt.write( "set y2tics nomirror;\n" )
        # f_rtt.write( "set y2tics textcolor rgb 'blue';\n" )
        f_rtt.write( "set xrange [0:];\n" )
        f_rtt.write( "set y2range [0:];\n" )
        f_rtt.write( "set yrange [0:];\n" )
        f_rtt.write( "set boxwidth 0.9;\n" )
        f_rtt.write( "set xtics scale 1 nomirror offset 1.5;\n" )
        f_rtt.write( "set style line 1 lt 1 lw 0.5;\n" )
        f_rtt.write( "set style fill solid border -1\n" )
        f_rtt.write( "set style line 1 lt 1 lc rgb 'red' lw 1\n" )
        f_rtt.write( "set style line 2 lt 1 pt 2 ps 1 lc rgb 'blue' lw 1\n" )
        f_rtt.write( "set style line 3 lt 1 pt 3 ps 1 lc rgb 'green' lw 1\n" )
        f_rtt.write( "set style line 4 lt 1 pt 4 ps 1 lc rgb 'orange' lw 1\n" )
        f_rtt.write( "set style line 5 lt 1 pt 4 ps 1 lc rgb 'violet' lw 1\n" )
        # format: 1time, 2mss, 3cwnd, 4(cwnd * mss)/1024, 5s ssth, 6r ssth, 7rtt, 8rtt_var, 9unacked, 10throghtput, 11cell_service, 12rsrp, 13pci
        f_rtt.write("plot '"+rtt_log_file+"' every ::1 using 1:2 ls 1 title 'RTT' with lines,\n " )
        # f_rtt.write("  '"+rtt_log_file+"' every ::1 using 1:2 ls 2 title 'RTT' axes x1y2  with lines,\n " )

        cmd = "gnuplot tmpPltFile\n cp "+rtt_log_file+" probedata"
        f_rtt.close()
        cmd_run(cmd)

def draw_sprout_old_figure(tput_mean, rtt_mean):
    f_tpt = open('tmpPltFile', 'w')
    f_tpt.write( "reset;\n" )
    f_tpt.write( "set terminal unknown;\n" )
    # f_tpt.write( "plot '"+readfilename[:-4]+"_p.txt' using 1:2;\n" ) 
    f_tpt.write( "set terminal gif font 'Arial' 12;\n" )
    f_tpt.write( "set output '"+filename+"_tput.png';\n" )
    f_tpt.write( "set term png size 1000, 400;\n" )
    f_tpt.write( "set title '"+cca_name+"' font 'Arial-Bold, 19';\n" )
    f_tpt.write( "set key top horizontal left;\n" )
    f_tpt.write( "set xlabel 'Time (Seconds)';\n" )
    f_tpt.write( "set ylabel 'Throghtput (Mbps) Avg:"+str(round(tput_mean,3))+";\n" )
    f_tpt.write( "set y2label 'RSRP';\n" )
    f_tpt.write( "set ytics nomirror;\n" )
    f_tpt.write( "set ytics textcolor rgb 'red';\n" )
    f_tpt.write( "set y2tics nomirror;\n" )
    f_tpt.write( "set y2tics textcolor rgb 'blue';\n" )
    f_tpt.write( "set xrange [0:];\n" )
    f_tpt.write( "set y2range [-125:-50];\n" )
    f_tpt.write( "set yrange [0:];\n" )
    f_tpt.write( "set boxwidth 0.9;\n" )
    f_tpt.write( "set xtics scale 1 nomirror offset 1.5;\n" )
    f_tpt.write( "set style line 1 lt 1 lw 0.5;\n" )
    f_tpt.write( "set style fill solid border -1\n" )
    f_tpt.write( "set style line 1 lt 1 pt 1 ps 1 lc rgb 'red' lw 1\n" )
    f_tpt.write( "set style line 2 lt 1 pt 2 ps 1 lc rgb 'blue' lw 1\n" )
    f_tpt.write( "set style line 3 lt 1 pt 3 ps 1 lc rgb 'green' lw 1\n" )
    f_tpt.write( "set style line 4 lt 1 pt 4 ps 1 lc rgb 'orange' lw 1\n" )
    f_tpt.write( "set style line 5 lt 1 pt 4 ps 1 lc rgb 'violet' lw 1\n" )
    # format: 1time, 2mss, 3cwnd, 4(cwnd * mss)/1024, 5s ssth, 6r ssth, 7rtt, 8rtt_var, 9unacked, 10throghtput, 11cell_service, 12rsrp, 13pci
    f_tpt.write( "plot '"+tput_log_file+"'  every ::1 using 1:2 ls 1 title 'Throughput' with lines,\\\n " )
    f_tpt.write("   '"+tput_log_file+"'  every ::1 using 1:4 ls 3 title 'RSRP' axes x1y2 with lines,\n " )

    cmd = "gnuplot tmpPltFile\n cp "+tput_log_file+" probedata"
    f_tpt.close()
    cmd_run(cmd)

    f_rtt = open('tmpPltFile', 'w')
    f_rtt.write( "reset;\n" )
    f_rtt.write( "set terminal unknown;\n" )
    # f_rtt.write( "plot 'tmpRttFile' using 1:2;\n" ) 
    f_rtt.write( "set terminal gif font 'Arial' 12;\n" )
    f_rtt.write( "set output '"+filename+"_rtt.png';\n" )
    f_rtt.write( "set term png size 1000, 400;\n" )
    f_rtt.write( "set title '"+cca_name+"'  font 'Arial-Bold, 19';\n" )
    f_rtt.write( "set key top horizontal left;\n" )
    f_rtt.write( "set xlabel 'Time (Seconds)';\n" )
    # f_rtt.write( "set ylabel 'Throughput (Mbps)';\n" )
    f_rtt.write( "set ylabel 'RTT (ms)"+str(rtt_mean)+"';\n" )
    f_rtt.write( "set ytics nomirror;\n" )
    f_rtt.write( "set ytics textcolor rgb 'red';\n" )
    # f_rtt.write( "set y2tics nomirror;\n" )
    # f_rtt.write( "set y2tics textcolor rgb 'blue';\n" )
    f_rtt.write( "set xrange [0:];\n" )
    # f_rtt.write( "set y2range [0:];\n" )
    f_rtt.write( "set yrange [0:];\n" )
    f_rtt.write( "set boxwidth 0.9;\n" )
    f_rtt.write( "set xtics scale 1 nomirror offset 1.5;\n" )
    f_rtt.write( "set style line 1 lt 1 lw 0.5;\n" )
    f_rtt.write( "set style fill solid border -1\n" )
    f_rtt.write( "set style line 1 lt 1 pt 1 ps 1 lc rgb 'red' lw 1\n" )
    f_rtt.write( "set style line 2 lt 1 pt 2 ps 1 lc rgb 'blue' lw 1\n" )
    f_rtt.write( "set style line 3 lt 1 pt 3 ps 1 lc rgb 'green' lw 1\n" )
    f_rtt.write( "set style line 4 lt 1 pt 4 ps 1 lc rgb 'orange' lw 1\n" )
    f_rtt.write( "set style line 5 lt 1 pt 4 ps 1 lc rgb 'violet' lw 1\n" )
    # format: 1time, 2mss, 3cwnd, 4(cwnd * mss)/1024, 5s ssth, 6r ssth, 7rtt, 8rtt_var, 9unacked, 10throghtput, 11cell_service, 12rsrp, 13pci
    f_rtt.write("plot '"+rtt_log_file+"' every ::1 using 1:2 ls 1 title 'RTT' with lines,\n " )
    # f_rtt.write("  '"+rtt_log_file+"' every ::1 using 1:2 ls 2 title 'RTT' axes x1y2  with lines,\n " )

    cmd = "gnuplot tmpPltFile\n cp "+rtt_log_file+" probedata"
    f_rtt.close()
    cmd_run(cmd)

def draw_sprout_new_figure(tput_mean, rtt_mean):
    f_tpt = open('tmpPltFile', 'w')
    f_tpt.write( "reset;\n" )
    f_tpt.write( "set terminal unknown;\n" )
    # f_tpt.write( "plot '"+readfilename[:-4]+"_p.txt' using 1:2;\n" ) 
    f_tpt.write( "set terminal gif font 'Arial' 12;\n" )
    f_tpt.write( "set output '"+filename+"_tput.png';\n" )
    f_tpt.write( "set term png size 1000, 400;\n" )
    f_tpt.write( "set title '"+cca_name+"' font 'Arial-Bold, 19';\n" )
    f_tpt.write( "set key top horizontal left;\n" )
    f_tpt.write( "set xlabel 'Time (Seconds)';\n" )
    f_tpt.write( "set ylabel 'Throghtput (Mbps) Avg:"+str(round(tput_mean,3))+";\n" )
    f_tpt.write( "set y2label 'RSRP';\n" )
    f_tpt.write( "set ytics nomirror;\n" )
    f_tpt.write( "set ytics textcolor rgb 'red';\n" )
    f_tpt.write( "set y2tics nomirror;\n" )
    f_tpt.write( "set y2tics textcolor rgb 'blue';\n" )
    f_tpt.write( "set xrange [0:];\n" )
    f_tpt.write( "set y2range [-125:-50];\n" )
    f_tpt.write( "set yrange [0:];\n" )
    f_tpt.write( "set boxwidth 0.9;\n" )
    f_tpt.write( "set xtics scale 1 nomirror offset 1.5;\n" )
    f_tpt.write( "set style line 1 lt 1 lw 0.5;\n" )
    f_tpt.write( "set style fill solid border -1\n" )
    f_tpt.write( "set style line 1 lt 1 pt 1 ps 1 lc rgb 'red' lw 1\n" )
    f_tpt.write( "set style line 2 lt 1 pt 2 ps 1 lc rgb 'blue' lw 1\n" )
    f_tpt.write( "set style line 3 lt 1 pt 3 ps 1 lc rgb 'green' lw 1\n" )
    f_tpt.write( "set style line 4 lt 1 pt 4 ps 1 lc rgb 'orange' lw 1\n" )
    f_tpt.write( "set style line 5 lt 1 pt 4 ps 1 lc rgb 'violet' lw 1\n" )
    # format: 1time, 2mss, 3cwnd, 4(cwnd * mss)/1024, 5s ssth, 6r ssth, 7rtt, 8rtt_var, 9unacked, 10throghtput, 11cell_service, 12rsrp, 13pci
    f_tpt.write( "plot '"+tput_log_file+"'  every ::1 using 1:2 ls 1 title 'Throughput' with lines,\\\n " )
    f_tpt.write("   '"+tput_log_file+"'  every ::1 using 1:4 ls 3 title 'RSRP' axes x1y2 with lines,\n " )

    cmd = "gnuplot tmpPltFile\n cp "+tput_log_file+" probedata"
    f_tpt.close()
    cmd_run(cmd)

    f_rtt = open('tmpPltFile', 'w')
    f_rtt.write( "reset;\n" )
    f_rtt.write( "set terminal unknown;\n" )
    # f_rtt.write( "plot 'tmpRttFile' using 1:2;\n" ) 
    f_rtt.write( "set terminal gif font 'Arial' 12;\n" )
    f_rtt.write( "set output '"+filename+"_rtt.png';\n" )
    f_rtt.write( "set term png size 1000, 400;\n" )
    f_rtt.write( "set title '"+cca_name+"'  font 'Arial-Bold, 19';\n" )
    f_rtt.write( "set key top horizontal left;\n" )
    f_rtt.write( "set xlabel 'Time (Seconds)';\n" )
    f_rtt.write( "set ylabel 'Throughput (Mbps)';\n" )
    f_rtt.write( "set y2label 'RTT (ms)"+str(rtt_mean)+"';\n" )
    f_rtt.write( "set ytics nomirror;\n" )
    f_rtt.write( "set ytics textcolor rgb 'red';\n" )
    f_rtt.write( "set y2tics nomirror;\n" )
    f_rtt.write( "set y2tics textcolor rgb 'blue';\n" )
    f_rtt.write( "set xrange [0:];\n" )
    f_rtt.write( "set y2range [0:];\n" )
    f_rtt.write( "set yrange [0:];\n" )
    f_rtt.write( "set boxwidth 0.9;\n" )
    f_rtt.write( "set xtics scale 1 nomirror offset 1.5;\n" )
    f_rtt.write( "set style line 1 lt 1 lw 0.5;\n" )
    f_rtt.write( "set style fill solid border -1\n" )
    f_rtt.write( "set style line 1 lt 1 pt 1 ps 1 lc rgb 'red' lw 1\n" )
    f_rtt.write( "set style line 2 lt 1 pt 2 ps 1 lc rgb 'blue' lw 1\n" )
    f_rtt.write( "set style line 3 lt 1 pt 3 ps 1 lc rgb 'green' lw 1\n" )
    f_rtt.write( "set style line 4 lt 1 pt 4 ps 1 lc rgb 'orange' lw 1\n" )
    f_rtt.write( "set style line 5 lt 1 pt 4 ps 1 lc rgb 'violet' lw 1\n" )
    # format: 1time, 2mss, 3cwnd, 4(cwnd * mss)/1024, 5s ssth, 6r ssth, 7rtt, 8rtt_var, 9unacked, 10throghtput, 11cell_service, 12rsrp, 13pci
    f_rtt.write("plot '"+rtt_log_file+"' every ::1 using 1:3 ls 1 title 'Tput' with lines,\\\n " )
    f_rtt.write("  '"+rtt_log_file+"' every ::1 using 1:2 ls 2 title 'RTT' axes x1y2  with lines,\n " )

    cmd = "gnuplot tmpPltFile\n cp "+rtt_log_file+" probedata"
    f_rtt.close()
    cmd_run(cmd)

if cca_name == 'copa' or cca_name=='verus':
    parse_file(readfilename)
elif cca_name == 'sprout':
    parse_file_sprout(readfilename)