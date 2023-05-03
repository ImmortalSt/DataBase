#pragma once
#include <iostream>
#include <vector>
#include <string>
#include <list>
#include <cstdint>
#include <nlohmann/json.hpp>

using std::string, std::vector, std::list, std::cout, std::endl, nlohmann::json;


class IContainer {
public:

	virtual json getElement(json j) = 0;

	virtual int addElement(json j) = 0; 

	virtual int removeElementByParam(json param) = 0;
	
	virtual int changeElementUsingParam(json param) = 0;

};
