#pragma once
#include "IContainer.h"

class MedicElement {
private:
	int id;
	string name;
	string surname;
	string specialist;
	int cabinet;
public:
	MedicElement() {
		id = 0;
		name = "0 ";
		surname = "0 ";
		specialist = "0 ";
		cabinet = 0;
	}

	void print() {
		cout << id << " " << name << " " << surname << " " << specialist << " " << cabinet << "\n";
	}

	int GetId() { return id; }
	string GetName() { return name; }
	string GetSurname() { return surname; }
	string GetSpecialist() { return specialist; }
	int GetCabinet() { return cabinet; }
};

class MedicsContainer {
private: 
	const int CAPACITY = 100;
	vector<list<MedicElement>> table;

	int GetHash(string name, string surname) {
		int index = std::stoi(name + surname) % CAPACITY;
		return index;
	}

public:
	MedicsContainer() {
		table.reserve(CAPACITY);
		for (int i = 0; i < CAPACITY; i++) {
			table.push_back(list<MedicElement>());
		}
	}

	MedicElement GetMedicElement(string name, string surname) {
		for (MedicElement newelement : table[GetHash(name, surname)]) {
			if (newelement.GetName() == name && newelement.GetSurname() == surname) {
				return newelement;
			}
		}
	}

	MedicElement GetMedicElement(int cabinet) {
	}

	int removeElement(string name, string surname) {
		list<MedicElement> newelement = table[GetHash(name, surname)];
		auto it = newelement.begin();
		for (int i = 0; i < newelement.size(); i++) {
			std::advance(it, i);
			if ((*it).GetName() == name && (*it).GetSurname() == surname) {
				newelement.erase(it);
				return 0;
			}
		}
	}

	int addElement(MedicElement element) {
		table[GetHash(element.GetName(), element.GetSurname())].push_back(element);
		return 0;
	}

	int changeElement(MedicElement old, MedicElement new_one) {
		list<MedicElement> newelement = table[GetHash(old.GetName(),old.GetSurname())];
		auto it = newelement.begin();
		for (int i = 0; i < newelement.size(); i++) {
			std::advance(it, i);
			if ((*it).GetName() == old.GetName() && (*it).GetSurname() == old.GetSurname()) {
				newelement.erase(it);
				newelement.insert(it, new_one);
				return 0;
			}
		}
	}

};