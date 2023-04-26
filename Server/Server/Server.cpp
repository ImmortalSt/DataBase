#include "../Server/src/components/container/usersContainer.h"
#include "../Server/src/components/container/medicsContainer.h"
#include "../Server/src/components/container/priem_timesContainer.h"
#include "../Server/src/components/container/users_priems.h"
#include <iostream>

int mainy()
{
	UserElement a;
	UsersContainer b;
	b.addElement(a);
	b.GetUserElement(a.GetName(), a.GetSurname()).print();
	b.removeElement(a.GetName(), a.GetSurname());
	b.GetUserElement(a.GetName(), a.GetSurname()).print();
	
	User_priemElement c;
	User_priemsContainer d;
	d.addElement(c);
	d.GetUser_priemElement(c.GetId(), c.GetPriem()).print();

	Priem_timeElement e;
	Priem_timesContainer f;
	f.addElement(e);
	f.GetPriem_timeElement(e.GetId(), e.GetTime()).print();

	MedicElement g;
	MedicsContainer h;
	h.addElement(g);
	h.GetMedicElement(g.GetName(), g.GetSurname()).print();

}

// Запуск программы: CTRL+F5 или меню "Отладка" > "Запуск без отладки"
// Отладка программы: F5 или меню "Отладка" > "Запустить отладку"

// Советы по началу работы 
//   1. В окне обозревателя решений можно добавлять файлы и управлять ими.
//   2. В окне Team Explorer можно подключиться к системе управления версиями.
//   3. В окне "Выходные данные" можно просматривать выходные данные сборки и другие сообщения.
//   4. В окне "Список ошибок" можно просматривать ошибки.
//   5. Последовательно выберите пункты меню "Проект" > "Добавить новый элемент", чтобы создать файлы кода, или "Проект" > "Добавить существующий элемент", чтобы добавить в проект существующие файлы кода.
//   6. Чтобы снова открыть этот проект позже, выберите пункты меню "Файл" > "Открыть" > "Проект" и выберите SLN-файл.
