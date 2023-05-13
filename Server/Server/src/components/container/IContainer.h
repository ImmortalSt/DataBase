#pragma once
#include <iostream>
#include <vector>
#include <string>
#include <list>
#include <cstdint>
#include <fstream>
#include "../json/nlohmann/single_include/nlohmann/json.hpp"
#include <iostream>
#include <fstream>
#include <string>

using namespace std; /* ::string, std::vector, std::list, std::cout, std::endl, nlohmann::json;*/
using namespace nlohmann;

class IContainer {
public:

	virtual json getElementById(json param) = 0;

	virtual json getElement(json j) = 0;

	virtual int addElement(json &j) = 0; 

	virtual int removeElementByParam(json &param) = 0;
	
	virtual int UpdateElementsParam(json &param) = 0;

	virtual vector<json>* GetElements() = 0;
};
