#include <iostream>
#include "src/components/NetworkModule/NetworkModule.h"
#include "../Server/src/components/container/usersContainer.h"
#include "../Server/src/components/container/medicsContainer.h"
#include "../Server/src/components/container/priem_timesContainer.h"
#include "../Server/src/components/container/users_priemsContainer.h"
#include "src/components/json/nlohmann/single_include/nlohmann/json.hpp"


void StartLoop(INetwork* network);

void main(string from_client) {
	INetwork* network = (INetwork*)new Network();
	
	
	int a = 0;
	StartLoop(network);
}

void StartLoop(INetwork* network) {
	UsersContainer users;
	MedicsContainer medics;
	PriemTimesContainer tmpriems;
	User_PriemsContainer uspriems;
	while (true) {
		
		std::string buffer = network->receiveRequest();
		nlohmann::json recv_msg = nlohmann::json::parse(buffer);
		if (recv_msg["db_name"] == "users") {
			if (recv_msg["method"] == "INSERT") {
				users.addElement(recv_msg["param"]); //
			}
			else if (recv_msg["method"] == "UPDATE SET name=:name, surname=:surname, number=:number, polis=:polis, age =:age WHERE id=:id") {
				users.UpdateElementsParam(recv_msg["param"]);
			}
			else if (recv_msg["method"] == "SELECT email, pass, id, is_admin") {

			}
			else if (recv_msg["method"] == "SELECT email, name, surname, number, polis, age, id") {
				//нахуй
			}
			else if (recv_msg["method"] == "SELECT email, name, surname, number, polis, age WHERE id=:id") {
				json j; 
				j["email"] = users.getElementById(recv_msg["param"])["email"];
				j["name"] = users.getElementById(recv_msg["param"])["name"];
				j["surname"] = users.getElementById(recv_msg["param"])["surname"];
				j["number"] = users.getElementById(recv_msg["param"])["number"];
				j["polis"] = users.getElementById(recv_msg["param"])["polis"];
				j["age"] = users.getElementById(recv_msg["param"])["age"];
				network->sendRequest(j.dump());
			}
			else if (recv_msg["method"] == "SELECT email, id") {
				for (int i = 0; i < users.GetElements()->size(); i++) {
					users.getElement(recv_msg["param"])["id"];
					users.getElement(recv_msg["param"])["email"];
				} 
				// тут словарь словарей
			}
			else if (recv_msg["method"] == "SELECT * WHERE id=:id") {
				network->sendRequest(users.getElementById(recv_msg["param"]).dump());
			}
			else if (recv_msg["method"] == "UPDATE WHERE id=:id") {
				users.UpdateElementsParam(recv_msg["param"]);
			}
			else if (recv_msg["method"] == "DELETE WHERE id=:id") {
				users.removeElementByParam(recv_msg["param"]);
			}
 
		}
		else if (recv_msg["db_name"] == "medics") {
			if (recv_msg["method"] == "INSERT") {
				medics.addElement(recv_msg["param"]);
			}
			else if (recv_msg["method"] == "SELECT specialty, id") {
				json j;
				j["speciality"] = medics.getElement(recv_msg["param"])["speciality"];
				j["id"] = medics.getElement(recv_msg["param"])["id"];
				if (recv_msg["param"]["id"] == "") j["speciality"] = j["id"] = "";
				network->sendRequest(j.dump());
			}
			else if (recv_msg["method"] == "SELECT name, surname, cabinet WHERE id=:id") {
				json j;
				j["name"] = medics.getElement(recv_msg["param"])["name"];
				j["surname"] = medics.getElement(recv_msg["param"])["surname"];
				j["cabinet"] = medics.getElement(recv_msg["param"])["cabinet"];
				network->sendRequest(j.dump());
			}
			else if (recv_msg["method"] == "SELECT specialty WHERE id=:id") {
				json j;
				j["speciality"] = medics.getElement(recv_msg["param"])["speciality"];
				network->sendRequest(j.dump());
			}
			else if (recv_msg["method"] == "SELECT * WHERE id = :id") {
				network->sendRequest(medics.getElementById(recv_msg["param"]).dump());
			}
			else if (recv_msg["method"] == "UPDATE WHERE id=:id") {
				medics.UpdateElementsParam(recv_msg["param"]);
			}
			else if (recv_msg["method"] == "DELETE WHERE id=:id") {
				medics.removeElementByParam(recv_msg["param"]);
			}
		}
		else if (recv_msg["db_name"] == "priemtimes") {
			if (recv_msg["method"] == "INSERT") {
				tmpriems.addElement(recv_msg["param"]);
			}
			else if ("SELECT time, id WHERE medic_id = :id and is_used = 0") {
				json j;
				j["time"] = tmpriems.getElementByMedic(recv_msg["param"])["time"];
				j["id"] = tmpriems.getElementByMedic(recv_msg["param"])["id"];
				network->sendRequest(j.dump());
			}
			else if (recv_msg["method"] == "SELECT time WHERE medic_id=:id") {
				network->sendRequest(tmpriems.getElement(recv_msg["param"])["time"].dump());
			}
			else if (recv_msg["method"] == "UPDATE SET is_used = 1 WHERE id=:id") {
				tmpriems.UpdateElementsParam(recv_msg["param"]);
			}
			else if (recv_msg["method"] == "SELECT time, id WHERE medic_id=:id") {
				json j;
				j["time"] = tmpriems.getElementByMedic(recv_msg["param"])["time"];
				j["id"] = tmpriems.getElementByMedic(recv_msg["param"])["id"];
				network->sendRequest(j.dump());
			}
			else if (recv_msg["method"] == "SELECT * WHERE id=:id") {
				json j;
				j["medic_id"] = tmpriems.getElement(recv_msg["param"])["medic_id"];
				j["time"] = tmpriems.getElement(recv_msg["param"])["time"];
				j["is_used"] = tmpriems.getElement(recv_msg["param"])["is_used"];
				network->sendRequest(j.dump());
			}
			else if (recv_msg["method"] == "UPDATE WHERE id=:id") {
				tmpriems.UpdateElementsParam(recv_msg["param"]);
			}
			else if (recv_msg["method"] == "DELETE WHERE id=:id") {
				tmpriems.removeElementByParam(recv_msg["param"]);
			}

		}
		else if (recv_msg["db_name"] == "user_priems") {
			if (recv_msg["method"] == "INSERT") {
				uspriems.addElement(recv_msg["param"]);
			}
			else if (recv_msg["method"] == "SELECT priem, id WHERE user_id=:id") {
				json j;
				j["priem"] = uspriems.getElementById(recv_msg["param"])["priem"];
				j["user_id"] = uspriems.getElementById(recv_msg["param"])["user_id"];
				network->sendRequest(j.dump());
			}
		}
		else {
			cout << "\n Incorrect  db_name\n";
		}
	}
}