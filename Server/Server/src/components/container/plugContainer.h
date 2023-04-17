#pragma once
#include "IContainer.h"



class PlugContainer : IContainer {
private:
	std::vector<element> a;

public:

	int addElement(element el) override {
		return;
	}

	int removeElement(int id) override {
		return;
	}

	int changeElement(int id, element el) override {
		return;
	}


};