#include "../Server/src/components/container/usersContainer.h"
#include "../Server/src/components/container/medicsContainer.h"
#include "../Server/src/components/container/priem_timesContainer.h"
#include "../Server/src/components/container/users_priems.h"
#include <iostream>
#include "src/components/NetworkModule/NetworkModule.h"
#include <nlohmann/json.hpp>



void main(string from_client) {
	INetwork* network = (INetwork*)new Network();
	MedicsContainer* medics = new MedicsContainer;
	UsersContainer* users = new UsersContainer;
	Priem_timesContainer* tm_priems = new Priem_timesContainer;
	User_priemsContainer* us_priems = new User_priemsContainer;
	while (true) {
		std::string buffer = network->receiveRequest();
		std::cout << buffer;
		nlohmann::json recv =  nlohmann::json::parse(buffer);

		if (recv["Method"] == "INSERT") {
			std::cout << "\n ddd:" << recv["DBname"];
		}
		
		
		

		

		
		
		
		
	}
	int a = 0;
	
}