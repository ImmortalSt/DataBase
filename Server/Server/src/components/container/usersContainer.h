#pragma once
#include "IContainer.h"


class UserElement {
private:
	int hash_id;
	string email;
	string pass;
	int is_admin; // true - false
	int number;
	int polis;
	string name;
	string surname;
	int age;
public:
	UserElement() {
		hash_id = 1;
		email = "1";
		pass = "1";
		is_admin = 0; // true - false
		number = 1;
		polis = 1;
		name  = "1";
		surname = "1";
		age = 1;
	}

	void print() {
		cout << hash_id <<" "<<  email <<" "<<   pass << " " << is_admin << "\n";
	}

public:

	string GetEmail() {
		return email;
	}

	string GetPass() {
		return pass;
	}

	int GetIs_admin() {
		return is_admin;
	}

	int GetNumber() {
		return number;
	}

	int GetPolis() {
		return polis;
	}

	string GetName() {
		return name;
	}

	string GetSurname() {
		return surname;
	}

	int GetAge() {
		return age;
	}
};

class UsersContainer {
private:
	const int CAPACITY = 100;
	vector<list<UserElement>> table;

	int GetHash(string name, string surname) {
		int index = std::stoi(name + surname) % CAPACITY;
		return index;
	}
public:
	UsersContainer() {
		table.reserve(CAPACITY);
		for (int i = 0; i < CAPACITY; i++) {
			table.push_back(list<UserElement>());
		}
	}

	UserElement GetUserElement(string name, string surname) {
		for (UserElement newelement : table[GetHash(name, surname)]) {
			if (newelement.GetName() == name && newelement.GetSurname() == surname) {
				return newelement;
			}
		}
	}

	UserElement GetUserElement(int cabinet) {
	}

	int removeElement(string name, string surname) {
		list<UserElement> newelement = table[GetHash(name, surname)];
		auto it = newelement.begin();
		for (int i = 0; i < newelement.size(); i++) {
			std::advance(it, i);
			if ((*it).GetName() == name && (*it).GetSurname() == surname) {
				newelement.erase(it);
				return 0;
			}
		}
	}

	int addElement(UserElement element) {
		table[GetHash(element.GetName(), element.GetSurname())].push_back(element);
		return 0;
	}

	int changeElement(UserElement old, UserElement new_one) {
		list<UserElement> newelement = table[GetHash(old.GetName(), old.GetSurname())];
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