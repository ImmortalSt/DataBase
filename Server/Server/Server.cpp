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
				string msg = "[";
				for (int i = 0; i < users.GetElements()->size(); i++) {
					msg += "(\"email\" : " + (string)users.GetElements()->at(i)["email"] + "," + "\"pass\" : " + (string)users.GetElements()->at(i)["pass"] + ","
						+ "\"id\" : " + (string)users.GetElements()->at(i)["id"] + "," + "\"is_admin\" : " + (string)users.GetElements()->at(i)["is_admin"] + ")," ;
				}
				msg[msg.length() - 1] = ']';
				network->sendRequest(msg);
			}
			else if (recv_msg["method"] == "SELECT email, name, surname, number, polis, age, id") {
				string msg = "[";
				for (int i = 0; i < users.GetElements()->size(); i++) {
					msg += "(\"email\" : " + (string)users.GetElements()->at(i)["email"] + "," + "\"name\" : " + (string)users.GetElements()->at(i)["name"] + ","
						+ "\"surname\" : " + (string)users.GetElements()->at(i)["surname"] + "," + "\"number\" : " + (string)users.GetElements()->at(i)["number"] + ","
						+ "\"polis\" : " + (string)users.GetElements()->at(i)["polis"] + "," + "\"age\" : " + (string)users.GetElements()->at(i)["age"] + "," 
						"\"id\" : " + (string)users.GetElements()->at(i)["id"] + "," + "),";
				}
				msg[msg.length() - 1] = ']';
				network->sendRequest(msg);
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
				string msg = "[";
				for (int i = 0; i < users.GetElements()->size(); i++) {
					msg += "(\"email\" : " + (string)users.GetElements()->at(i)["email"] + "," + 
					"\"id\" : " + (string)users.GetElements()->at(i)["id"] + "),";
				}
				msg[msg.length() - 1] = ']';
				network->sendRequest(msg);
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
			else {
				cout << "\nIncorrect method in users\n";	
			}
		}
		else if (recv_msg["db_name"] == "medics") {
			if (recv_msg["method"] == "INSERT") {
				medics.addElement(recv_msg["param"]);
			}
			else if (recv_msg["method"] == "SELECT specialty, id") {
				string msg = "[";
				for (int i = 0; i < medics.GetElements()->size(); i++) {
					msg += "(\"speciality\" : " + (string)medics.GetElements()->at(i)["speciality"] + "," +
						"\"id\" : " + (string)medics.GetElements()->at(i)["id"] + "),";
				}
				msg[msg.length() - 1] = ']';
				network->sendRequest(msg);
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
			else {
				cout << "\nIncorrect method in medics\n";
			}
		}
		else if (recv_msg["db_name"] == "priemtimes") {
			
			if (recv_msg["method"] == "INSERT") {
				tmpriems.addElement(recv_msg["param"]);
			}
			else if (recv_msg["method"] == "SELECT time, id WHERE medic_id = :id and is_used = 0") {
				string msg = "[";
				for (int i = 0; i < tmpriems.GetElements()->size(); i++) {
					if (tmpriems.GetElements()->at(i)["is_used"] == 0) {
						msg += "(\"time\" : " + (string)tmpriems.GetElements()->at(i)["time"] + "," + "\"id\" : " 
							+ (string)tmpriems.GetElements()->at(i) + "),";
					} else {}
				}
				msg[msg.length() - 1] = ']';
				network->sendRequest(msg);
			}
			else if (recv_msg["method"] == "SELECT time WHERE medic_id=:id") {////////////////////////////////////////////////////
				network->sendRequest(tmpriems.getElementByMedic(recv_msg["param"])["time"].dump());
			}
			else if (recv_msg["method"] == "UPDATE SET is_used = 1 WHERE id=:id") {
				tmpriems.getElementById(recv_msg["param"])["is_used"] = 1;
			}
			else if (recv_msg["method"] == "SELECT time, id WHERE medic_id=:id") {
				json j;
				j["time"] = tmpriems.getElementByMedic(recv_msg["param"])["time"];
				j["id"] = tmpriems.getElementByMedic(recv_msg["param"])["id"];
				network->sendRequest(j.dump());
			}
			else if (recv_msg["method"] == "SELECT * WHERE id=:id") {
				network->sendRequest(tmpriems.getElementByMedic(recv_msg["param"]));
			}
			else if (recv_msg["method"] == "UPDATE WHERE id=:id") {
				tmpriems.UpdateElementsParam(recv_msg["param"]);
			}
			else if (recv_msg["method"] == "DELETE WHERE id=:id") {
				tmpriems.removeElementByParam(recv_msg["param"]);
			}
			else {
				cout << "\nIncorrect method in priemtimes\n";
			}
		}
		else if (recv_msg["db_name"] == "user_priems") {
			if (recv_msg["method"] == "INSERT") {
				uspriems.addElement(recv_msg["param"]);
			}
			else if (recv_msg["method"] == "SELECT priem, id WHERE user_id=:id") {
				json j;
				j["priem"] = uspriems.getElementById(recv_msg["param"])["priem"];
				j["id"] = uspriems.getElementById(recv_msg["param"])["id"];
				network->sendRequest(j.dump());
			}
			else {
				cout << "\nIncorrect method in user_priems\n";
			}
		}
		else {
			cout << "\n Incorrect  db_name\n";
		}
	}
}