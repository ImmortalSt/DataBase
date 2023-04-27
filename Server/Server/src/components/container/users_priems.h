#pragma once
#include "IContainer.h"

class User_priemElement {
private:
	int id;
	int user_id;
	string priem;
public:
	User_priemElement() {
		id = 1;
		user_id = 1;
		priem = "1";
	}

	void print() {
		cout << id << " " << user_id << " " << priem << "\n";
 	}

	int GetId() { return id; }
	int GetUser_id() { return user_id; }
	string GetPriem() { return priem; }




};

class User_priemsContainer {
private:
	const int CAPACITY = 100;
	vector<list<User_priemElement>> table;

	int GetHash(string priem) {
		int index = std::stoi(priem) % CAPACITY;
		return index;
	}
public:
	User_priemsContainer() {
		table.reserve(CAPACITY);
		for (int i = 0; i < CAPACITY; i++) {
			table.push_back(list<User_priemElement>());
		}
	}

	User_priemElement GetUser_priemElement(int id, string priem) {
		for (User_priemElement newelement : table[GetHash(priem)]) {
			if (newelement.GetId() == id) {
				return newelement;
			}
		}
	}

	int removeElement(string priem, int id) {
		list<User_priemElement> newelement;
		table[GetHash(priem)] = newelement;
		auto it = newelement.begin();
		for (int i = 0; i < newelement.size(); i++) {
			std::advance(it, i);
			if ((*it).GetId() == id) {
				newelement.erase(it);
				return 0;
			}
		}
	}
	int addElement(User_priemElement element) {
		table[GetHash(element.GetPriem())].push_back(element);
		return 0;
	}

	int changeElement(User_priemElement old, User_priemElement new_one) {
		list<User_priemElement> newelement = table[GetHash(old.GetPriem())];
		auto it = newelement.begin();
		for (int i = 0; i < newelement.size(); i++) {
			std::advance(it, i);
			if ((*it).GetId() == old.GetId()) {
				newelement.erase(it);
				newelement.insert(it, new_one);
				return 0;
			}
		}
	}

};