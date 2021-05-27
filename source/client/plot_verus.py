#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib as mtp
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("client_file", help="e.g. client_60001.out")
parser.add_argument("server_file", help="Receiver.out")
parser.add_argument("-o", "--output", help="output directory")
args=parser.parse_args()

readfilename = args.client_file
tmp_file_name_tput = readfilename[:-15] + 'verus_tput.txt'
tmp_file_name_rtt = readfilename[:-15] + 'verus_rtt.txt'

f_tput = open(tmp_file_name_tput, 'w')
f_rtt = open(tmp_file_name_rtt, 'w')

path = args.output
if path == None:
	path, filename = os.path.split(args.server_file)

# plt.rcParams['text.latex.preamble']=[r'\boldmath']
# params = {'text.usetex' : True,
#           'font.size' : 20,
#           'legend.fontsize': 11,
#           'font.family' : 'lmodern',
#           'text.latex.unicode': True,
#           }
# plt.rcParams.update(params)

fig = plt.figure(figsize=(8,3), facecolor='w')

# processing the verus receiver log file to plot the throughput
trace = open (args.client_file, 'r')
throughput = []
bytes = 1492 #MTU of verus is 1450 + 42 UDP/IP overhead
startTime = trace.readline().strip().split(",")[0]

for time in trace:
	if (float(time.strip().split(",")[0]) - float(startTime)) <= 1.0:
		bytes += 1492
	else:
		tput = bytes*8/1000000.0
		throughput.append(tput)
		f_tput.write(str(startTime)+"\t"+str(tput)+"\n")
		bytes = 1492
		startTime = time.strip().split(",")[0]
		

tput_mean = sum(throughput) / len(throughput) 
throughput.insert(0, 0.0)



plt.plot(list(range(0,len(throughput)+0)), throughput, color='g', label='Verus', lw=2)


plt.xlabel('Time (s)')
plt.ylabel('Throughput (Mbps) avg.'+str(round(tput_mean, 1)))
plt.legend(loc='best',bbox_to_anchor=(1., 1.05), numpoints=1, fancybox=True, shadow=True, ncol=3)
plt.grid(True, which="both")
plt.savefig(path+'/throughput.png',
	    dpi=1000,           # Plot will be occupy a maximum of available space
        bbox_inches='tight')


### delay
def parse_delay_verus(filename):
	delays = []
	times1 = []

	delay_file = open(filename,"r")
	delay_file.seek(0)
	for line in delay_file:
		tokens = line.split(",")
		if float(tokens[1]) > 0.0 :
			delays.append((float(tokens[2])))
			times1.append((float(tokens[0])))
			f_rtt.write(str((float(tokens[0])))+"\t"+str((float(tokens[2])))+"\n")
	delay_file.close()
	rtt_mean = sum(delays) / len(delays) 
	return  delays, times1, rtt_mean

fig = plt.figure(figsize=(8,3), facecolor='w')
ax = plt.gca()

delays1, delayTimes1, rtt_mean = parse_delay_verus(args.server_file)
plt.plot(delayTimes1, delays1, label="Verus", color="g", lw=2)

plt.xlabel('Time (s)')
plt.ylabel('Delay (ms) avg.'+str(round(rtt_mean, 1)))
plt.legend(loc='upper right',bbox_to_anchor=(1., 1.05), numpoints=1, fancybox=True, shadow=True, ncol=4)
plt.grid(True, which="both")
plt.savefig(path+'/delay.png',
		dpi=1000,           # Plot will be occupy a maximum of available space
		bbox_inches='tight')
f_tput.close()
f_rtt.close()