#pragma once

#include "../container/IContainer.h"
class MedicsContainer : IContainer {
private:
	int id = 0;
	json j;
	vector<json>* medics = new vector<json>();
public:
	MedicsContainer() {
		ifstream file("src\\components\\container\\medics.txt");
		string s;
		while (getline(file, s)) {
			json m = json::parse(s);
			medics->push_back(m);
		}
		id = medics->size() + 1;
		file.close();
	}

	json getElement(json param) override {
		for (int i = 0; i < medics->size(); i++) {
			if (param["surname"] == medics->at(i)["surname"] && param["name"] == medics->at(i)["name"]) {
				return medics->at(i);
			}
		}
	}

	vector<json>* GetElements() override {
		return medics;
	}

	json getElementById(json param) override {
		for (int i = 0; i < medics->size(); i++) {
			if (param["id"] == medics->at(i)["id"])
				return medics->at(i);
		}
	}

	int addElement(json &param) override {
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

		std::ofstream outfile("src\\components\\container\\medics.txt", std::ios_base::app);
		outfile << param << '\n';
		outfile.close();
		medics->push_back(param);
		return 0;
	}

	int removeElementByParam(json &param) override {
		for (int i = 0; i < medics->size(); i++) {
			if (param["id"] == medics->at(i)["id"]) {
				medics->erase(medics->begin() + i);
				return 0;
			}
		}
	}

	int UpdateElementsParam(json &param) override {
		for (int i = 0; i < medics->size(); i++) {
			if (param["id"] == medics->at(i)["id"]) {
				if (param.contains("id"))
					medics->at(i)["id"] = param["id"];
				if (param.contains("name"))
					medics->at(i)["name"] = param["name"];
				if (param.contains("surname"))
					medics->at(i)["surname"] = param["surname"];
				if (param.contains("speciality"))
					medics->at(i)["speciality"] = param["speciality"];
				if (param.contains("cabinet"))
					medics->at(i)["cabinet"] = param["cabinet"];
				return 0;
			}
		}
	}
};