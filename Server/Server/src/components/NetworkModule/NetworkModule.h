#ifndef NETWORKMODULE_H;
//#define NETWORKMODULE_H;
#include <iostream>
#pragma comment(lib, "ws2_32.lib")
#include <winsock2.h>
#pragma warning(disable:4996)
#include <stdlib.h>
using namespace std;

class INetwork {
public:
	virtual int bindSock() = 0;
	virtual int sendRequest(string msg) = 0;
	virtual string receiveRequest() = 0;
};

class PlugNetwork : INetwork {
	int bindSock() override {
		return 1;
	}
	int sendRequest(string msg) override {
		return 0;
	}
	string receiveRequest() override {
		return "Ivan Ivanov";
	}

};

class Network : INetwork {
public:

	Network() {
		addr.sin_addr.s_addr = inet_addr("127.0.0.1");
		addr.sin_port = htons(1111);
		addr.sin_family = AF_INET;
		server = socket(AF_INET, SOCK_STREAM, NULL);
	}

	Network(const char* address, int port) {
		addr.sin_addr.s_addr = inet_addr(address);
		addr.sin_port = htons(port);
		addr.sin_family = AF_INET;
		server = socket(AF_INET, SOCK_STREAM, NULL);
	}

	void acceptSock() {
		int sizeofaddr = sizeof(addr);
		listen_Sock = accept(server, (SOCKADDR*)&addr, &sizeofaddr);
	}

	int bindSock() override {
		int result = bind(server, (SOCKADDR*)&addr, sizeof(addr));
		listen(server, SOMAXCONN);
		if (result == SOCKET_ERROR) {
			cout << "building socket failed, error: " << result << endl;
			WSACleanup();
		}
		else
			return 0;
	}

	int sendRequest(string _msg) override {
		char const* msg = _msg.c_str();
		int result = send(listen_Sock, msg, strlen(msg), NULL);
		if (result == SOCKET_ERROR) {
			cout << "send failed, error: " << result << endl;
			closesocket(listen_Sock);
			WSACleanup();
			return result;
		}
		else
			return 0;
	}

	string receiveRequest() override {
		acceptSock();
		char recvBuffer[512];
		ZeroMemory(recvBuffer, 512);

		int result = recv(listen_Sock, recvBuffer, size(recvBuffer), 0);
		string recvBuff(recvBuffer);

		if (result > 0) {
			cout << "Recieved bytes: " << result << endl;
			cout << "Recieved data: " << recvBuff << endl;
			return recvBuff;
		}
		else if (result == 0)
			cout << "Connection closing" << endl;
		else {
			cout << "Recieved failed" << endl;
			closesocket(listen_Sock);
			WSACleanup();
		}		
	}

private:
	SOCKET server;
	SOCKET listen_Sock;
	SOCKADDR_IN addr;
};

#endif


