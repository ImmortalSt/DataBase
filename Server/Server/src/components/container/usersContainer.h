#pragma once
#include "../container/IContainer.h"


class UsersContainer : IContainer {
private:
	int id = 0;
	json j;
	vector<json>* users = new vector<json>();
public:
	UsersContainer() {
		ifstream file("src\\components\\container\\users.txt");
		string s;
		while (getline(file, s)) {
			json m = json::parse(s);
			users->push_back(m);
		}
		id = users->size() + 1;

		file.close();

	}

	vector<json>* GetElements() override {
		return users;
	}

	json getElementById(json param) override {
		for (int i = 0; i < users->size(); i++) {
			if (param["id"] == users->at(i)["id"])
				return users->at(i);
		}
	}

	json getElement(json param) override {
		for (int i = 0; i < users->size(); i++) {
			if (param["email"] == users->at(i)["email"]) 
				return users->at(i);
		}
	}

	int addElement(json &param) override {
		if (!(param.contains("id")))
			param["id"] = ++id;
		if (!(param.contains("is_admin")))
			param["is_admin"] = "";
		if (!(param.contains("number")))
			param["number"] = "";
		if (!(param.contains("polis")))
			param["polis"] = "";
		if (!(param.contains("name")))
			param["name"] = "";
		if (!(param.contains("surname")))
			param["surname"] = "";
		if (!(param.contains("age")))
			param["age"] = "";
		
		users->push_back(param);
		std::ofstream outfile("src\\components\\container\\users.txt", std::ios_base::app);
		outfile << param << '\n';
		outfile.close();

		return 0;
	}
	
	int removeElementByParam(json &param) override {
		for (int i = 0; i < users->size(); i++) {
			if (param["id"] == users->at(i)["id"]) {
				users->erase(users->begin() + i);
				return 0;
			}
		}
	}

	int UpdateElementsParam(json &param) override {
		for (int i = 0; i < users->size(); i++) {
			if (param["id"] == users->at(i)["id"]) {
				if (param.contains("id"))
					users->at(i)["id"] = param["id"];
				if (param.contains("is_admin"))
					users->at(i)["is_admin"] = param["is_admin"];
				if (param.contains("number"))
					users->at(i)["number"] = param["number"];
				if (param.contains("polis"))
					users->at(i)["polis"] = param["polis"];
				if (param.contains("name"))
					users->at(i)["name"] = param["name"];
				if (param.contains("surname"))
					users->at(i)["surname"] = param["surname"];
				if (param.contains("age"))
					users->at(i)["age"] = param["age"];
				if (param.contains("email"))
					users->at(i)["email"] = param["email"];
				if (param.contains("pass"))
					users->at(i)["pass"] = param["pass"];
				return 0;
			}
		}
	}


};