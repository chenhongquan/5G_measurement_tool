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

print('run new_plot_from_tcp.py')

# readfilename filename(wrt) CCA_name
# python3 new_plot_from_udp.py readfilename filename(wrt) CCA_name
if(len(sys.argv)<3):
	print ("Usage error: --tput_file --tcpprobefile --output_dir --cca_name")
	exit()

readfilename=sys.argv[1]
probefilename=sys.argv[2]
filename=sys.argv[3]
cca_name=sys.argv[4]

tmp_file_name = readfilename[:-26] + '_tput.log'
tmp_rtt_file_name = readfilename[:-26] + '_rtt.log'

# print(tmp_file_name)
def parse_filename(filename):
    path = filename
    head_tail = os.path.split(path) 
    return head_tail[0]

def parse_file(readfilename):
    # re_resdfilename = re.compile(".*/(?P<ip>[\d.]*)-\d*-(?P<congalg>\w*)")
    # mtch_filename = re_filename.match(filename)
    # client_ip = '10.0.0.127' # get ip add freom phone
    # congalg = mtch_filename.group('congalg')

    f = open(tmp_file_name, 'w')
    # f_rtt = open(probefilename, 'w')
    with open(readfilename, 'r') as fout:
        lines = fout.read().splitlines()
        # print('fout here')
    fout.close()

    # with open(probefilename, 'r') as f_rtt_out:
    #     lines_rtt = f_rtt_out.read().splitlines()
    #     # print('fout here')
    # f_rtt_out.close()

    tmp_dir_path = parse_filename(readfilename)
    y = glob.glob(tmp_dir_path+'/'+'*.txt')
    # print(y)
    for j in y:
        if j.find("CellInfoClient")>=0:
            cellfile = j
    # # print(cellfile)
    try:
        with open(cellfile, 'r') as fout_2:
            cellinfo_lines = fout_2.read().splitlines()
        fout_2.close()
    except:
        print('no cell info')
    
    init_time, end_time, ts, check_time = -1, -1, -1, -1
    init_time_arrage = 0
    num_bytes, tmp_byte = 0, 0
    sent_time = {}
    count  = 0
    check = 0
    seq = '0'
    ts = -1.0
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
            if s[1] == 'IP':# and len(s) > 20:# and (s[13] == 'UDP,' or s[13] == 'TCP,'):
                if len(s) >= 20: # one line results
                    # 'old+version version=0'
                    if s[2].find('.'+str(PORT))>=0 :
                        # 'old+version'
                        version=0
                        ts = get_sec(s[0])
                        # seq = s[7].split(',')[0]
                        if init_time == -1:
                            # print(s)
                            init_time = ts
                            end_time = ts + interval
                            check_time = end_time
                            check = 0
                        num_bytes += int(s[s.index('length')+1])
                        # print(num_bytes, end_time-ts)
                        if end_time - ts > 0:
                            tmp_byte += int(s[s.index('length')+1])
                        else:
                            tpt = 8e-6 * tmp_byte / interval
                            # print(str(ts) +' '+ str(tpt))
                            # write
                            f.write(str(ts-init_time)+"\t"+str(round(tpt, 3))+"\t"+str(cell_service_num)+"\t"+str(rsrp)+"\n")
                            # reset
                            tmp_byte = int(s[s.index('length')+1])
                            end_time += interval
                            check +=1

                elif len(s) < 20:
                    # 'new_version'
                    # print(s)
                    version = 1
                    ts = get_sec(s[0])
                    if init_time == -1:
                        init_time = ts
                        # print(init_time)
                        end_time = ts + interval
                        check_time = end_time
                        check = 0

            elif  s[1] == '>':
                if s[0].find('.'+str(PORT))>=0:
                    current_time = ts
                    try:
                        num_bytes += int(s[s.index('length')+1])
                    except:
                        continue    
                    if end_time - current_time > 0:
                        tmp_byte += int(s[s.index('length')+1])
                    else:
                        # print(current_time, init_time, check)
                        if check == 0:
                            init_time_arrage = current_time
                        tpt = 8e-6 * tmp_byte / interval
                        # print(str(current_time) +' '+ str(tpt))
                        # write
                        f.write(str(round(current_time-init_time_arrage, 3))+"\t"+str(round(tpt, 3))+"\t"+str(-1)+"\t"+str(0)+"\n")
                        # reset
                        tmp_byte = int(s[s.index('length')+1])
                        end_time += interval
                        check +=1            
    f.close()

    tput_mean = 8e-6 * num_bytes / (end_time - init_time)
    rtt_mean = 0
    if probefilename.find('.txt') > 0:
        rtt_mean = parse_tcpprobe_file(probefilename)
        draw_figure(tput_mean, rtt_mean)
    else:
        draw_figure_only_tput(tput_mean)
    # print(rtt_mean, tput_mean)
    return (round(tput_mean,3), round(rtt_mean, 3), end_time - init_time)

def parse_tcpprobe_file(filename):
    f_rtt = open(tmp_rtt_file_name, 'w')
    with open(filename, 'r') as fout:
        lines = fout.read().splitlines()
    fout.close()

    # remove this
    t, init_t=0.0, -1
    mss = 0
    cwnd = 0
    KB_cwnd = 0
    check = 0
    rtt_mean = 0
    rtt_count = 0

    for line in lines[:-1]:
        s = line.split()
        t = float(s[0])
        if init_t == -1:
            init_t = t
        rtt = int(s[9])/1000
        rtt_mean +=rtt
        rtt_count +=1
        ca_name = s[26]
        f_rtt.write(str(t-init_t)+"\t"+str(rtt)+"\t"+str(s[6])+"\t"+str(s[8])+"\t"+str(s[10])+"\t"+str(s[23])+"\n") # time rtt cwnd snd_wnd rcv_wnd mss
        # f_rtt.write(str(t)+"\t"+str(s[6])+"\t"+str(s[7])+"\t"+str(s[8])+"\t"+str(rtt)+"\t"+str(s[10])+"\t"+str(s[11])+"\t"+str(s[12])+"\t"+str(s[13])+"\t"+str(s[14])+"\t"+str(s[15])+"\t"+str(s[16])+"\t"+str(s[17])+"\t"+str(s[18])+"\t"+str(s[19])+"\t"+str(s[20])+"\t"+str(s[21])+"\t"+str(s[22])+"\t"+str(s[23])+"\t"+str(s[24])+"\t"+str(s[25])+"\n")
    f_rtt.close()

    rtt_mean = rtt_mean/rtt_count
    return rtt_mean

def draw_figure_only_tput(tput_mean):
    f_tpt = open('tmpPltFile', 'w')
    f_tpt.write( "reset;\n" )
    f_tpt.write( "set terminal unknown;\n" )
    f_tpt.write( "plot '"+ tmp_file_name+"' using 1:2;\n" ) 
    f_tpt.write( "set terminal gif font 'Arial' 12;\n" )
    f_tpt.write( "set output '"+filename+"_tput.png';\n" )
    f_tpt.write( "set term png size 1000, 400;\n" )
    f_tpt.write( "set title '"+cca_name+"' font 'Arial-Bold, 19';\n" )
    f_tpt.write( "set key top horizontal left;\n" )
    f_tpt.write( "set xlabel 'Time (Seconds)';\n" )
    f_tpt.write( "set ylabel 'Throghtput (Mbps) Avg:"+str(round(tput_mean,3))+";\n" )
    # f_tpt.write( "set y2label 'RSRP';\n" )
    f_tpt.write( "set ytics nomirror;\n" )
    f_tpt.write( "set ytics textcolor rgb 'red';\n" )
    # f_tpt.write( "set y2tics nomirror;\n" )
    # f_tpt.write( "set y2tics textcolor rgb 'blue';\n" )
    f_tpt.write( "set xrange [0:];\n" )
    # f_tpt.write( "set y2range [-125:-50];\n" )
    f_tpt.write( "set yrange [0:];\n" )
    f_tpt.write( "set boxwidth 0.9;\n" )
    f_tpt.write( "set xtics scale 1 nomirror offset 1.5;\n" )
    f_tpt.write( "set style line 1 lt 1 lw 0.5;\n" )
    f_tpt.write( "set style fill solid border -1\n" )
    f_tpt.write( "set style line 1 lt 1 lc rgb 'blue' lw 1\n" )
    f_tpt.write( "set style line 2 lt 1 pt 2 ps 1 lc rgb 'red' lw 1\n" )
    f_tpt.write( "set style line 3 lt 1 pt 3 ps 1 lc rgb 'green' lw 1\n" )
    f_tpt.write( "set style line 4 lt 1 pt 4 ps 1 lc rgb 'orange' lw 1\n" )
    f_tpt.write( "set style line 5 lt 1 pt 4 ps 1 lc rgb 'violet' lw 1\n" )
    # format: 1time, 2mss, 3cwnd, 4(cwnd * mss)/1024, 5s ssth, 6r ssth, 7rtt, 8rtt_var, 9unacked, 10throghtput, 11cell_service, 12rsrp, 13pci
    f_tpt.write( "plot '"+tmp_file_name+"'  every ::1 using 1:2 ls 1 title 'Throughput' with lines,\n " )
    # f_tpt.write( " '"+tmp_file_name+"' using 1:3 ls 2 title 'CWND (y2)' axes x1y2 with lines,\n " )
    # f_tpt.write( " '"+tmp_file_name+"'  every ::1 using 1:4 ls 3 title 'RSRP' axes x1y2 with lines,\n " )

    cmd = "gnuplot tmpPltFile\n cp "+tmp_file_name+" probedata"
    f_tpt.close()
    cmd_run(cmd)

def draw_figure(tput_mean, rtt_mean):
    print(rtt_mean, tput_mean)
    f_tpt = open('tmpPltFile', 'w')
    f_tpt.write( "reset;\n" )
    f_tpt.write( "set terminal unknown;\n" )
    f_tpt.write( "plot '"+ tmp_file_name+"' using 1:2;\n" ) 
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
    f_tpt.write( "set style line 1 lt 1 lc rgb 'blue' lw 1\n" )
    f_tpt.write( "set style line 2 lt 1 pt 2 ps 1 lc rgb 'red' lw 1\n" )
    f_tpt.write( "set style line 3 lt 1 pt 3 ps 1 lc rgb 'green' lw 1\n" )
    f_tpt.write( "set style line 4 lt 1 pt 4 ps 1 lc rgb 'orange' lw 1\n" )
    f_tpt.write( "set style line 5 lt 1 pt 4 ps 1 lc rgb 'violet' lw 1\n" )
    # format: 1time, 2mss, 3cwnd, 4(cwnd * mss)/1024, 5s ssth, 6r ssth, 7rtt, 8rtt_var, 9unacked, 10throghtput, 11cell_service, 12rsrp, 13pci
    f_tpt.write( "plot '"+tmp_file_name+"'  every ::1 using 1:2 ls 1 title 'Throughput' with lines,\\\n " )
    # f_tpt.write( " '"+tmp_file_name+"' using 1:3 ls 2 title 'CWND (y2)' axes x1y2 with lines,\n " )
    f_tpt.write( " '"+tmp_file_name+"'  every ::1 using 1:4 ls 3 title 'RSRP' axes x1y2 with lines,\n " )

    cmd = "gnuplot tmpPltFile\n cp "+tmp_file_name+" probedata"
    f_tpt.close()
    cmd_run(cmd)

    f_rtt = open('tmpPltFile', 'w')
    f_rtt.write( "reset;\n" )
    f_rtt.write( "set terminal unknown;\n" )
    f_rtt.write( "plot '"+tmp_rtt_file_name+"' using 1:2;\n" ) 
    f_rtt.write( "set terminal gif font 'Arial' 12;\n" )
    f_rtt.write( "set output '"+filename+"_rtt.png';\n" )
    f_rtt.write( "set term png size 1000, 400;\n" )
    f_rtt.write( "set title '"+cca_name+"' font 'Arial-Bold, 19';\n" )
    f_rtt.write( "set key top horizontal left;\n" )
    f_rtt.write( "set xlabel 'Time (Seconds)';\n" )
    f_rtt.write( "set ylabel 'RTT (ms) Avg:"+str(rtt_mean)+";\n" )
    # f_rtt.write( "set y2label 'RTT var';\n" )
    f_rtt.write( "set ytics nomirror;\n" )
    f_rtt.write( "set ytics textcolor rgb 'red';\n" )
    # f_rtt.write( "set y2tics nomirror;\n" )
    # f_rtt.write( "set y2tics textcolor rgb 'blue';\n" )
    f_rtt.write( "set xrange [0:];\n" )
    # f_rtt.write( "set y2range [0:];\n" )
    f_rtt.write( "set yrange [0:];\n" )
    f_rtt.write( "set boxwidth 0.9;\n" )
    f_rtt.write( "set xtics scale 1 nomirror offset 1.5;\n" )
    # f_rtt.write( "set style line 1 lt 1 lw 0.5;\n" )
    f_rtt.write( "set style fill solid border -1\n" )
    f_rtt.write( "set style line 1 lt 1 lc rgb 'red' lw 1\n" )
    # f_rtt.write( "set style line 2 lt 1 pt 2 ps 1 lc rgb 'blue' lw 1\n" )
    # f_rtt.write( "set style line 3 lt 1 pt 3 ps 1 lc rgb 'red' lw 1\n" )
    # f_rtt.write( "set style line 4 lt 1 pt 4 ps 1 lc rgb 'orange' lw 1\n" )
    # f_rtt.write( "set style line 5 lt 1 pt 4 ps 1 lc rgb 'violet' lw 1\n" )
    # format: 1time, 2mss, 3cwnd, 4(cwnd * mss)/1024, 5s ssth, 6r ssth, 7rtt, 8rtt_var, 9unacked, 10throghtput, 11cell_service, 12rsrp, 13pci
    f_rtt.write( "plot '"+tmp_rtt_file_name+"'  every ::1 using 1:2 ls 1 title 'RTT' with lines,\n " )
    # f_rtt.write( " '"+tmp_rtt_file_name+"' every ::1 using 1:3 ls 2 title 'RTT var (y2)' axes x1y2 with linespoints,\n " )
    # f_rtt.write( " '"+tmp_file_name+"' using 1:4 ls 3 title 'RTT' axes x1y2 with linespoints,\n " )

    cmd = "gnuplot tmpPltFile\n cp "+tmp_rtt_file_name+" probedata"
    f_rtt.close()
    cmd_run(cmd)

parse_file(readfilename)
