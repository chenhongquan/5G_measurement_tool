import os 
import time
import sys
import sqlite3 as lite
import glob
import subprocess 
from yattag import Doc
from threading import Thread
import numpy as np
# import strftime from time
from datetime import datetime
import sys
sys.path.append("../config/")
from setup import * 

if(len(sys.argv)<3):
	print ("Usage error: --tput_file --rtt_file --output")
	exit()

readfilename=sys.argv[1]
rtt_readfilename=sys.argv[2] 
filename=sys.argv[3]
print(readfilename)
S_addr = str(HOST)+'.'+str(60001)
# #filename = '5g-1/figure_sprout_1'
# # readfilename = '5g-1/sprout_tput_2020-08-05_1596668229.txt'
# #filename = '5g-3/figure_sprout_3'
# #readfilename = '5g-3/sprout_tput_2020-08-05_1596668645.txt'
# filename = '5g-4/figure_sprout_4'
# readfilename = '5g-4/sprout_tput_2020-08-05_1596668748.txt'

f = open(readfilename[:-4]+'_p.txt', 'w')
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
for line in lines:
    s = line.split()
    # print(s[2]+' and '+s[4])
    if len(s) >= 8 and s[2] == S_addr: #and s[4].find('174.248.152.70')>=0:
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
        byte = s[7]
        if byte == 'length':
            byte = s[8]
            # print(bit)
        
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

# print(lines[0].split())
# l = lines[0].split()
# t=0
# # bit = 0
# old_t = 0
# tmp_bit = 0
# total_bit = 0
# # init_t_hh= l[0].split(':')[0]
# # init_t_mm= l[0].split(':')[1]
# # init_t_ss= l[0].split(':')[2].split('.')[0]
# # init_t_nano= l[0].split(':')[2].split('.')[1]
# init_t = get_sec(l[0])
# old_t = init_t
# print(init_t)
# for line in lines:
#     s = line.split()
#     # print(s[2]+' and '+s[4])
#     if len(s) < 8:
#         break
#     if s[2] == S_addr: #and s[4].find('174.248.152.70')>=0:
#     #if s[2].find('174.248.152.70')>=0:
#         # t = s[0]
#         # print('print lines is here ', s)
#         t = get_sec(s[0])
#         # print(str(t)+' '+str(old_t))
#         bit = s[7]
#         if bit == 'length':
#             bit = s[8]
#             # print(bit)
        
#         bit = int(bit)
#         # print(int(t))
#         # print(old_t)
#         # if old_t == 0:
#         #     init_t = int(t)
#         # print("int(t) is ",int(t))
#         # print("int(t) is ",int(t)-init_t)
#         # print("old_t is ",old_t)
#         if t - old_t <= 1:
#             tmp_bit +=bit
#             # print(tmp_bit)
#         else:
#             print(t)
#             tput = (( tmp_bit) * 8 )/1000000
#             # print((str(old_t)+"\t"+str(tput)))
#             total_bit += tput
#             f.write(str(old_t-init_t)+"\t"+str(tput)+"\n")
#             old_t = t
#             # if old_t < 0:
#             #     old_t +=60
#             tmp_bit = 0
            
#     print(str(total_bit/60))
#     # t = t+interval # every interval ms
# f.close()

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
f2.write( "set title 'Sprout' font 'Arial-Bold, 19';\n" )
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
f2.write( "plot 'tmpDataFile'  every ::1  using 1:2 ls 1 title 'Throughput' with linespoints,\\\n " )
# f2.write( " 'tmpDataFile' using 1:3 ls 2 title 'CWND (y2)' axes x1y2 with linespoints,\n " )
# f2.write( " 'tmpDataFile' using 1:4 ls 3 title 'RTT' axes x1y2 with linespoints,\n " )

cmd = "gnuplot tmpPltFile\n cp tmpDataFile probedata"
f2.close()
cmd_run(cmd)
