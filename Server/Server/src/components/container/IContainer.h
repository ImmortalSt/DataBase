#pragma once
#include <iostream>
#include <vector>
#include <string>
#include <list>
#include <cstdint>

using namespace std;/*std::string, std::vector, std::list, std::cout, std::endl;*/


class IContainer {
public:
	virtual void* getElement(void* element) = 0;

	virtual int addElement(void* element) = 0; // it returns index 

	virtual int removeElement(void* element) = 0;

	virtual int changeElement(void* el1, void* el2) = 0;

};
