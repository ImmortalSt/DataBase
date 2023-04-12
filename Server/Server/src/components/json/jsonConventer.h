#pragma once
#include <nlohmann/json.hpp>

class Data {
	int a;
	std::string b;
};

class JsonConventer {
private:
	nlohmann::json j;
	std::string s;
public:

	std::string ConvertToJson(Data data) {
		return;
	}

	Data ConvertToData(nlohmann::json _j) {
		return;
	}

};