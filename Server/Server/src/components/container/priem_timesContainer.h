#pragma once
#include "IContainer.h"

class Priem_timeElement {
private:
	int id;
	int medic_id;
	string time;
	int is_used;
public:
	Priem_timeElement() {
		id = 1;
		medic_id = 1;
		time = "1";
		is_used = 0;
	}

	void  print() {
		cout << id << " " << medic_id << " " << time << " " << is_used << "\n";
	}

	int GetId() { return id; }
	int GetMedic_id() { return medic_id; }
	string GetTime() { return time; }
	int GetIs_used() { return is_used; }
};

class Priem_timesContainer {
private:
	const int CAPACITY = 100;
	vector<list<Priem_timeElement>> table;

	int GetHash(string time) {
		int index = std::stoi(time) % CAPACITY;
		return index;
	}

public:

	Priem_timesContainer() {
		table.reserve(CAPACITY);
		for (int i = 0; i < CAPACITY; i++) {
			table.push_back(list<Priem_timeElement>());
		}
	}

	Priem_timeElement GetPriem_timeElement(int id, string time) {
		for (Priem_timeElement newelement : table[GetHash(time)]) {
			if (newelement.GetId() == id) {
				return newelement;
			}
		}
	}

	int removeElement(string time, int id) {
		list<Priem_timeElement> newelement = table[GetHash(time)];
		auto it = newelement.begin();
		for (int i = 0; i < newelement.size(); i++) {
			std::advance(it, i);
			if ((*it).GetId() == id) {
				newelement.erase(it);
				return 0;
			}
		}
	}
	int addElement(Priem_timeElement element) {
		table[GetHash(element.GetTime())].push_back(element);
		return 0;
	}

	int changeElement(Priem_timeElement old, Priem_timeElement new_one) {
		list<Priem_timeElement> newelement = table[GetHash(old.GetTime())];
		auto it = newelement.begin();
		for (int i = 0; i < newelement.size(); i++) {
			std::advance(it, i);
			if ((*it).GetId() == old.GetId()) {
				newelement.erase(it);
				newelement.insert(it, new_one);
				return 0;
			}
		};
	}
};


