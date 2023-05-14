#pragma once
#include "../container/IContainer.h"

class PriemTimesContainer : IContainer {
private:
	int id = 0;
	json j;
	vector<json>* tmpriems = new vector<json>();
public:
	PriemTimesContainer() {
		ifstream file("src\\components\\container\\priemtimes.txt");
		string s;
		while (getline(file, s)) {
			json m = json::parse(s);
			tmpriems->push_back(m);
		}
		id = tmpriems->size() + 1;

		file.close();
	}

	vector<json>* GetElements() override {
		return tmpriems;
	}

	json getElementById(json param) override {
		for (int i = 0; i < tmpriems->size(); i++) {
			if (param["id"] == tmpriems->at(i)["id"])
				return tmpriems->at(i);
		}
	}

	json getElement(json param) override {
		for (int i = 0; i < tmpriems->size(); i++) {
			if (param["user_id"] == tmpriems->at(i)["user_id"])
				return tmpriems->at(i);
		}
	}

	json getElementByMedic(json param) {
		for (int i = 0; i < tmpriems->size(); i++) {
			if (param["medic_id"] == tmpriems->at(i)["medic_id"])
				return tmpriems->at(i);
		}
	}

	

	int addElement(json &param) override {
		if (!(param.contains("id")))
			param["id"] = ++id;
		if (!(param.contains("medic_id")))
			param["medic_id"] = 0;
		if (!(param.contains("time")))
			param["time"] = "";
		if (!(param.contains("is_used")))
			param["is_used"] = 1;


		std::ofstream outfile("src\\components\\container\\priemtimes.txt", std::ios_base::app);
		outfile << param << '\n';
		outfile.close();
		tmpriems->push_back(param);
		return 0;
	}

	int removeElementByParam(json &param) override {
		for (int i = 0; i < tmpriems->size(); i++) {
			if (param["id"] == tmpriems->at(i)["id"]) {
				tmpriems->erase(tmpriems->begin() + i);
				return 0;
			}
		}
	}

	int UpdateElementsParam(json &param) override {
		for (int i = 0; i < tmpriems->size(); i++) {
			if (param["id"] == tmpriems->at(i)["id"]) {
				if (param.contains("medic_id"))
					tmpriems->at(i)["medic_id"] = param["medic_id"];
				if (param.contains("user_id"))
					tmpriems->at(i)["user_id"] = param["user_id"];
				if (param.contains("is_used"))
					tmpriems->at(i)["is_used"] = param["is_used"];
				
			}

		}
		std::ofstream outfile("src\\components\\container\\priemtimes.txt", std::ios_base::trunc);
		for (int i = 0; i, tmpriems->size(); i++) {
			outfile << tmpriems->at(i) << "\n";
		}
		outfile.close();
		return 0;
	}
};