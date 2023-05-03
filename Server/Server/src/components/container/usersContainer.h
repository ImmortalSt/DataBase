#pragma once
#include "../container/IContainer.h"


class UsersContainer : IContainer {
private:
	int id = 0;
	json j;
	vector<json>* users;
public:

	json getElement(json param) override {
		for (int i = 0; i < users->size(); i++) {
			if (param["email"] == users->at(i)["email"]) 
				return users->at(i);
		}
	}

	int addElement(json param) override {
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

		return 0;
	}
	
	int removeElementByParam(json param) override {
		for (int i = 0; i < users->size(); i++) {
			if (param["email"] == users->at(i)["email"]) {
				users->erase(users->begin() + i);
				return 0;
			}
		}
	}

	int changeElementUsingParam() {
		return 0;
	}

};