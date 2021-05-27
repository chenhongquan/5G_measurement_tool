#include <cassert>
#include <chrono>
#include <cstdlib>
#include <iostream>
#include <mutex>
#include <string.h>
#include <thread>

#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>

#include "tcp-header.hh"
#include "udp-socket.hh"

#define BUFFSIZE 15000

using namespace std;

// used to lock socket used to listen for packets from the sender
mutex socket_lock; 
int port = 9001; // set this port for the server

// Periodically probes a server with a well known IP address and looks for
// senders that want to connect with this application. In case such a 
// sender exists, tries to punch holes in the NAT (assuming that this 
// process is a NAT).
//
// To be run as a separate thread, so the rest of the code can assume that 
// packets arrive as if no NAT existed.
//
// Currently is only robust if the sender is not behind a NAT, but only the 
// sender needs to be changed to fix this. 
/*void punch_NAT(string serverip, UDPSocket &sender_socket) {
	const int buffsize = 2048;
	char buff[buffsize];
	UDPSocket::SockAddress addr_holder;
	UDPSocket server_socket;

	server_socket.bindsocket(serverip, 4839, 0);
	while (1) {
		this_thread::sleep_for( chrono::seconds(5) );

		server_socket.senddata(string("Listen").c_str(), 6, serverip, 4839);
		server_socket.receivedata(buff, buffsize, -1, addr_holder);

		char ip_addr[32];
		int port;
		sscanf(buff, "%s:%d", ip_addr, &port);

		int attempt_count = 0;
		const int num_attempts = 500;
		while(attempt_count < num_attempts) {
			socket_lock.lock();
				sender_socket.senddata("NATPunch", 8, string(ip_addr), port);
				// keep the timeout short so that acks are sent in time
				int received = sender_socket.receivedata(buff, buffsize, 5, 
															addr_holder);
			socket_lock.unlock();
			if (received == 0) break;
			++ attempt_count;
		}
		cout << "Could not connect to sender at " << UDPSocket::decipher_socket_addr(addr_holder) << endl;
	}
}*/

// For each packet received, acks back the pseudo TCP header with the 
// current  timestamp
void echo_packets(UDPSocket &sender_socket) {
	char buff[BUFFSIZE];
	sockaddr_in sender_addr;
	char hello[18] = "Hello from client";

	chrono::high_resolution_clock::time_point start_time_point = \
		chrono::high_resolution_clock::now();
	//set memory and address to send and then receive 
	memset(&sender_addr, 0, sizeof(sender_addr));	
	// Filling server information 
        sender_addr.sin_family = AF_INET;
        sender_addr.sin_port = htons(port);
        sender_addr.sin_addr.s_addr = inet_addr("000.000.000.000"); // change server IP
    std::cout<<"Let us send the permission to server to send\n";
	if(sendto(sender_socket.getsocket(), (const char *)hello, strlen(hello),
                MSG_CONFIRM, (const struct sockaddr *) &sender_addr,
                        sizeof(sender_addr))<0){
		perror("Error in sending");
		exit(0);
	}else{
		std::cout<<"sent the message succeful\n";
		//exit(0);
	}
	while (1) {
		int received __attribute((unused)) = -1;
		while (received == -1) {
			//socket_lock.lock();
				received = sender_socket.receivedata(buff, BUFFSIZE, -1, \
					sender_addr);
			//socket_lock.unlock();
			assert( received != -1 );
		}
		cout<<"syslab: Done receiving the datan\n";
		TCPHeader *header = (TCPHeader*)buff;
		header->receiver_timestamp = \
			chrono::duration_cast<chrono::duration<double>>(
				chrono::high_resolution_clock::now() - start_time_point
			).count()*1000; //in milliseconds

		//socket_lock.lock();
			//sender_socket.senddata(buff, sizeof(TCPHeader), &sender_addr);
		if(sendto(sender_socket.getsocket(), (const char *)buff, sizeof(TCPHeader),0, (const struct sockaddr *) &sender_addr,sizeof(sender_addr))<0){
			perror("Failed to send");
			exit(0);
		}
		//socket_lock.unlock();
	}
}

int main(int argc, char* argv[]) {
	if (argc == 2)
		port = atoi(argv[1]);

	UDPSocket sender_socket;
	//sender_socket.bindsocket(port);//sand: commenting to send some data first
	
	//thread nat_thread(punch_NAT, nat_ip_addr, ref(sender_socket));
	echo_packets(sender_socket);

	return 0;
}