#! /usr/bin/python
import sys

if(len(sys.argv)<5):
        print (sys.argv[0],"--filename --interval --write_file --stream")
        exit(0)

filename=sys.argv[1]
interval=float(sys.argv[2])
write_file=sys.argv[3]
stream = int(sys.argv[4])
fdRead=open(filename,"r")
protocol=""
duration=0
streamsCount=0
streamId=0
serverIp=""
clientIp=""
serverPort=0
clientPort=0
processCount=0
thrProcessCount=0
start_file=0
write_cwnd=[]
write_thr=[]
cwnd_write=0
thr_write=0

for line in fdRead:
#for line in sys.stdin: 
        #print line
        if("local" in line and "connected to" in line):
                param=line.split()
                serverIp=param[8]
                clientIp=param[3]
                serverPort=int(param[10])
                clientPort=int(param[5])
                #print serverIp,serverPort,clientIp,clientPort

        if("Starting Test" in line and start_file==0):
                processCount=0
                thrProcessCount=0
                param=line.split()
                protocol=param[3]
                streamsCount=int(param[4])
                duration=int(param[12])
                #print protocol,streamsCount,duration
                start_file=1

        if("mss" in line and "cwnd" in line and "totalretx" in line and processCount<=streamsCount*(duration/interval) and cwnd_write==0):
                #if(start_file==1):
                #       print "open file"
                #       fdWrite=open(serverIp+"_"+str(serverPort)+"_"+clientIp+"_"+str(clientPort)+"_"+str(dip_count[clientIp+serverIp+str(serverPort)])+".txt","w")
                #       start_file=0

                if(processCount==streamsCount*(duration/interval)):
                        #print "closing file"
                        #fdWrite.close()
                        continue

                param=line.split()
                write_str=str(streamId)+" "
                for i in range(0,len(param)):
                        write_str+=param[i]+" "

                #print write_str
                #fdWrite.write(write_str+"\n")
                write_cwnd.append(write_str)
                streamId+=1
                if(streamId==streamsCount):
                        streamId=0
                        cwnd_write=1
                processCount+=1

        if("sec" in line and "Bytes" in line and "bits/sec" in line and "SUM" not in line and "sender" not in line and "receiver" not in line and thrProcessCount<=streamsCount*(duration/interval) and thr_write==0):

                if(thrProcessCount==streamsCount*(duration/interval)):
                        continue

                param=line.split()
                thr=float(param[6])
                if(param[7]=="Mbits/sec"):
                        thr=thr
                if(param[7]=="Kbits/sec"):
                        thr=thr/1000
                if(param[7]=="bits/sec"):
                        thr=thr/1000000
                #print thr
                write_thr.append(thr)
                streamId+=1
                if(streamId==streamsCount):
                        streamId=0
                        thr_write=1
                thrProcessCount+=1

        if(start_file==1):
                if(cwnd_write==0 and thr_write==0 and thrProcessCount==0 and processCount==0):
                        #print "open file"
                        #fdWrite=open(serverIp+"_"+str(serverPort)+"_"+clientIp+"_"+str(clientPort)+"_"+str(dip_count[clientIp+serverIp+str(serverPort)])+".txt","w")
                        fdWrite=open(write_file,"w")

                if(cwnd_write==1 and thr_write==1):
                        cwnd_write=0
                        thr_write=0
                        #print "Writing into file",len(write_cwnd),len(write_thr)
                        for i in range(0,len(write_cwnd)):
                                fdWrite.write(write_cwnd[i]+" "+str(write_thr[i])+"\n")
                        write_cwnd=[]
                        write_thr=[]
                if(thrProcessCount==streamsCount*(duration/interval) and processCount<=streamsCount*(duration/interval)):
                        #print "closing file"

                        start_file=0
                        fdWrite.close()
                         


fdRead.close()