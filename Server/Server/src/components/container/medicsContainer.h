#pragma once
#include "../container/IContainer.h"

class MedicsContainer : IContainer {
private:
	int id = 0;
	json j;
	vector<json>* medics;
public:

	json getElement(json param) override {
		for (int i = 0; i, medics->size(); i++) {
			if (param["surname"] == medics->at(i)["surname"] && param["name"] == medics->at(i)["name"]) {
				return medics->at(i);
			}
		}
	}

	int addElement(json param) override {
		if (!(param.contains("id")))
			param["id"] = ++id;
		if (!(param.contains("name")))
			param["name"] = "";
		if (!(param.contains("surname")))
			param["surname"] = "";
		if (!(param.contains("speciality")))
			param["speciality"] = "";
		if (!(param.contains("cabinet")))
			param["cabinet"] = 666;
		medics->push_back(param);
		return 0;
	}

	int removeElementByParam(json param) override {
		for (int i = 0; i < medics->size(); i++) {
			if (param["surname"] == medics->at(i)["surname"] && param["name"] == medics->at(i)["name"]) {
				medics->erase(medics->begin() + i);
				return 0;
			}
		}
	}

	int changeElementUsingParam() {
		return 0;
	}

	MedicsContainer() = default;
};