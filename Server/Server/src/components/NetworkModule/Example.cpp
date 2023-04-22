#include <iostream>
#include <string>
#pragma comment(lib, "ws2_32.lib")
#include <winsock2.h>
#pragma warning(disable:4996)
#include <stdlib.h>
#include <time.h>
#include "src/components/NetworkModule/NetworkModule.h"
using namespace std;

int main() {
		WSAData wsaData;
		WORD DLLVersion = MAKEWORD(2, 1);
		if (WSAStartup(DLLVersion, &wsaData) != 0) {
			cout << "Error" << endl;
		}
		string alphabet = "AaBbCcDdEeFfGgJjKkLlMmNnOoPpQqRrSsTZ0123456789";
		srand(time(NULL));
		Network serv = Network();
		serv.bindSock();
		serv.listenSock();
		cout << "<<SERVER FIELD>>" << endl<< endl;
		while (TRUE) {
			
			serv.acceptSock();
			string rec = serv.receiveRequest();
			
			for (int i = 0; i < rec.size(); i++) {
				int r = rand() % (alphabet.size());
				rec[i] = alphabet[r];
			}
			char const* msg = rec.c_str();
			cout << "Server convert recieved msg to: " << msg << endl;
			serv.setMsg(msg);
			serv.sendRequest();
			cout << endl;
		}
}

