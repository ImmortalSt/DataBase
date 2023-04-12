#pragma once
#include <iostream>
#include <vector>

class element  {
private:

public:

	element getElement() {
		return;
	}
};


class IContainer {
public:

	virtual int addElement(element el) = 0;

	virtual int removeElement(int id) = 0;

	virtual int changeElement(int id, element el) = 0;

};

