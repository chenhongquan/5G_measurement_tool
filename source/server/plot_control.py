import os
import time
import sys
from yattag import Doc
import sys
sys.path.append("../config/")
from setup import * 
import glob
from datetime import date

# work done by syslabshare1

# plot function starting 
# This is for plotting the results of iperf3

# TODO: setup configure file 
duration = int(sys.argv[1])	# str(duration)
ClientState = sys.argv[2]	# proto -> ClientState
ClientStreams = int(sys.argv[3])
exp_count = int(sys.argv[4])
proto = sys.argv[5]
# Temporary
descrpition = 'This is conducted with '+str(proto)+', in '+str(duration)+'s, '+ClientState+', '+str(ClientStreams)+' flows, '+str(exp_count)+' times'

# draw with iperf3 data
print('python3 ' + exe_dir+'/' + 'plot.py '+str(duration)+' '+ClientState+' '+str(ClientStreams)+' '+str(exp_count)+' '+str(proto))
os.system('python3 ' + exe_dir+'/' + 'plot.py '+str(duration)+' '+ClientState+' '+str(ClientStreams)+' '+str(exp_count)+' '+str(proto))

# draw with tcpprobe data
print('python3 ' + exe_dir+'/' + 'plot_tcp_other.py '+str(duration)+' '+ClientState+' '+str(ClientStreams)+' '+str(exp_count)+' '+str(proto))
os.system('python3 ' + exe_dir+'/' + 'plot_tcp_other.py '+str(duration)+' '+ClientState+' '+str(ClientStreams)+' '+str(exp_count)+' '+str(proto))
# if proto == 'bbr':
#     os.system('python3 ' + exe_dir+'/' + 'plot_tcp_bbr.py '+str(duration)+' '+ClientState+' '+str(ClientStreams)+' '+str(exp_count)+' '+str(proto))
# else:
#     os.system('python3 ' + exe_dir+'/' + 'plot_tcp_other.py '+str(duration)+' '+ClientState+' '+str(ClientStreams)+' '+str(exp_count)+' '+str(proto))


filename = ''
server_file_list = []
client_file_list = []
probe_file_list = []

y = glob.glob(data_dir+'/'+'*.txt') # after checking, enable this
for n in y:
    if n.find("pServer")>=0:
        # filename=filename+"_server_"+str(exp_count)
        server_file_list.append(n[len_dir:])
        # server_file_list.append(n[33:])
    elif n.find("pClient")>=0:
        # filename=filename+"_client_"+str(exp_count)
        client_file_list.append(n[len_dir:])
        # client_file_list.append(n[33:])
    elif n.find("tcpprobe")>=0:
        # filename=filename+"_client_"+str(exp_count)
        probe_file_list.append(n[len_dir:])
        # client_file_list.append(n[33:])

server_file_list.sort()
client_file_list.sort()
# plot file name: 
# result_dir+'/'+s_name+"_cwnd.png
# result_dir+'/'+s_name+"_rtt.png
# result_dir+'/'+s_name+"_ssth.png
# result_dir+'/'+s_name+"_rsrp.png
for i in range(exp_count):
    s_name = server_file_list[i]
    # c_name = client_file_list[i]

    tmp_a = s_name.split('_')[9]
    print(s_name)
    exp_count_fixed = int(tmp_a[:-4])
    print("Here, working on for index_"+str(exp_count_fixed)+".html")
    print("s_name is "+s_name)
    h=0
    for h in range(exp_count):
        if client_file_list[h].find('_'+str(exp_count_fixed)+'.txt')>=0:
            c_name = client_file_list[h]
            print("Found c_name : "+c_name)
    
    for v in range(exp_count):
        if probe_file_list[v].find('_'+str(exp_count_fixed)+'.txt')>=0:
            probe_name = probe_file_list[v]
            print("Found probe_name : "+probe_name)

    s_name = s_name[:-4]+"_server_"+str(exp_count_fixed)+"_"+ClientState
    c_name = c_name[:-4]+"_client_"+str(exp_count_fixed)+"_"+ClientState
    probe_name = probe_name[:-4]+"_tcpprbe_"+str(exp_count_fixed)+"_"+ClientState
    print("------------------Final Results------------------")
    print("------------------s_name is "+s_name)
    print("------------------c_name is "+c_name)
    print("------------------probe_name is "+probe_name)
    doc, tag, text = Doc().tagtext()
    # TODO: write html file 
    # pServer_128.105.145.245_9001_73.243.11.61_36658_1592423453_1_download_cubic.txt

    indexfilename = result_dir+'/'+"index_"+str(exp_count_fixed)+".html"
    with tag('html'):
        with tag('head'):
            with tag('script', ('src','fillData.js')):
                text("")															
        with tag('body', ('onload','fillData()'), id = 'Results'):
            with tag('h1'):
                text("Experiment No. = TEST ") # + str(exp_count_fixed))
            with tag('h1'):
                text("Run No. = " + str(exp_count_fixed))
            with tag('h1'):
                text("Description = " + descrpition)
            with tag('h2'):
                text("Setup")
            with tag('table'):
                with tag('tr'):
                    with tag('td'):
                        text('Item')
                    with tag('td'):
                        text('Value')
                with tag('tr'):
                    with tag('td'):
                        text("ClientState")
                    with tag('td'):
                        text(ClientState)
                with tag('tr'):
                    with tag('td'):
                        text("Congestion control")
                    with tag('td'):
                        text(proto)
                with tag('tr'):
                    with tag('td'):
                        text("duration")
                    with tag('td'):
                        text(str(duration))
                with tag('tr'):
                    with tag('td'):
                        text("interval")
                    with tag('td'):
                        text(str(interval))
            with tag('table'):			
                with tag('tr'):		
                    with tag('td'):
                        with tag('h3'):
                            with tag('p'):
                                text('TCP_Probe 1 cwnd&RTT Graph')
                            with tag('div', id='photo-container'):
                                doc.stag('img', src=probe_name+"_total_tp1.png", klass="photo")					
                    with tag('td'):							
                        with tag('h3'):
                            with tag('p'):
                                text('TCP_Probe 2 Graph')
                            with tag('div', id='photo-container'):
                                doc.stag('img', src=probe_name+"_total_tp2.png",  klass="photo")	
            with tag('table'):			
                with tag('tr'):		
                    with tag('td'):
                        with tag('h3'):
                            with tag('p'):
                                text('Perf3 Server Throghtput&cwnd&RTT Graph')
                            with tag('div', id='photo-container'):
                                doc.stag('img', src=s_name+"_total.png", klass="photo")					
                    with tag('td'):							
                        with tag('h3'):
                            with tag('p'):
                                text('Perf3 Client Throghtput&cwnd&RTT Graph')
                            with tag('div', id='photo-container'):
                                doc.stag('img', src=c_name+"_total.png",  klass="photo")
            with tag('table'):			
                with tag('tr'):			
                    with tag('td'):
                        with tag('h3'):
                            with tag('p'):
                                text('Perf3 Server Throghtput&cwnd Graph')
                            with tag('div', id='photo-container'):
                                doc.stag('img', src=s_name+"_cwnd.png", klass="photo")					
                    with tag('td'):							
                        with tag('h3'):
                            with tag('p'):
                                text('Perf3 Client Throghtput&cwnd Graph')
                            with tag('div', id='photo-container'):
                                doc.stag('img', src=c_name+"_cwnd.png",  klass="photo")
            with tag('table'):			
                with tag('tr'):			
                    with tag('td'):
                        with tag('h3'):
                            with tag('p'):
                                text('Perf3 Server ssthreshold Graph')
                            with tag('div', id='photo-container'):
                                doc.stag('img', src=s_name+"_ssth.png", klass="photo")					
                    with tag('td'):							
                        with tag('h3'):
                            with tag('p'):
                                text('Perf3 Client ssthreshold Graph')
                            with tag('div', id='photo-container'):
                                doc.stag('img', src=c_name+"_ssth.png", klass="photo")							
            with tag('table'):			
                with tag('tr'):			
                    with tag('td'):
                        with tag('h3'):
                            with tag('p'):
                                text('Perf3 RTT Server Graph')
                            with tag('div', id='photo-container'):
                                doc.stag('img', src=s_name+"_rtt.png", klass="photo")					
                    with tag('td'):							
                        with tag('h3'):
                            with tag('p'):
                                text('Perf3 RTT Client Graph')
                            with tag('div', id='photo-container'):
                                doc.stag('img', src=c_name+"_rtt.png", klass="photo")				
            with tag('table'):			
                with tag('tr'):			
                    with tag('td'):
                        with tag('h3'):
                            with tag('p'):
                                text('Server Throghtput & RSRP Graph')
                            with tag('div', id='photo-container'):
                                doc.stag('img', src=s_name+"_rsrp.png", klass="photo")					
                    with tag('td'):							
                        with tag('h3'):
                            with tag('p'):
                                text('Client Throghtput & RSRP Graph')
                            with tag('div', id='photo-container'):
                                doc.stag('img', src=c_name+"_rsrp.png", klass="photo")				
            with tag('table'):	
                with tag('tr'):			
                    with tag('td'):
                        with tag('h3'):
                            with tag('p'):
                                text('Server Throghtput & Service Graph')
                            with tag('div', id='photo-container'):
                                doc.stag('img', src=s_name+"_service.png", klass="photo")					
                    with tag('td'):							
                        with tag('h3'):
                            with tag('p'):
                                text('Client Throghtput & Service Graph')
                            with tag('div', id='photo-container'):
                                doc.stag('img', src=c_name+"_service.png", klass="photo")			
            with tag('table'):	
                with tag('tr'):			
                    with tag('td'):
                        with tag('h3'):
                            with tag('p'):
                                text('Server Throghtput & Temperature Graph')
                            with tag('div', id='photo-container'):
                                doc.stag('img', src=s_name+"_temperature.png", klass="photo")					
       
    with open(indexfilename, 'w') as fout:
        fout.write(doc.getvalue())
    fout.close()


# index.html

today = date.today()
current_time="%.0f"%time.time()
doc, tag, text = Doc().tagtext()
index_main_filename = home_dir+'/'+"index.html"
with tag('html'):
    with tag('head'):
        with tag('script', ('src','fillData.js')):
            text("")															
    with tag('body', ('onload','fillData()'), id = 'Results'):
        with tag('h1'):
            text("5G Measurement Study Results") # + str(exp_count_fixed))
        with tag('h2'):
            text("Date: "+ str(today)+" " + str(current_time))
        with tag('h2'):
            text("Location = Superior")
        with tag('h2'):
            with tag('td'):
                text("Congestion control")
            with tag('td'):
                text(proto)
        for i in range(exp_count):
            print(i)
            with tag('table'):
                with tag('tr'):
                    with tag('td'):
                        text('Index: '+ str(i+1))
                    with tag('td'):
                        with tag('a', href='plot/index_'+str(i)+'.html'):
                            text('link')
            	       
    with open(index_main_filename, 'w') as fout:
        fout.write(doc.getvalue())
    fout.close()

# TODO: copy all file into results folder with date-lte/5g-protocol
backup_tmp_folder_name = backup_dir+'/' + server_name+'-'+str(today)+'-'+ str(current_time)+'-'+proto+'-'+ClientState+'-stream-'+str(ClientStreams)+'-exp-'+str(exp_count)+'-d-'+str(duration)+'-i-'+str(interval)
cmd = 'mkdir ' + backup_tmp_folder_name
print("backup_tmp_folder_namemd is "+backup_tmp_folder_name)
os.system(cmd)
cmd = 'mkdir ' + backup_tmp_folder_name+'/data'
os.system(cmd)
cmd = 'mkdir ' + backup_tmp_folder_name+'/plot'
os.system(cmd)


cp_cmp = 'cp -R '+data_dir+'/'+' '+backup_tmp_folder_name+'/data'
os.system(cp_cmp)
cp_cmp = 'cp -R '+result_dir+'/'+' '+backup_tmp_folder_name
os.system(cp_cmp)
cp_cmp = 'cp -R '+tmp_dir+'/'+' '+backup_tmp_folder_name+'/plot'
os.system(cp_cmp)

# server 1
if server_name == 'server_1':
    tar_cmp = 'tar -cvf '+'~/backup1.tar.gz '+backup_tmp_folder_name+'/*'
    os.system(tar_cmp)

    cp_cmp = 'cp ~/backup1.tar.gz /mydata/www/html/tmp/'
    os.system(cp_cmp)

elif server_name == 'server_2':

    tar_cmp = 'tar -cvf '+'~/backup2.tar.gz '+backup_tmp_folder_name+'/*'
    os.system(tar_cmp)

    scp_cmd = id_rsa+' ~/backup2.tar.gz '+username+'@'+main_host+':/mydata/www/html/tmp/'
    print(scp_cmd)
    os.system(scp_cmd)

elif server_name == 'server_3':
    tar_cmp = 'tar -cvf '+'~/backup3.tar.gz '+backup_tmp_folder_name+'/*'
    os.system(tar_cmp)

    scp_cmd = id_rsa+' ~/backup3.tar.gz '+username+'@'+main_host+':/mydata/www/html/tmp/'
    print(scp_cmd)
    os.system(scp_cmd)

rm_cmd = 'rm ../../data/* ../../plot/* ../../tmpData/* ~/backup/* -rf'
os.system(rm_cmd)
print(rm_cmd)