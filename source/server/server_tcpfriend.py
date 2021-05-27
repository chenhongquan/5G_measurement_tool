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

start_server=0
exp_count=0
filename=""
p=1
print('Delete all files in '+data_dir)
cmd = 'rm -rf '+data_dir+'/* '
os.system(cmd)    

print('1. exe_dir is ',exe_dir)
print('2. data_dir is ',data_dir)
print('3. result_dir is ',result_dir)
print('4. tmp_dir is ',tmp_dir)

if not os.path.exists(data_dir+'/'):
    os.makedirs(data_dir+'/')
if not os.path.exists(result_dir+'/'):
    os.makedirs(result_dir+'/')
if not os.path.exists(tmp_dir+'/'):
    os.makedirs(tmp_dir+'/')
if not os.path.exists(backup_dir+'/'):
    os.makedirs(backup_dir+'/')

if(len(sys.argv)<2):
    print ("Usage error: --#proto")
    exit()
# # server 2
www_name = 'mydata'
su = 'sudo'

proto=sys.argv[1]

tcp_cc_list = ['reno','cubic','bbr','vegas','westwood','exll','pcc']

if tcp_cc_list.count(proto) > 0 :
    # cmd = 'python3 server_tcp_cc.py'
    # os.system(cmd)

    print('change tcp_congestion_control to '+proto)
    cmd = su+' sysctl -w net.ipv4.tcp_congestion_control='+proto
    os.system(cmd)

    # if proto == 'bbr': cmd=
    # else:

    result = subprocess.check_output(cmd, shell=True)
    temp_proto = result.decode("utf-8") 
    proto=temp_proto.split()[2]
    print("protocol is "+proto)
    # exp_num = 0
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, 5000))
            while True:
                s.listen()
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr[0],addr[1])
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        else:
                            if("Can I start" in data.decode("utf-8")):
                                decode_data = data.decode("utf-8")
                                decode_data_group = decode_data.split()
                                print(decode_data_group)
                                ClientState = decode_data_group[4]
                                ClientIP = decode_data_group[5] # background|foreground
                                ClientStreams = int(decode_data_group[6])
                                exp_num=int(decode_data_group[7])
                                finish_num=int(decode_data_group[8])
                                x="%.0f"%time.time()
                                if(b"download" in data):
                                    filename="Server_"+ClientIP+"_"+str(PORT)+"_"+addr[0]+"_"+str(addr[1])+"_download_"+str(ClientStreams)+"_"+str(ClientState)+"_"+str(x)+"_"+str(exp_num)+".txt"
                                    print(filename)
                                if(b"upload" in data):
                                    filename="Server_"+ClientIP+"_"+str(PORT)+"_"+addr[0]+"_"+str(addr[1])+"_upload_"+str(ClientStreams)+"_"+str(ClientState)+"_"+str(x)+"_"+str(exp_num)+".txt"
                                    print(filename)
                                # TODO : run tcp_probe (sudo cat /proc/net/tcpprobe > data 2>&1)
                                tcp_probe_filename = "tcpprobe_"+ClientIP+"_"+str(PORT)+"_"+addr[0]+"_"+str(addr[1])+"_download_"+str(ClientStreams)+"_"+str(ClientState)+"_"+str(x)+"_"+str(exp_num)+".txt"
                                cmd_tcp_probe = su+" cat /proc/net/tcpprobe > "+data_dir+'/'+tcp_probe_filename+" 2>&1"
                                subprocess.Popen(cmd_tcp_probe,shell=True)
                                cmd="iperf3 -s -p "+str(PORT)+" -V -i "+str(interval)+" -f m > "+tmp_dir+'/'+filename  # run iperf3
                                print ("cmd is:",cmd) 
                                subprocess.Popen(cmd,shell=True)
                                conn.sendall(b"yes")
                                #res=p.communicate()
                                #print (res)
                                print (data,"\tLaunched the command")
                            if("Done" in data.decode("utf-8")):
                                print ("Clinet is done with iperf",data)
                                exp_count+=1
                                cmd=su+" kill $(ps aux | grep iperf3 | awk {'print $2'} )"
                                print ("cmd is:",cmd)
                                os.system(cmd)
                                cmd_2=su+" kill $(ps aux | grep tcpprobe | awk {'print $2'} )"
                                print ("cmd is:",cmd_2)
                                os.system(su+' killall -9 cat')
                                os.system(cmd_2)
                                #create the parsed output
                                write_file="p"+filename
                                cmd="./server_parser.py "+tmp_dir+'/'+filename+" "+str(interval)+" "+data_dir+'/'+write_file
                                print ("cmd is:",cmd)
                                os.system(cmd)
                                #break
                                #exit()    
                                if finish_num==1:
                                    print('finish_num is ', finish_num)
                                    p = 0
                            else:
                                print(data)    
                if p==0:
                    print('p==0')
                    break
                            
    except KeyboardInterrupt:
        pass        

    # run = exp_count + 1
    print('\n Stop Here! Total experiment number: '+ str(exp_count))
    print('Working on plot and index.html files.... wait....\n')
    # sleep(10)
    # exp_count=2
    # run=2

    # draw with iperf3 and tcpprobe data
    cmd = 'python3 ' + exe_dir+'/' + 'plot_control.py '+str(duration)+' '+ClientState+' '+str(ClientStreams)+' '+str(exp_count)+' '+str(proto)
    print("cmd is "+cmd)
    os.system(cmd)


else:
    # Sprout
    if proto == 'sprout':
        # run server
        # cmd = 'python3 run_sprout.py'
        # os.system(cmd)
        x="%.0f"%time.time()
        rtt_filename="sprout_rtt_"+str(today)+"_"+str(x)+".txt"
        tput_filename="sprout_tput_"+str(today)+"_"+str(x)+".txt"

        cc_repo = path.join(base_dir, 'sprout')
        model = path.join(cc_repo, 'src', 'examples', 'sprout.model')
        src = path.join(cc_repo, 'src', 'examples', 'sproutbt2')
        # sproutbt2
        tmp_file_name = data_dir+'/'+rtt_filename
        rtt_command = src+' 2>&1 | tee ' +tmp_file_name
        print(rtt_command)
        p2 = subprocess.Popen(rtt_command, stderr = subprocess.PIPE, shell=True) 
        s_time = "%.0f"%time.time()
        time.sleep(10)
        tput_cmd = su+' tcpdump -n udp -v > '+data_dir+'/'+tput_filename
        p1 = subprocess.Popen(tput_cmd, stderr = subprocess.PIPE, shell=True) 
        c_time = "%.0f"%time.time()
        while(1):
            if int(c_time)-int(s_time) > duration+30 : # 15s: initial booting time 
                os.system(su+' killall -9 tcpdump')
                os.system(su+' killall -9 cat')
                os.system(su+' killall -9 sproutbt2')
                # tar_cmp = 'tar -cvf '+'~/sprout.tar.gz '+data_dir+'/*'
                # os.system(tar_cmp)
                plot_file = '../client/new_plot_from_udp.py'
                new_result_dir = "/"+www_name+"/www/html/tmp/"+str(server_name)+"_"+str(proto)+"_"+str(today)+"_"+str(x)
                cmd = 'mkdir ' + new_result_dir
                os.system(cmd)
                dir_list = os.listdir(data_dir)
                # dir = dir_list[0]
                for dir in dir_list:
                    if dir.find('tput') >= 0:
                        tput = dir
                    if dir.find('rtt')>=0:
                        rtt = dir

                # python3 new_plot_from_udp.py readfilename filename(wrt) CCA_name
                cmd = 'python3 '+plot_file+' '+data_dir+'/'+tput+' '+data_dir+'/'+rtt+' '+data_dir+'/sprout_figure'+' '+'sprout'
                print(cmd)
                os.system(cmd)

                cmd = 'mv '+data_dir+'/* '+ new_result_dir 
                os.system(cmd)

                break
            else:
                c_time = "%.0f"%time.time()
    # Verus
    elif proto == 'verus':
        # # run server
        # cmd = 'python3 run_verus.py'
        # os.system(cmd)
        x="%.0f"%time.time()
        result_dir_name="verus_"+str(today)+"_"+str(x)

        # ./verus_server -name test -p 60001 -t 30
        cc_repo = path.join(base_dir, 'verus')
        src = path.join(cc_repo, 'src', 'verus_server')
        verus_result_dir = path.join(src, result_dir_name)
        new_verus_result_dir = path.join(data_dir, result_dir_name)

        cmd = 'mkdir ' + new_verus_result_dir
        os.system(cmd)

        tput_filename="verus_tput_"+str(today)+"_"+str(x)+".txt"
        rtt_filename="verus_rtt_"+str(today)+"_"+str(x)+".txt"

        # rtt_cmd = src+' > '+data_dir+'/'+rtt_filename
        tput_cmd = su+' tcpdump -n udp -v > '+data_dir+'/'+result_dir_name+'/'+tput_filename
        print(tput_cmd)
        p1 = subprocess.Popen(tput_cmd, stderr = subprocess.PIPE, shell=True) 

        s_time = "%.0f"%time.time()
        # verus_server result: Losses.out Receiver.out Verus.out
        rtt_command = src+' -name ' +result_dir_name +' -p 9001 -t '+ str(duration)
        p1 = subprocess.Popen(rtt_command, stderr = subprocess.PIPE, shell=True) 

        duration_1 = int(duration) + 5
        time.sleep(duration_1)

        c_time = "%.0f"%time.time()
        while(1):
            if int(c_time)-int(s_time) > duration : # 15s: initial booting time 
                os.system(su+' killall -9 tcpdump')
                # os.system(tar_cmp)
                break
            else:
                c_time = "%.0f"%time.time()

        time.sleep(15)
        cmd = 'cp ' +result_dir_name+'/* '+new_verus_result_dir
        os.system(cmd)

        verus_plot_file = '../client/plot_verus.py'
        cmd = 'python3 '+verus_plot_file+' '+new_verus_result_dir+'/Receiver.out  -o '+new_verus_result_dir
        os.system(cmd)

        plot_file = '../client/new_plot_from_udp.py'
        dir_list = os.listdir(new_verus_result_dir)
        # dir = dir_list[0]
        print(dir_list)
        for dir in dir_list:
            if dir.find('verus_tput_')>= 0:
                tput = dir
            if dir.find('Receiver.out')>=0:
                rtt = dir

        # python3 new_plot_from_udp.py readfilename filename(wrt) CCA_name
        cmd = 'python3 '+plot_file+' '+new_verus_result_dir+'/'+tput+' '+new_verus_result_dir+'/'+rtt+' '+new_verus_result_dir+'/verus_figure '+proto
        print(cmd)
        os.system(cmd)

        new_result_dir = "/"+www_name+"/www/html/tmp/"+str(server_name)+"_"+str(proto)+"_"+str(today)+"_"+str(x)
        cmd = 'mkdir ' + new_result_dir
        os.system(cmd)

        cmd = 'mv '+new_verus_result_dir+'/* '+ new_result_dir 
        os.system(cmd)    


    #COPA
    elif proto == 'copa':
        # # run server
        # cmd = 'python3 run_copa.py'
        # os.system(cmd)
        x="%.0f"%time.time()
        tput_filename="copa_tput_"+str(today)+"_"+str(x)+".txt"
        rtt_filename="copa_rtt_"+str(today)+"_"+str(x)+".txt"

        # rtt_cmd = src+' > '+data_dir+'/'+rtt_filename
        tput_cmd = su+' tcpdump -n udp -v > '+data_dir+'/'+tput_filename
        p1 = subprocess.Popen(tput_cmd, stderr = subprocess.PIPE, shell=True) 
        # os.system(tput_cmd)
        s_time = "%.0f"%time.time()
        rtt_command = '~/genericCC/sender serverip='+HOST+' offduration=0 onduration=1000000 cctype=markovian delta_conf=do_ss:auto:0.5 traffic_params=deterministic > '+data_dir+'/'+rtt_filename
        p2 = subprocess.Popen(rtt_command, stderr = subprocess.PIPE, shell=True) 
        # os.system(tput_cmd)
        # returned_value = os.system(rtt_command)
        # print('returned value:', returned_value)
        c_time = "%.0f"%time.time()
        while(1):
            if int(c_time)-int(s_time) > duration+5 : # 15s: initial booting time 
                os.system(su+' killall -9 sender')
                os.system(su+' killall -9 tcpdump')
                # tar_cmp = 'tar -cvf '+'~/copa.tar.gz '+data_dir+'/*'
                # os.system(tar_cmp)
                time.sleep(10)

                plot_file = '../client/new_plot_from_udp.py'
                dir_list = os.listdir(data_dir)
                # dir = dir_list[0]
                print(dir_list)
                for dir in dir_list:
                    if dir.find('tput')>= 0:
                        tput = dir
                    if dir.find('rtt')>=0:
                        rtt = dir

                # python3 new_plot_from_udp.py readfilename filename(wrt) CCA_name
                cmd = 'python3 '+plot_file+' '+data_dir+'/'+tput+' '+data_dir+'/'+rtt+' '+data_dir+'/copa_figure '+proto
                print(cmd)
                os.system(cmd)

                new_result_dir = "/"+www_name+"/www/html/tmp/"+str(server_name)+"_"+str(proto)+"_"+str(today)+"_"+str(x)
                cmd = 'mkdir ' + new_result_dir
                os.system(cmd)

                cmd = 'mv '+data_dir+'/* '+ new_result_dir 
                os.system(cmd)    
                # cmd = 'rm '+data_dir+'/* '
                # os.system(cmd)    
                break
            else:
                c_time = "%.0f"%time.time()

        # cmd = 'rm -rf ../../data/*'
        # os.system(cmd)
    #C2TCP
    elif proto == 'c2tcp':
        # # run server
        # cmd = 'python3 run_c2tcp.py'
        # os.system(cmd)
        cmd = su+' sysctl -w net.ipv4.tcp_congestion_control=cubic'
        os.system(cmd)
        cmd = su+' sysctl -w net.ipv4.tcp_c2tcp_enable=1'
        os.system(cmd)
        x="%.0f"%time.time()
        tput_filename="c2tcp_"+str(today)+"_"+str(x)+".txt"

        tcp_probe_filename = "tcpprobe_0.0.0.0_00000_"+str(HOST)+"_"+str(PORT)+"_download_1_foreground_"+str(x)+"_0.txt"
        cmd_tcp_probe = su+" cat /proc/net/tcpprobe > "+data_dir+'/'+tcp_probe_filename+" 2>&1"
        p0 = subprocess.Popen(cmd_tcp_probe,shell=True)

        # rtt_cmd = src+' > '+data_dir+'/'+rtt_filename
        tput_cmd = su+' tcpdump -n -v > '+data_dir+'/'+tput_filename
        p1 = subprocess.Popen(tput_cmd, stderr = subprocess.PIPE, shell=True) 

        rtt_command = su+' ~/c2tcp/server '+str(PORT)+' 0 200 1000'
        p2 = subprocess.Popen(rtt_command, stderr = subprocess.PIPE, shell=True) 
        print('duration is '+ str(duration))
        print('before_duration '+ str(duration))
        print(datetime.datetime.now())

        time.sleep(duration)
        print('after_duration '+ str(duration))
        print(datetime.datetime.now())
        os.system(su+' killall -9 server')
        os.system(su+' killall -9 tcpdump')
        os.system(su+' killall -9 cat')

        time.sleep(40)
        
        plot_file = '../client/new_plot_from_tcp.py'
        dir_list = os.listdir(data_dir)
        # dir = dir_list[0]
        tcpprobe = ''
        for dir in dir_list:
            if dir.find('c2tcp_2020') >= 0 and dir.find('Cell') < 0 :
                tput = dir
            elif  dir.find('tcpprobe_') >= 0 and dir.find('png') < 0 :
                tcpprobe = dir

        # cmd = 'python3 '+plot_file+' '+new_result_dir+'/'+dir+' '+ new_result_dir+'/figire'
        # os.system(cmd)

        # python3 new_plot_from_udp.py readfilename filename(wrt) CCA_name
        cmd = 'python3 '+plot_file+' '+data_dir+'/'+tput+' '+data_dir+'/'+tcpprobe+' '+data_dir+'/ '+proto
        print(cmd)
        os.system(cmd)

        if tcpprobe !='':
            print('python3 plot_tcp_other.py '+str(duration)+' foreground 1 1 '+str(proto))
            os.system('python3 plot_tcp_other.py '+str(duration)+' foreground 1 1 '+str(proto))
            os.system('mv ../../plot/* '+data_dir)
        new_result_dir = "/"+www_name+"/www/html/tmp/"+str(server_name)+"_"+str(proto)+"_"+str(today)+"_"+str(x)
        cmd = 'mkdir ' + new_result_dir
        os.system(cmd)

        cmd = 'mv '+data_dir+'/* '+ new_result_dir 
        os.system(cmd)    
        # cmd = 'rm '+data_dir+'/* '
        # os.system(cmd)    
        cmd = su+' sysctl -w net.ipv4.tcp_c2tcp_enable=0'
        os.system(cmd)

        # while(1):
        #     print(int(c_time)-int(s_time))
        #     if int(c_time)-int(s_time) > duration + :
        #         os.system(su+' killall -9 server')
        #         os.system(su+' killall -9 tcpdump')
        #         os.system(su+' killall -9 cat')

        #         time.sleep(10)
                
        #         plot_file = '../client/new_plot_from_tcp.py'
        #         dir_list = os.listdir(data_dir)
        #         # dir = dir_list[0]
        #         tcpprobe = ''
        #         for dir in dir_list:
        #             if dir.find('c2tcp_2020') >= 0 and dir.find('Cell') < 0 :
        #                 tput = dir
        #             elif  dir.find('tcpprobe_') >= 0 and dir.find('png') < 0 :
        #                 tcpprobe = dir

        #         # cmd = 'python3 '+plot_file+' '+new_result_dir+'/'+dir+' '+ new_result_dir+'/figire'
        #         # os.system(cmd)

        #         # python3 new_plot_from_udp.py readfilename filename(wrt) CCA_name
        #         cmd = 'python3 '+plot_file+' '+data_dir+'/'+tput+' '+data_dir+'/'+tcpprobe+' '+data_dir+'/ '+proto
        #         print(cmd)
        #         os.system(cmd)

        #         if tcpprobe !='':
        #             print('python3 plot_tcp_other.py '+str(duration)+' foreground 1 1 '+str(proto))
        #             os.system('python3 plot_tcp_other.py '+str(duration)+' foreground 1 1 '+str(proto))
        #             os.system('mv ../../plot/* '+data_dir)
        #         new_result_dir = "/"+www_name+"/www/html/tmp/"+str(server_name)+"_"+str(proto)+"_"+str(today)+"_"+str(x)
        #         cmd = 'mkdir ' + new_result_dir
        #         os.system(cmd)

        #         cmd = 'mv '+data_dir+'/* '+ new_result_dir 
        #         os.system(cmd)    
        #         # cmd = 'rm '+data_dir+'/* '
        #         # os.system(cmd)    
        #         cmd = su+' sysctl -w net.ipv4.tcp_c2tcp_enable=0'
        #         os.system(cmd)
        #         break
        #     else:
        #         c_time = "%.0f"%time.time()


    # # server 1
    if server_name == 'server_1':
        tar_cmp = 'tar -cvf '+'~/backup1.tar.gz '+new_result_dir+'/*'
        os.system(tar_cmp)

        cp_cmp = 'cp ~/backup1.tar.gz /mydata/www/html/tmp/'
        os.system(cp_cmp)

    # # server 2
    if server_name == 'server_2':
        tar_cmp = 'tar -cvf '+'~/backup2.tar.gz '+new_result_dir+'/*'
        os.system(tar_cmp)

        scp_cmd = id_rsa+' ~/backup2.tar.gz user@000.000.000.000:/mydata/www/html/tmp/'
        print(scp_cmd)
        os.system(scp_cmd)
    # # server 3
    elif server_name == 'server_3':
        tar_cmp = 'tar -cvf '+'~/backup3.tar.gz '+new_result_dir+'/*'
        os.system(tar_cmp)

        scp_cmd = id_rsa+' ~/backup3.tar.gz user@000.000.000.000:/mydata/www/html/tmp/'
        print(scp_cmd)
        os.system(scp_cmd)



if multi == True and server_name == 'server_1':
    time.sleep(20)

    backup_tmp_folder_name_2 = '/mydata/www/html/tmp/' + server_name+'-'+str(today)+'-'+ str(x)+'-'+proto

    cmd = 'mkdir ' + backup_tmp_folder_name_2
    os.system(cmd)
    print(tcp_cc_list.count(proto))
    if tcp_cc_list.count(proto) <= 0 :
        tar_cmp = 'tar -xvf '+'/mydata/www/html/tmp/backup1.tar.gz -C '+backup_tmp_folder_name_2+' --strip-components=4'
    else:
        tar_cmp = 'tar -xvf '+'/mydata/www/html/tmp/backup1.tar.gz -C '+backup_tmp_folder_name_2+' --strip-components=3'
    print(tar_cmp)
    os.system(tar_cmp)

    # if tcp_cc_list.count(proto) <= 0 :
    #     tar_cmp = 'tar -xvf '+'/mydata/www/html/tmp/backup2.tar.gz -C '+backup_tmp_folder_name_2+' --strip-components=4'
    # else:
    #     tar_cmp = 'tar -xvf '+'/mydata/www/html/tmp/backup2.tar.gz -C '+backup_tmp_folder_name_2+' --strip-components=3'
    tar_cmp = 'tar -xvf '+'/mydata/www/html/tmp/backup2.tar.gz -C '+backup_tmp_folder_name_2+' --strip-components=3'
    print(tar_cmp)
    os.system(tar_cmp)
    
    # if tcp_cc_list.count(proto) <= 0 :
    #     tar_cmp = 'tar -xvf '+'/mydata/www/html/tmp/backup3.tar.gz -C '+backup_tmp_folder_name_2+' --strip-components=4'
    # else:
    #     tar_cmp = 'tar -xvf '+'/mydata/www/html/tmp/backup3.tar.gz -C '+backup_tmp_folder_name_2+' --strip-components=3'
    tar_cmp = 'tar -xvf '+'/mydata/www/html/tmp/backup3.tar.gz -C '+backup_tmp_folder_name_2+' --strip-components=3'
    print(tar_cmp)
    os.system(tar_cmp)

    cmd = 'rm /mydata/www/html/tmp/backup*'
    print(cmd)
    os.system(cmd)

    if proto == 'c2tcp' or proto == 'verus':
        cmd = 'rm -rf /mydata/www/html/tmp/server_1_'+str(proto)+'_*'
        print(cmd)
        os.system(cmd)
