from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, \
    Button, TextBox, Widget, Label, DatePicker, DropdownList, CheckBox, PopUpDialog
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText

from datetime import datetime
import sys
import re
import sqlite3

class LoginModel(object):
    def __init__(self):
        # Create a database in RAM.
        self._db = sqlite3.connect('basenewtest.db')
        self._db.row_factory = sqlite3.Row

        # Create the basic contact table.
        
        # self._db.cursor().execute('''
        #     CREATE TABLE users(
        #     id INTEGER PRIMARY KEY,
        #     email TEXT,
        #     pass TEXT,
        #     is_admin TEXT,
        #     number INTEGER,
        #     polis INTEGER,
        #     name TEXT,
        #     surname TEXT,
        #     age INTEGER,
        #     priem BLOB,
        #     priemtime FLOAT
        #     )      
        # ''')
        # self._db.commit()
        
        # self._db.cursor().execute('''
        #     CREATE TABLE medics(
        #     id INTEGER PRIMARY KEY,
        #     name TEXT,
        #     surname TEXT,
        #     specialty TEXT,
        #     cabinet INTEGER
        #     )
        # ''')
        # self._db.commit()

        # self._db.cursor().execute('''
        #     CREATE TABLE priemtimes(
        #     id INTEGER PRIMARY KEY,
        #     medic_id INTEGER,
        #     time TEXT
        #     )        
        # ''')
        # self._db.commit()
        
        # self._db.cursor().execute('''
            # CREATE TABLE user_priems(
            # id INTEGER PRIMARY KEY,
            # user_id INTEGER,
            # priem TEXT
            # )                      
        # ''')
        # self._db.commit()
        
        # Current contact when editing.
        self.current_id = None

    def add(self, user):
        self._db.cursor().execute('''
            INSERT INTO users(email, pass)
            VALUES(:email, :pass)''',
                                  user)
        self._db.commit()
    
    def get_auth_info(self):
        return self._db.cursor().execute(
            "SELECT email, pass, id, is_admin from users").fetchall()

    def update_current(self, details):
        if self.current_id is None:
            self.add(details)
        else:
            self._db.cursor().execute('''
            UPDATE users SET email=:email, pass=:pass WHERE id=:id''',
                                                details)
            self._db.commit()
            
    def update_user(self, details):
        user_id = self.current_id
        self._db.cursor().execute('''
        UPDATE users SET name=:name, surname=:surname, number=:number, polis=:polis, age =:age WHERE id=:id''', details)
        self._db.commit()

    def get_summary(self):
        return self._db.cursor().execute(
            "SELECT email, name, surname, number, polis, age, id from users").fetchall()

    def get_user(self, user_id):
        return self._db.cursor().execute(
            "SELECT email, name, surname, number, polis, age from users WHERE id=:id", {"id": user_id}).fetchall()

    def get_current_user(self):
        if self.current_id is None:
            return {"email": "", "name": "", "surname": "", "number": "", "polis": "", "age": ""}
        else:
            return self.get_user(self.current_id)

    def get_medics_specialty(self):
        return self._db.cursor().execute(
            "SELECT specialty, id from medics").fetchall()
        
    def get_medic_name(self, medic_id):
        return self._db.cursor().execute(
            "SELECT name, surname, cabinet from medics WHERE id=:id", {"id": medic_id}).fetchall()
        
    def get_medic_time(self, medic_id):
        return self._db.cursor().execute(
            "SELECT time, id from priemtimes WHERE medic_id=:id and is_used = 0", {"id": medic_id}).fetchall()
        
    def get_medic_specialty(self, medic_id):
        return self._db.cursor().execute(
            "SELECT specialty from medics WHERE id=:id", {"id": medic_id}).fetchall()
        
    def get_medic_time_by_id(self, medic_id):
        return self._db.cursor().execute(
            "SELECT time from priemtimes WHERE medic_id=:id", {"id": medic_id}).fetchall()
    
    def make_appointment(self, priem):
        self._db.cursor().execute('''
            INSERT into user_priems(user_id, priem)
            VALUES(:user_id, :priem)''',
                                    priem)
        self._db.commit()
        
    def make_priemtime_is_used(self, priem_id):
        self._db.cursor().execute(
            "UPDATE priemtimes SET is_used = 1 WHERE id=:id", {"id": priem_id})
        self._db.commit()
            
    def get_appointments(self, user_id):
        return self._db.cursor().execute(
            "SELECT priem, id from user_priems WHERE user_id=:id", {"id": user_id}).fetchall()
    
    def get_users_list(self):
        return self._db.cursor().execute(
            "SELECT email, id from users WHERE is_admin IS NULL").fetchall()
    
    def admin_get_user(self, user_id):
        return self._db.cursor().execute(
            "SELECT * from users WHERE id=:id", {"id": user_id}).fetchone()
    
    def admin_get_current_user(self):
        if self.current_id is None:
            return {"email": "", "pass": "", "name": "", "surname": "", "number": "","polis": "","age": ""}
        else:
            return self.admin_get_user(self.current_id)
    
    def admin_add_user(self, user):
        self._db.cursor().execute('''
            INSERT INTO users(email, pass, name, surname, number, polis, age)
            VALUES(:email, :pass, :name, :surname, :number, :polis, :age)''',                      
                                    user)
        self._db.commit()
    
    def admin_update_current_user(self, details):
        if self.current_id is None:
            self.admin_add_user(details)
        else:
            self._db.cursor().execute('''
                UPDATE users SET email=:email, pass=:pass, name=:name,
                surname=:surname, number=:number, polis=:polis, age=:age WHERE id=:id''',
                                        details)
            self._db.commit()
    
    def delete_user(self, user_id):
        self._db.cursor().execute('''
            DELETE FROM users WHERE id=:id''', {"id": user_id})
        self._db.commit()
        
    def admin_get_medic(self, medic_id):
        return self._db.cursor().execute(
            "SELECT * from medics WHERE id=:id", {"id": medic_id}).fetchone()
    
    def admin_get_current_medic(self):
        if self.current_id is None:
            return {"name": "", "surname": "", "specialty": "", "cabinet": ""}
        else:
            return self.admin_get_medic(self.current_id)
    
    def admin_add_medic(self, medic):
        self._db.cursor().execute('''
            INSERT INTO medics(name, surname, specialty, cabinet)
            VALUES(:name, :surname, :specialty, :cabinet)''',                      
                                    medic)
        self._db.commit()

    def admin_update_current_medic(self, details):
        if self.current_id is None:
            self.admin_add_medic(details)
        else:
            self._db.cursor().execute('''
                UPDATE medics SET name=:name, surname=:surname, specialty=:specialty,
                cabinet=:cabinet WHERE id=:id''',
                                        details)
            self._db.commit()
    
    def delete_medic(self, medic_id):
        self._db.cursor().execute('''
            DELETE FROM medics WHERE id=:id''', {"id": medic_id})
        self._db.commit()
# class Greetings(Frame):
#     def __init__(self, screen, model):
#         super(LoginMenu, self).__init__(screen,
#                                         screen.height * 2 // 3,
#                                         screen.width * 2 // 3,
#                                         can_scroll=False,
#                                         )
#         self._model = model

#     def _next(self):
#         raise NextScene("LoginMenu")


class LoginMenu(Frame):
    def __init__(self, screen, model):
        super(LoginMenu, self).__init__(screen,
                                          screen.height * 2 // 2,
                                          screen.width * 2 // 3,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Вход",
                                          reduce_cpu=True)
        self._model = model

        layoutdiv = Layout([1])
        self.add_layout(layoutdiv)
        layoutdiv.add_widget(Divider(height=2, draw_line=False))
        layoutdiv.add_widget(Label(label="Госуслуги", align="^", height=1))
        layoutdiv.add_widget(Divider(height=5, draw_line=False))


        layout = Layout([30,30,30], fill_frame=True)
        self.add_layout(layout)

        self._email = Text("E-mail:", "email", max_length=20, validator=self._check_email, on_change=self._on_pick)
        self._pass = Text("Пароль:", "pass", hide_char='*', max_length=20, validator="^[a-zA-Z0-9]*$", on_change=self._on_pick)

        layout.add_widget(Divider(draw_line=False), 0)
        layout.add_widget(self._email, 1)
        layout.add_widget(self._pass, 1)
        layout.add_widget(Divider(draw_line=False), 2)
        self.fix()

        layout2 = Layout([1,1,1])
        self.add_layout(layout2)

        self._login_button = Button("Войти", self._login)

        layout2.add_widget(self._login_button, 1)
        layout2.add_widget(Button("Регистрация", self._reg), 0)
        layout2.add_widget(Button("Выйти", self._exit), 2)
        self.fix()
        self._on_pick

    def _on_pick(self):
        self._login_button.disabled = (self._email.is_valid is False) or (self._email.value == '') or (self._pass.value == '') or (self._pass.is_valid is False)

    def _login(self):
        self.save()
        self.itr = 0
        self.usrs = self._model.get_auth_info()
        for row in self.usrs:
            self.id = row[2]
            self.email = row[0]
            self.passw = row[1]
            self.is_admin = row[3]
            if (self.data["email"] == self.email) and (self.data["pass"] == self.passw):
                self.itr += 1
                if self.is_admin == '1':
                    raise NextScene("Admin panel")
                else:
                    self._model.current_id = self.id
                    raise NextScene("User Menu")
            if self.itr == 0:
                self._scene.add_effect(
                PopUpDialog(self._screen,
                            "Неверный email/пароль",
                            ["Ok"]))

    

    def _reg(self):
        self._model.current_id = None
        raise NextScene("Register")
    
    def _exit(self):
        self._scene.add_effect(
        PopUpDialog(self._screen,
                    "Вы уверены?",
                    ["Да", "Нет"],
                    on_close=self._quit_on_yes))
    
    @staticmethod
    def _check_email(value):
        m = re.match(r"^[a-zA-Z0-9_\-.]+@[a-zA-Z0-9_\-.]+\.[a-zA-Z0-9_\-.]+$",
                     value)
        return len(value) == 0 or m is not None
    
    @staticmethod
    def _quit_on_yes(selected):
        # Yes is the first button
        if selected == 0:
            raise StopApplication("User requested exit")

class RegisterMenu(Frame):
    def __init__(self, screen, model):
        super(RegisterMenu, self).__init__(screen,
                                        screen.height * 2 // 2,
                                        screen.width * 2 // 3,
                                        hover_focus=True,
                                        can_scroll=False,
                                        title="Регистрация",
                                        reduce_cpu=True)
        self._model = model

        layoutdiv = Layout([1])
        self.add_layout(layoutdiv)
        layoutdiv.add_widget(Label(label="Запись на прием", align="^", height=1))
        layoutdiv.add_widget(Divider(height=7, draw_line=False))

        self._email = Text("E-mail:", "email", max_length=20, validator=self._check_email, on_change=self._on_pick)
        self._pass = Text("Пароль:", "pass", hide_char='*', max_length=20, validator="^[a-zA-Z0-9]*$", on_change=self._on_pick)
        self._pass2 = Text("Повторите пароль:", "pass2", hide_char='*', max_length=20, validator="^[a-zA-Z0-9]*$", on_change=self._on_pick)

        layout = Layout([20,30,20], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Divider(draw_line=False), 0)
        layout.add_widget(self._email, 1)
        layout.add_widget(self._pass, 1)
        layout.add_widget(self._pass2, 1)
        layout.add_widget(Divider(draw_line=False), 2)
        self.fix()
        self._reg_button = Button("Зарегистрироваться", self._register)

        layout2 = Layout([1,1])
        self.add_layout(layout2)
        layout2.add_widget(self._reg_button, 0)
        layout2.add_widget(Button("Вернуться", self._return), 1)
        self.fix()
        self._on_pick
        #self._check

    def _on_pick(self):
        self._reg_button.disabled = (self._email.is_valid is False) or (self._email.value == '') or (self._pass.value == '') or (self._pass.is_valid is False) or (self._pass.value != self._pass2.value)
    
    def _register(self):
        self.save()
        self._model.update_current(self.data)
        raise NextScene("Login")
    
    def _return(self):

        raise NextScene("Login")
    
    @staticmethod
    def _check_email(value):
        m = re.match(r"^[a-zA-Z0-9_\-.]+@[a-zA-Z0-9_\-.]+\.[a-zA-Z0-9_\-.]+$",
                     value)
        return len(value) == 0 or m is not None


class UserMenu(Frame):
    def __init__(self, screen, model):
        super(UserMenu, self).__init__(screen,
                                        screen.height * 2 // 2,
                                        screen.width * 2 // 3,
                                        hover_focus=True,
                                        can_scroll=False,
                                        on_load=self._reload,
                                        title="Ваши данные",
                                        reduce_cpu=True)
        self._model = model

        layout = Layout([100], fill_frame=False)
        self.add_layout(layout)
        layout.add_widget(Divider(draw_line=False, height=1))
        layout.add_widget(Label(label="ГОСУСЛУГИ", align="^", height=1))

        layoutmain = Layout([1], fill_frame=True)
        self.add_layout(layoutmain)

        self._email = Text("E-mail:", "email", readonly=True)
        self._name = Text("Имя:", "name", readonly=True)
        self._surname = Text("Фамилия:", "surname", readonly=True)
        self._number = Text("Номер:", "number", readonly=True)
        self._polis = Text("Полис:", "polis", readonly=True)
        self._age = Text("Возраст:", "age", readonly=True)

        layoutmain.add_widget(Label(label="Ваши данные:", align="<"))
        layoutmain.add_widget(self._email)
        layoutmain.add_widget(self._name)
        layoutmain.add_widget(self._surname)
        layoutmain.add_widget(self._number)
        layoutmain.add_widget(self._polis)
        layoutmain.add_widget(self._age)
        layoutmain.add_widget(Divider())
        layoutmain.add_widget(Label("Ваши приемы:", align="<"), 0)
        self._appointments = ListBox(Widget.FILL_FRAME, options=self._model.get_appointments(self._model.current_id), add_scroll_bar=True)
        layoutmain.add_widget(self._appointments)
        layoutmain.add_widget(Divider())
        layoutbutton = Layout([1,1,1])
        self.add_layout(layoutbutton)
        layoutbutton.add_widget(Button("Выход", self._exit), 2)
        layoutbutton.add_widget(Button("Записаться к врачу", self._appointment), 1)
        layoutbutton.add_widget(Button("Изменение данных", self._change_data), 0)
        self.fix()      

    def _reload(self, new_value = None):
        self._appointments.options = self._model.get_appointments(self._model.current_id)
        self._appointments.value = new_value
        self._params = self._model.get_current_user()
        for row in self._params:
            self._email.value = row[0]
            self._name.value = row[1]
            self._surname.value = row[2]
            self._number.value = row[3]
            self._polis.value = row[4]
            self._age.value = row[5]
    
    def _appointment(self):
        raise NextScene("Make appointment")

    def _change_data(self):
        raise NextScene("User change data")

    @staticmethod
    def _exit():
        raise StopApplication("User press exit")

class UserChangeMenu(Frame):
    def __init__(self, screen, model):
        super(UserChangeMenu, self).__init__(screen,
                                        screen.height * 2 // 2,
                                        screen.width * 2 // 3,
                                        hover_focus=True,
                                        can_scroll=False,
                                        title="Изменение данных",
                                        reduce_cpu=True)
        self._model = model

        layout = Layout([100], fill_frame=False)
        self.add_layout(layout)
        layout.add_widget(Divider(draw_line=False, height=2))
        layout.add_widget(Label(label="ГОСУСЛУГИ", align="^", height=3))

        layoutmain = Layout([1], fill_frame=True)
        self.add_layout(layoutmain)
        self._name = Text("Имя:", "name", validator="^[a-zA-Zа-яА-Я]*$", on_change=self._on_pick)
        self._surname = Text("Фамилия:", "surname", validator="^[a-zA-Zа-яА-Я]*$", on_change=self._on_pick)
        self._number = Text("Номер:", "number", validator="^[0-9]*$", max_length=11, on_change=self._on_pick)
        self._polis = Text("Полис:", "polis", validator="^[0-9]*$", max_length=8, on_change=self._on_pick)
        self._age = Text("Возраст:", "age", validator="^[0-9]*$", max_length=2, on_change=self._on_pick)
        layoutmain.add_widget(Label(label="Введите данные:", align="<"),0)
        layoutmain.add_widget(self._name,0)
        layoutmain.add_widget(self._surname,0)
        layoutmain.add_widget(self._number, 0)
        layoutmain.add_widget(self._polis, 0)
        layoutmain.add_widget(self._age, 0)
        layoutbutton = Layout([1,1])
        self.add_layout(layoutbutton)
        self._save_return_button = Button("Сохранить", self._save_return)
        layoutbutton.add_widget(self._save_return_button, 0)
        layoutbutton.add_widget(Button("Не сохранять и выйти", self._dont_save_return), 1)
        
        self.fix()
    
    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(UserChangeMenu, self).reset()
        #self.data = self._model.get_current_contact()

    def _on_pick(self):
        self._save_return_button.disabled = (self._name.is_valid is False) or (self._name.value == '') or (self._surname.value == '') or (self._surname.is_valid is False) or (self._number.value == '') or (self._number.is_valid is False) or (self._polis.value == '') or (self._polis.is_valid is False) or (self._age.value == '') or (self._age.is_valid is False)
    

    def _save_return(self):
        self.save()
        self.data["id"] = self._model.current_id
        self._model.update_user(self.data)
        raise NextScene("User Menu")

    def _dont_save_return(self):
        raise NextScene("User Menu")

class MakeAppointment(Frame):
    def __init__(self, screen, model):
        super(MakeAppointment, self).__init__(screen,
                                        screen.height * 2 // 2,
                                        screen.width * 2 // 3,
                                        hover_focus=True,
                                        can_scroll=False,
                                        title="Запись к врачу",
                                        reduce_cpu=True)
        self._model = model

        layout = Layout([100], fill_frame=False)
        self.add_layout(layout)
        layout.add_widget(Divider(draw_line=False, height=2))
        layout.add_widget(Label(label="Запись", align="^", height=3))

        layoutmain = Layout([20,60,20],fill_frame=True)
        self.add_layout(layoutmain)
        layoutmain.add_widget(Divider(False, 1), 0)
        self._specialty_choose = DropdownList(label="Специализация", options=self._model.get_medics_specialty(), on_change=self._show_medic_name_and_cab, fit=True)
        layoutmain.add_widget(self._specialty_choose, 1)
        self._medic_name = Text(label="Ваш врач:", name="medic_name", readonly=True, max_length=30)
        layoutmain.add_widget(self._medic_name, 1)
        self._medic_cab = Text(label="Кабинет:", name="cab", readonly=True, max_length=3)
        layoutmain.add_widget(self._medic_cab, 1)
        layoutmain.add_widget(Divider(False, 1), 2)
        self._time_choose = DropdownList(label="Время", options=[("/Выберите врача/", 1)], fit=True)
        layoutmain.add_widget(self._time_choose, 1)
        #layoutmain.add_widget(self._medic_choose, 1)
        #layoutmain.add_widget(self._time_choose, 2)

        layoutbuttons = Layout([1,2])
        self.add_layout(layoutbuttons)
        self._make_appointment_button = Button("Записаться", self._make_appointment)
        self._return_button = Button("Выйти", self._return)
        layoutbuttons.add_widget(self._make_appointment_button, 0)
        layoutbuttons.add_widget(self._return_button, 1)
        self.fix()
        

    def _show_medic_name_and_cab(self):
        self.id = self._specialty_choose.value
        self.medic = self._model.get_medic_name(self.id)
        for row in self.medic:
            self.medic_name = row[0]
            self.medic_surname = row[1]
            self.medic_cab = row[2]
        self.medic_fullname = self.medic_name + ' ' + self.medic_surname
        self._medic_name.value = self.medic_fullname
        self._medic_cab.value = self.medic_cab
        self._time_choose.options = self._model.get_medic_time(self.id)
        
            
    
    def _make_appointment(self):
        self.save()
        self.id = self._specialty_choose.value
        self.specialty_temp = self._model.get_medic_specialty(self.id)
        for row in self.specialty_temp:
            self.specialty = row[0]
        self.time_temp = self._model.get_medic_time_by_id(self.id)
        for row in self.time_temp:
            self.time = row[0]
        self._appointment_text = self.specialty + ' ' + self.data["medic_name"] + ' в кабинете ' + self.data["cab"] + ' в ' + self.time
        self._appointment = {"user_id": self._model.current_id, "priem": self._appointment_text}
        self._model.make_priemtime_is_used(self._time_choose.value)
        self._model.make_appointment(self._appointment)
        raise NextScene("User Menu")
        

    def _return(self):
        raise NextScene("User Menu")
class AdminPanel(Frame):
    def __init__(self, screen, model):
        super(AdminPanel, self).__init__(screen,
                                        screen.height * 2 // 2,
                                        screen.width * 2 // 3,
                                        hover_focus=True,
                                        can_scroll=False,
                                        title="Админ-панель",
                                        reduce_cpu=True)
        self._model = model

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Divider(draw_line=False, height=2))
        layout.add_widget(Label(label="Добро пожаловать, администратор", align="^", height=3))
        

        layout_buttons = Layout([1,1,1,1])
        self.add_layout(layout_buttons)
        layout_buttons.add_widget(Button("Список юзеров", self._get_user_list), 0)
        layout_buttons.add_widget(Button("Cписок врачей", self._get_medic_list), 1)
        layout_buttons.add_widget(Button("Список доступных записей", self._get_priemtimes_list), 2)
        layout_buttons.add_widget(Button("Выйти", self._exit), 3)
        self.fix()
    def _get_user_list(self):
        raise NextScene("User list")
    
    def _get_medic_list(self):
        raise NextScene("Medic list")
    
    def _get_priemtimes_list(self):
        pass
    
    def _exit(self):
        self._scene.add_effect(
        PopUpDialog(self._screen,
                    "Вы уверены?",
                    ["Да", "Нет"],
                    on_close=self._quit_on_yes))
        
    @staticmethod
    def _quit_on_yes(selected):
        # Yes is the first button
        if selected == 0:
            raise StopApplication("User requested exit")

class UserList(Frame):
    def __init__(self, screen, model):
        super(UserList, self).__init__(screen,
                                    screen.height * 2 // 2,
                                    screen.width * 2 // 3,
                                    on_load=self._reload_list,
                                    hover_focus=True,
                                    can_scroll=False,
                                    title="Список юзеров",
                                    reduce_cpu=True)
        self._model = model
        
        layoutmain = Layout([100], fill_frame=True)
        self.add_layout(layoutmain)
        self._user_list = ListBox(
            Widget.FILL_FRAME,
            model.get_users_list(),
            name="users",
            add_scroll_bar=True,
            on_change=self._on_pick,
            on_select=self._edit)
        self._edit_button = Button("Редактировать", self._edit)
        self._delete_button = Button("Удалить", self._delete)
        layoutmain.add_widget(self._user_list)
        layoutmain.add_widget(Divider())
        layoutbuttons = Layout([1,1,1,1])
        self.add_layout(layoutbuttons)
        layoutbuttons.add_widget(Button("Создать", self._add), 0)
        layoutbuttons.add_widget(self._edit_button, 1)
        layoutbuttons.add_widget(self._delete_button, 2)
        layoutbuttons.add_widget(Button("Вернуться", self._quit), 3)
        self.fix()
        self._on_pick()
        
        
    def _on_pick(self):
        self._edit_button.disabled = self._user_list.value is None
        self._delete_button.disabled = self._user_list.value is None
    
    def _reload_list(self, new_value=None):
        self._user_list.options = self._model.get_users_list()
        self._user_list.value = new_value
        
    def _add(self):
        self._model.current_id = None
        raise NextScene("Edit user")
    
    def _edit(self):
        self.save()
        self._model.current_id = self.data["users"]
        raise NextScene("Edit user")
    
    def _delete(self):
        self.save()
        self._model.delete_user(self.data["users"])
        self._reload_list()
        
    @staticmethod  
    def _quit():
        raise NextScene("Admin panel")

class EditUser(Frame):
    def __init__(self, screen, model):
        super(EditUser, self).__init__(screen,
                                       screen.height * 2 // 2,
                                       screen.width * 2 // 3,
                                       hover_focus=True,
                                       can_scroll=False,
                                       title="Данные пользователя",
                                       reduce_cpu=True)
        self._model = model
        
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("E-mail:", "email"))
        layout.add_widget(Text("Пароль:", "pass"))
        layout.add_widget(Text("Имя:", "name"))
        layout.add_widget(Text("Фамилия:", "surname"))    
        layout.add_widget(Text("Номер:", "number"))
        layout.add_widget(Text("Полис:", "polis"))
        layout.add_widget(Text("Возраст:", "age"))
        layoutbuttons = Layout([1,1,1,1])
        self.add_layout(layoutbuttons)
        layoutbuttons.add_widget(Button("OK", self._ok), 0)
        layoutbuttons.add_widget(Button("Отмена", self._cancel), 3)
        self.fix()
        
    def reset(self):
        super(EditUser, self).reset()
        self.data = self._model.admin_get_current_user()
        
    def _ok(self):
        self.save()
        self._model.admin_update_current_user(self.data)
        raise NextScene("User list")
    
    @staticmethod
    def _cancel():
        raise NextScene("User list")

class MedicList(Frame):
    def __init__(self, screen, model):
        super(MedicList, self).__init__(screen,
                                    screen.height * 2 // 2,
                                    screen.width * 2 // 3,
                                    on_load=self._reload_list,
                                    hover_focus=True,
                                    can_scroll=False,
                                    title="Список врачей",
                                    reduce_cpu=True)
        self._model = model
        
        layoutmain = Layout([100], fill_frame=True)
        self.add_layout(layoutmain)
        self._medic_list = ListBox(
            Widget.FILL_FRAME,
            model.get_medics_specialty(),
            name="medics",
            add_scroll_bar=True,
            on_change=self._on_pick,
            on_select=self._edit)
        self._edit_button = Button("Редактировать", self._edit)
        self._delete_button = Button("Удалить", self._delete)
        layoutmain.add_widget(self._medic_list)
        layoutmain.add_widget(Divider())
        layoutbuttons = Layout([1,1,1,1])
        self.add_layout(layoutbuttons)
        layoutbuttons.add_widget(Button("Создать", self._add), 0)
        layoutbuttons.add_widget(self._edit_button, 1)
        layoutbuttons.add_widget(self._delete_button, 2)
        layoutbuttons.add_widget(Button("Вернуться", self._quit), 3)
        self.fix()
        self._on_pick()
        
        
    def _on_pick(self):
        self._edit_button.disabled = self._medic_list.value is None
        self._delete_button.disabled = self._medic_list.value is None
    
    def _reload_list(self, new_value=None):
        self._medic_list.options = self._model.get_medics_specialty()
        self._medic_list.value = new_value
        
    def _add(self):
        self._model.current_id = None
        raise NextScene("Edit medic")
    
    def _edit(self):
        self.save()
        self._model.current_id = self.data["medics"]
        raise NextScene("Edit medic")
    
    def _delete(self):
        self.save()
        self._model.delete_medic(self.data["medics"])
        self._reload_list()
        
    @staticmethod  
    def _quit():
        raise NextScene("Admin panel")

class EditMedic(Frame):
    def __init__(self, screen, model):
        super(EditMedic, self).__init__(screen,
                                       screen.height * 2 // 2,
                                       screen.width * 2 // 3,
                                       hover_focus=True,
                                       can_scroll=False,
                                       title="Данные врача",
                                       reduce_cpu=True)
        self._model = model
        
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("Имя:", "name"))
        layout.add_widget(Text("Фамилия:", "surname"))    
        layout.add_widget(Text("Специальность:", "specialty"))
        layout.add_widget(Text("Кабинет:", "cabinet"))
        layoutbuttons = Layout([1,1,1,1])
        self.add_layout(layoutbuttons)
        layoutbuttons.add_widget(Button("OK", self._ok), 0)
        layoutbuttons.add_widget(Button("Отмена", self._cancel), 3)
        self.fix()
        
    def reset(self):
        super(EditMedic, self).reset()
        self.data = self._model.admin_get_current_medic()
        
    def _ok(self):
        self.save()
        self._model.admin_update_current_medic(self.data)
        raise NextScene("Medic list")
    
    @staticmethod
    def _cancel():
        raise NextScene("Medic list")
                
def demo(screen, scene):
    scenes = [
        Scene([LoginMenu(screen, users)], -1, name="Login"),
        Scene([RegisterMenu(screen, users)], -1, name="Register"),
        Scene([UserMenu(screen, users)], -1, name="User Menu"),
        Scene([UserChangeMenu(screen, users)], -1, name="User change data"),
        Scene([MakeAppointment(screen, users)], -1, name="Make appointment"),
        Scene([AdminPanel(screen, users)], -1, name = "Admin panel"),
        Scene([UserList(screen, users)], -1, name = "User list"),
        Scene([EditUser(screen, users)], -1, name= "Edit user"),
        Scene([MedicList(screen, users)], -1, name="Medic list"),
        Scene([EditMedic(screen, users)], -1, name="Edit medic")
    ]
    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)

users = LoginModel()
last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene