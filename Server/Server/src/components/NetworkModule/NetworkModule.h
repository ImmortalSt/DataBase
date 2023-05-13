#ifndef NETWORKMODULE_H
#define NETWORKMODULE_H
#include <iostream>
#include <string>
#include <iostream>
#include <fstream>
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

class Network : INetwork {
public:

    Network() {
        WSADATA wsa_data;
        WSAStartup(MAKEWORD(2, 2), &wsa_data);

        addr.sin_addr.s_addr = inet_addr("127.0.0.1");
        addr.sin_port = htons(1111);
        addr.sin_family = AF_INET;
        server = socket(AF_INET, SOCK_STREAM, NULL);
        bindSock();
    }

    Network(const char* address, int port) {
        WSADATA wsa_data;
        WSAStartup(MAKEWORD(2, 2), &wsa_data);
        addr.sin_addr.s_addr = inet_addr(address);
        addr.sin_port = htons(port);
        addr.sin_family = AF_INET;
        server = socket(AF_INET, SOCK_STREAM, NULL);
        bindSock();
    }

    void acceptSock() {
        int sizeofaddr = sizeof(addr);
        listen_Sock = accept(server, (SOCKADDR*)&addr, &sizeofaddr);
    }

    int bindSock() override {
        bind(server, (SOCKADDR*)&addr, sizeof(addr));
        int a = listen(server, SOMAXCONN);
        int u = GetLastError();
        return 0;
    }

    int sendRequest(string _msg) override {
        char const* msg = _msg.c_str();
        int result = send(listen_Sock, msg, strlen(msg), NULL);
        if (result == SOCKET_ERROR) {
            cout << "\nsend failed, error: " << result << endl;
            closesocket(listen_Sock);
            WSACleanup();
            return result;
        }
        else {
            std::string log = "\nServer send: " + _msg + '\n';
            std::ofstream outfile("C:\\Users\\Comp\\Documents\\Roguelike\\DataBase\\Server\\Server\\src\\components\\NetworkModule\\log.txt", std::ios_base::app);
            outfile << log << '\n';
            outfile.close();
            std::cout << log;
            cout << log << endl;
            return 0;
        }

    }

    string receiveRequest() override {
        if (listen_Sock == 0) acceptSock();
        char recvBuffer[512];
        ZeroMemory(recvBuffer, 512);

        int result = recv(listen_Sock, recvBuffer, size(recvBuffer), 0);
        string recvBuff(recvBuffer);

        if (result > 0) {
            std::string log = "\nRecieved bytes: " + std::to_string(result) + "\n" + "\nRecieved data : " + recvBuff + '\n';
            std::ofstream outfile("C:\\Users\\Comp\\Documents\\Roguelike\\DataBase\\Server\\Server\\src\\components\\NetworkModule\\log.txt", std::ios_base::app);
            outfile << log << '\n';
            outfile.close();
            std::cout << log;
            return recvBuff;
        }
        else {
            cout << "\nRecieved failed" << endl;
            closesocket(listen_Sock);
            WSACleanup();
            return "-1";
        }
    }

private:
    SOCKET server;
    SOCKET listen_Sock = 0;
    SOCKADDR_IN addr;
};

#endif