#pragma once
#include "../container/IContainer.h"

class PriemTimesContainer : IContainer {
private:
	int id = 0;
	json j;
	vector<json>* tmpriems;
public:

	json getElement(json param) override {
		for (int i = 0; i < tmpriems->size(); i++) {
			if (param["priems"] == tmpriems->at(i)["priems"] && param["id"] == tmpriems->at(i)["id"])
				return tmpriems->at(i);
		}
	}

	int addElement(json param) override {
		if (!(param.contains("id")))
			param["id"] = ++id;
		if (!(param.contains("medic_id")))
			param["medeic_id"] = 0;
		if (!(param.contains("time")))
			param["time"] = "";
		if (!(param.contains("is_used")))
			param["is_used"] = 1;
		tmpriems->push_back(param);
		return 0;
	}

	int removeElementByParam(json param) override {
		for (int i = 0; i < tmpriems->size(); i++) {
			if (param["priems"] == tmpriems->at(i)["priems"] && param["id"] == tmpriems->at(i)["id"]) {
				tmpriems->erase(tmpriems->begin() + i);
				return 0;
			}
		}
	}

	int changeElementUsingParam() {
		return 0;
	}
};