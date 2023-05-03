#include "../Server/src/components/container/usersContainer.h"
#include "../Server/src/components/container/medicsContainer.h"
#include "../Server/src/components/container/priem_timesContainer.h"
#include "../Server/src/components/container/users_priemsContainer.h"
#include <iostream>
#include "src/components/NetworkModule/NetworkModule.h"
#include <nlohmann/json.hpp>


void StartLoop(INetwork* network);

void main(string from_client) {
	INetwork* network = (INetwork*)new Network();
	
	
	int a = 0;
	StartLoop(network);
}

void StartLoop(INetwork* network) {
	while (true) {
		UsersContainer* users{};
		MedicsContainer* medics{};
		PriemTimesContainer* tmpriems{};
		User_PriemsContainer* uspriems{};
		
		std::string buffer = network->receiveRequest();
		std::cout << buffer;
		nlohmann::json recv = nlohmann::json::parse(buffer);
		if (recv["DBName"] == "users") {
			if (recv["Method"] == "INSERT") {
				users->addElement(recv["param"]);
			}
		}
		else if (recv["DBName"] == "medics") {
			if (recv["method"] == "INSERT") {
				medics->addElement(recv["param"]);
			}
		}
		else if (recv["DBName"] == "priemtimes") {
			if (recv["method"] == "INSERT") {
				tmpriems->addElement(recv["param"]);
			}
		}
		else if (recv["DBName"] == "user_priems") {
			if (recv["method"] == "INSERT") {
				uspriems->addElement(recv["param"]);
			}
		}
		else {
			cout << "\n Incorrect  DBNAME\n";
		}
	}
}