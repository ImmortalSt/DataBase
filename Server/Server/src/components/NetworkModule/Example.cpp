#include <iostream>
#include <string>
#pragma comment(lib, "ws2_32.lib")
#include <winsock2.h>
#pragma warning(disable:4996)
#include <stdlib.h>
#include <time.h>
#include "src/components/NetworkModule/NetworkModule.h"
using namespace std;

int servak() {
		
		string alphabet = "AaBbCcDdEeFfGgJjKkLlMmNnOoPpQqRrSsTZ0123456789";
		srand(time(NULL));
		//
		WSAData wsaData;
		WORD DLLVersion = MAKEWORD(2, 1);
		if (WSAStartup(DLLVersion, &wsaData) != 0) {
			cout << "Error" << endl;
		}
		
		
		Network serv = Network();
		serv.bindSock();
		cout << "<<SERVER FIELD>>" << endl<< endl;
		while (TRUE) {
			//serv.sendRequest(serv.receiveRequest());
			
			string rec = serv.receiveRequest();

			for (int i = 0; i < rec.size(); i++) {
				int r = rand() % (alphabet.size());
				rec[i] = alphabet[r];
			}

			cout << "Server convert recieved msg to: " << rec << endl;
			serv.sendRequest(rec);
			cout << endl;
		}
}

