import re
import os 
import time
import sys
import sqlite3 as lite
import glob
import subprocess 
from threading import Thread
import numpy as np
# import strftime from time
from datetime import datetime
import sys
sys.path.append("../config/")
from setup import * 

if(len(sys.argv)<3):
	print ("Usage error: --tput_file --output_dir")
	exit()

readfilename=sys.argv[1]
# rtt_readfilename=sys.argv[2] 
filename=sys.argv[2]
print(readfilename)

S_addr = str(HOST)+'.'+str(PORT)S

# draw with tcpprobe data
os.system('python3 ../server/plot_tcp_other.py '+str(duration)+' foreground 1 1 c2tcp')

f = open('tmpDataFile', 'w')
with open(readfilename, 'r') as fout:
    lines = fout.read().splitlines()
    print('fout here')
fout.close()

print(lines[0].split())
l = lines[0].split()
t=-1
# bit = 0
start_time = -1
end_time = -1
tmp_byte = 0
total_byte = 0
# end_time = start_time
print(start_time)
for line in lines[:-1]:
    s = line.split()
    # print(s[2]+' and '+s[4])
    if len(s) >= 15 and s[2] == S_addr: #and s[4].find('174.248.152.70')>=0:
        # t = s[0]
        # print('print lines is here ', s)
        t = get_sec(s[0])
        # print('getting t '+str(t))
        if start_time == -1:
            start_time = t
        if end_time == -1:
             end_time = start_time + interval
        # end_time = t
        # print(str(t)+' '+str(old_t))
        try:
            length_num = s.index('length') #
        except:
            continue
        byte = s[length_num+1]
        
        total_byte += int(byte)
        # print(str(t)+' '+str(end_time))
        if t - end_time <= 0:
            tmp_byte +=int(byte)
            # print(tmp_byte)
        else:
            print(str(t-start_time))
            tput = (((tmp_byte) * 8 )/1000000)/interval
            # print((str(old_t)+"\t"+str(tput)))
            # total_byte += tput
            f.write(str(end_time-start_time)+"\t"+str(tput)+"\n")
            end_time += interval
            # if old_t < 0:
            #     old_t +=60
            tmp_byte = int(byte)

tput_mean = ((total_byte*8)/(t-start_time))/1000000
tput_mean = round(tput_mean,2)
tput_mean = str(tput_mean)
print(str(total_byte/(t-start_time)/1000000))
# t = t+interval # every interval ms
f.close()

# file_to_numpy = np.loadtxt('test.txt', delimiter='\t')
# # print(file_to_numpy)
# time = file_to_numpy[:,0]
# tput = file_to_numpy[:,1]
# # tmp_tput_mean = np.mean(tput, axis=0)
# tmp_tput_mean = np.mean(tput, axis=0)

# tput_mean = int(tmp_tput_mean)
# # rtt_mean = int(tmp_rtt_mean)
# tput_mean = round(tput_mean, 2)
# rtt_mean = round(rtt_mean, 2)
# rtt_mean = rtt_mean/1000
# plot througput and cwnd
f2 = open('tmpPltFile', 'w')
f2.write( "reset;\n" )
f2.write( "set terminal unknown;\n" )
f2.write( "plot 'tmpDataFile' using 1:2;\n" ) 
f2.write( "set terminal gif font 'Arial' 12;\n" )
f2.write( "set output '"+filename+".png';\n" )
f2.write( "set term png size 1000, 400;\n" )
f2.write( "set title 'c2tcp' font 'Arial-Bold, 19';\n" )
f2.write( "set key top horizontal left;\n" )
f2.write( "set xlabel 'Time (Seconds)';\n" )
f2.write( "set ylabel 'Throghtput (Mbps) Avg:"+str(tput_mean)+";\n" )
# f2.write( "set y2label 'Congestion window';\n" )
f2.write( "set ytics nomirror;\n" )
f2.write( "set ytics textcolor rgb 'red';\n" )
# f2.write( "set y2tics nomirror;\n" )
# f2.write( "set y2tics textcolor rgb 'blue';\n" )
f2.write( "set xrange [0:];\n" )
# f2.write( "set y2range [0:];\n" )
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
f2.write( "plot 'tmpDataFile'  every ::1 using 1:2 ls 1 title 'Throughput' with linespoints,\\\n " )
# f2.write( " 'tmpDataFile' using 1:3 ls 2 title 'CWND (y2)' axes x1y2 with linespoints,\n " )
# f2.write( " 'tmpDataFile' using 1:4 ls 3 title 'RTT' axes x1y2 with linespoints,\n " )

cmd = "gnuplot tmpPltFile\n cp tmpDataFile probedata"
f2.close()
cmd_run(cmd)