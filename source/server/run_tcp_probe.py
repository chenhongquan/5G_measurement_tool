#!/usr/bin/env python3
import socket
import os, sys, time
import subprocess
import _thread as thread
from yattag import Doc
sys.path.append("../config/")
from setup import * 
from os import path
from datetime import date
import datetime
import numpy as np 

start_server=0
exp_count=0
filename=""
p=1

# # server 2
www_name = 'mydata'
su = 'sudo'

proto=sys.argv[1]

tcp_cc_list = ['cubic','bbr','exll','pcc']

if tcp_cc_list.count(proto) > 0 :
    # cmd = 'python3 server_tcp_cc.py'
    # os.system(cmd)

    print('change tcp_congestion_control to '+proto)
    cmd = su+' sysctl -w net.ipv4.tcp_congestion_control='+proto
    os.system(cmd)
    cmd = su+' sysctl -w net.ipv4.tcp_c2tcp_enable=0'
    os.system(cmd)

    # TODO : run tcp_probe (sudo cat /proc/net/tcpprobe > data 2>&1)
    x="%.0f"%time.time()
    tcp_probe_filename = "tcpprobe_for_web_"+str(x)+".txt"
    cmd_tcp_probe = su+" cat /proc/net/tcpprobe > "+data_dir+'/'+tcp_probe_filename+" 2>&1"
    subprocess.Popen(cmd_tcp_probe,shell=True)
                                
    time.sleep(120)                            
    # kill tcp_probe
    cmd_2=su+" kill $(ps aux | grep tcpprobe | awk {'print $2'} )"
    print ("cmd is:",cmd_2)
    os.system(su+' killall -9 cat')
    os.system(cmd_2)


print("filename is", data_dir+'/'+tcp_probe_filename)
i = data_dir+'/'+tcp_probe_filename

filename = i[len_dir:-4] # ../../data/
# filename_fig = result_dir+'/'+filename+"_tcpprbe_"+str(exp_num)
rtt_file=filename+'.log'
temp_x = filename.split('_')


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
# 128.110.153.174:443
for line in lines[1:-1]:
    s = line.split()
    print(s)
    if t == 0:
        init_t = float(s[0])
    t = float(s[0])
    rtt = int(s[9])/1000
    ca_name = s[26]
    f_rtt.write(str(t-init_t)+"\t"+str(rtt)+"\t"+str(s[6])+"\t"+str(s[8])+"\t"+str(s[10])+"\t"+str(s[23])+"\n") # time rtt cwnd snd_wnd rcv_wnd mss
    f.write(str(t)+"\t"+str(s[6])+"\t"+str(s[7])+"\t"+str(s[8])+"\t"+str(rtt)+"\t"+str(s[10])+"\t"+str(s[11])+"\t"+str(s[12])+"\t"+str(s[13])+"\t"+str(s[14])+"\t"+str(s[15])+"\t"+str(s[16])+"\t"+str(s[17])+"\t"+str(s[18])+"\t"+str(s[19])+"\t"+str(s[20])+"\t"+str(s[21])+"\t"+str(s[22])+"\t"+str(s[23])+"\t"+str(s[24])+"\t"+str(s[25])+"\n")
f.close()
f_rtt.close()

print(filename)
ClientState = 'web'
ca_name = proto
print(result_dir+"/"+filename+"_web_total_tp2.png")

# plot througput and cwnd
f7 = open('tmpPltFile', 'w')
f7.write( "reset;\n" )
f7.write( "set terminal gif font 'Arial' 12;\n" )
f7.write( "set output '"+result_dir+"/"+filename+"_web_total_tp1.png';\n" )
f7.write( "set term png size 1000, 600;\n" )
f7.write( "set multiplot layout 2, 1 title '"+str(ca_name)+"' font 'Arial-Bold, 19';\n" )
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
f7.write( "set xrange [0:"+str(duration)+"];\n" )
f7.write( "set y2range [0:];\n" )
f7.write( "set yrange [0:];\n" )
f7.write( "plot 'tmpDataFile' using 1:2 ls 2 title 'CWND' with line,\\\n " )
f7.write( "  'tmpDataFile' using 1:3 ls 3 title 'ssth' axes x1y2 with line,\n " )
f7.write( "set ylabel 'RTT (ms)';\n" )
f7.write( "set ytics textcolor rgb 'forest-green';\n" )
f7.write( "set y2label '"+str(proto)+"';\n" )
f7.write( "set y2tics nomirror;\n" )
f7.write( "set y2tics textcolor rgb 'blue';\n" )
f7.write( "set ytics textcolor rgb 'black';\n" )
f7.write( "set xrange [0:"+str(duration)+"];\n" )
f7.write( "set y2range [0:];\n" )
f7.write( "set yrange [0:];\n" )
f7.write( "plot  'tmpDataFile' using 1:5 ls 3 title 'rtt' with line,\n " )

cmd = "gnuplot tmpPltFile\n cp tmpDataFile probedata"
f.close()
f7.close()
cmd_run(cmd)


f3 = open('tmpPltFile', 'w')
f3.write( "reset;\n" )
f3.write( "set terminal gif font 'Arial' 12;\n" )
f3.write( "set output '"+result_dir+"/"+filename+"_web_total_tp2.png';\n" )
f3.write( "set term png size 1000, 600;\n" )
f3.write( "set multiplot layout 3, 1 title '"+str(ca_name)+"' font 'Arial-Bold, 19';\n" )
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
f3.write( "set xrange [0:"+str(duration)+"];\n" )
f3.write( "set y2range [0:];\n" )
f3.write( "set yrange [0:];\n" )
f3.write( "plot 'tmpDataFile' using 1:4 ls 1 title 'snd wnd' with line,\\\n " )
f3.write( "  'tmpDataFile' using 1:6 ls 2 title 'rcv wnd' with line,\n " )
f3.write( "set ylabel 'bytes acked';\n" )
f3.write( "set ytics textcolor rgb 'forest-green';\n" )
f3.write( "set ytics nomirror;\n" )
f3.write( "set y2label 'mss';\n" )
f3.write( "set y2tics textcolor rgb 'black';\n" )
f3.write( "set y2tics nomirror;\n" )
f3.write( "set xrange [0:"+str(duration)+"];\n" )
f3.write( "set y2range [0:];\n" )
f3.write( "set yrange [0:];\n" )
f3.write( "plot  'tmpDataFile' using 1:18 ls 3 title 'bytes acked' with line,\\\n " )
f3.write( "  'tmpDataFile' using 1:19 ls 2 title 'mss' with line,\n " )
f3.write( "set ylabel 'Inflight Pkts';\n" )
f3.write( "set ytics textcolor rgb 'forest-green';\n" ) 
f3.write( "set ytics nomirror;\n" )
f3.write( "set y2label 'Lost Pks';\n" )
f3.write( "set y2tics textcolor rgb 'black';\n" )
f3.write( "set y2tics nomirror;\n" )
# f3.write( "set y2range [0:100];\n" )
f3.write( "set xrange [0:"+str(duration)+"];\n" )
f3.write( "set y2range [0:];\n" )
f3.write( "set yrange [0:];\n" )
f3.write( "plot  'tmpDataFile' using 1:20 ls 3 title 'inflight pkts' with line,\\\n " )
f3.write( "  'tmpDataFile' using 1:21 ls 1 lw 3 title 'lost pks' axes x1y2 with line,\n " )

cmd = "gnuplot tmpPltFile\n cp tmpDataFile probedata"
f.close()
f3.close()
cmd_run(cmd)      

# # index.html
# doc, tag, text = Doc().tagtext()
# # TODO: write html file 
# indexfilename = result_dir+'/'+"index.html"
# with tag('html'):
#     with tag('head'):
#         with tag('script', ('src','fillData.js')):
#             text("")															
#     with tag('body', ('onload','fillData()'), id = 'Results'):
#         with tag('h1'):
#             text("Experiment No. = TEST ") # + str(exp_count_fixed))
#         with tag('h2'):
#             text("Setup")
#         with tag('table'):
#             with tag('tr'):
#                 with tag('td'):
#                     text('Item')
#                 with tag('td'):
#                     text('Value')
#             with tag('tr'):
#                 with tag('td'):
#                     text("Congestion control")
#                 with tag('td'):
#                     text(proto)
#         with tag('table'):			
#             with tag('tr'):		
#                 with tag('td'):
#                     with tag('h3'):
#                         with tag('p'):
#                             text('Web cwnd&RTT Graph')
#                         with tag('div', id='photo-container'):
#                             doc.stag('img', src=filename+"_web_total_tp1.png", klass="photo")					
#         with tag('table'):			
#             with tag('tr'):		
#                 with tag('td'):
#                     with tag('h3'):
#                         with tag('p'):
#                             text('Web rwnd&packet loss Graph')
#                         with tag('div', id='photo-container'):
#                             doc.stag('img', src=filename+"_web_total_tp2.png", klass="photo")					

    
# with open(indexfilename, 'w') as fout:
#     fout.write(doc.getvalue())
# fout.close()


save_folder = "web_test_"+proto+"_"+str(x)

cmd = "mkdir /mydata/www/html/tmp/"+save_folder
cmd_run(cmd)
cmd = "mv ~/5G_measurement_tool/data/* /mydata/www/html/tmp/"+save_folder
cmd_run(cmd) 
cmd = "mv ~/5G_measurement_tool/plot/* /mydata/www/html/tmp/"+save_folder
cmd_run(cmd) 