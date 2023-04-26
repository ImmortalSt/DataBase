#pragma once
#include "IContainer.h"
#include <cstdint>


class HashContainer : IContainer {
private:

	class HashElement {
	public:
		int id;
		void* element;

		void operator = (const HashElement& other) {

		}

		HashElement(int id, void* element) {
			id = 0;
			element = nullptr;
		}

	};

	const int CAPACITY = 100;
	int size = 0;
	vector<list<HashElement>> table;



	int GetHash(void* el) {
		return (uint16_t)el % CAPACITY;
	}
public:
	HashContainer() {
		table.reserve(CAPACITY);
		for (int i = 0; i < 100; i++) table.push_back(list<HashElement>());
		auto it = table.begin();

	}

	void* getElement(void* element) {
		for (HashElement newelement : table[GetHash(element)]) {
			if (newelement.id == GetHash(element)) {
				return newelement.element;
			}
		}
	}

	int removeElement(void* element) override {
		list<HashElement>* list = &table[GetHash(element)];
		auto it = list->begin();
		for (int i = 0; i < list->size(); i++) {
			std::advance(it, i);
			if (&it == element) {
				list->erase(it);
				return 1;
			}
			else {
				cout << "Element in list was not deleted" << endl;
				return 0;
			}
		}
	}

	int addElement(void* element) override {
		HashElement newelement(0, 0);
		newelement.element = element;
		newelement.id = GetHash(element);
		int a = GetHash(element);
		table[a].push_back(newelement);

		return 0;

		/*size++;
		HashElement newElement = {size - 1, el};
		table[GetHash(size - 1)].push_back(newElement);
		return size - 1;*/
	}

	int changeElement(void* el1, void* el2) override {
		return 0;
	}
};