#pragma once
#include "../container/IContainer.h"


class User_PriemsContainer : IContainer {
private:
	int id = 0;
	json j;
	vector<json>* uspriems;
public:


	json getElement(json param) override {
		for (int i = 0; i < uspriems->size(); i++) {
			if (param["priem"] == uspriems->at(i)["priem"])
				return uspriems->at(i);
		}
	}

	vector<json>* GetElements() override {
		return uspriems;
	}

	json getElementById(json param) override {
		for (int i = 0; i < uspriems->size(); i++) {
			if (param["id"] == uspriems->at(i)["id"])
				return uspriems->at(i);
		}
	}


	int addElement(json &param) override {
		if (!(param.contains("id"))) 
			param["id"] = ++id;

		uspriems->push_back(param);
		return 0;

	}

	int removeElementByParam(json &param) override {
		for (int i = 0; i < uspriems->size(); i++) {
			if ( param["id"] == uspriems->at(i)["id"]) {
				uspriems->erase(uspriems->begin() + i);
				return 0;
			}
		}
	}

	int UpdateElementsParam(json &param) override {
		for (int i = 0; i < uspriems->size(); i++) {
			if (param["id"] == uspriems->at(i)["id"]) {
				if (param.contains("user_id"))
					uspriems->at(i)["user_id"] = param["user_id"];
				if (param.contains("user_id"))
					uspriems->at(i)["priem"] = param["priem"];
				return 0;
			}
		}
	}
};