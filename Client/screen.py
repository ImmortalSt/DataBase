from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, \
    Button, TextBox, Widget, Label, DatePicker, DropdownList, CheckBox, PopUpDialog
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText

import sys
import re
import sqlite3

# в базе уже есть один юзер для проверки - test@mail.com:qwerty

class LoginModel(object):
    def __init__(self):
        # Create a database in RAM.
        self._db = sqlite3.connect('base2.db')
        self._db.row_factory = sqlite3.Row

        # Create the basic contact table.
        
        # self._db.cursor().execute('''
        #     CREATE TABLE users(
        #     id INTEGER PRIMARY KEY,
        #     email TEXT,
        #     pass TEXT)
            
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
    
    def get_contact(self, user_id):
        return self._db.cursor().execute(
            "SELECT * from users WHERE id=:id", {"id": user_id}).fetchone()

    def update_current(self, details):
        if self.current_id is None:
            self.add(details)
        else:
            self._db.cursor().execute('''
            UPDATE users SET email=:email, pass=:pass WHERE id=:id''',
                                                details)
            


    def get_summary(self):
        return self._db.cursor().execute(
            "SELECT email, pass, id from users").fetchall()

    def get_contact(self, contact_id):
        return self._db.cursor().execute(
            "SELECT * from users WHERE id=:id", {"id": contact_id}).fetchone()

    # def get_current_contact(self):
    # if self.current_id is None:
    #     return {"name": "", "address": "", "phone": "", "email": "", "notes": ""}
    # else:
    #     return self.get_contact(self.current_id)

    # def delete_contact(self, contact_id):
    # self._db.cursor().execute('''
    #     DELETE FROM contacts WHERE id=:id''', {"id": contact_id})
    # self._db.commit()

class Greetings(Frame):
    def __init__(self, screen, model):
        super(LoginMenu, self).__init__(screen,
                                        screen.height * 2 // 3,
                                        screen.width * 2 // 3,
                                        can_scroll=False,
                                        )
        self._model = model

    def _next(self):
        raise NextScene("LoginMenu")


class LoginMenu(Frame):
    def __init__(self, screen, model):
        super(LoginMenu, self).__init__(screen,
                                          screen.height * 2 // 2,
                                          screen.width * 2 // 3,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Login menu",
                                          reduce_cpu=True)
        self._model = model

        layoutdiv = Layout([1])
        self.add_layout(layoutdiv)
        layoutdiv.add_widget(Label(label="Запись на прием", align="^", height=1))
        layoutdiv.add_widget(Divider(height=7, draw_line=False))


        layout = Layout([30,30,30], fill_frame=True)
        self.add_layout(layout)

        self._email = Text("E-mail:", "email", max_length=20, validator=self._check_email, on_change=self._on_pick)
        self._pass = Text("Password:", "pass", hide_char='*', max_length=20, validator="^[a-zA-Z0-9]*$", on_change=self._on_pick)

        layout.add_widget(Divider(draw_line=False), 0)
        layout.add_widget(self._email, 1)
        layout.add_widget(self._pass, 1)
        layout.add_widget(Divider(draw_line=False), 2)
        self.fix()

        layout2 = Layout([1,1,1])
        self.add_layout(layout2)

        self._login_button = Button("Login", self._login)

        layout2.add_widget(self._login_button, 1)
        layout2.add_widget(Button("Register", self._reg), 0)
        layout2.add_widget(Button("Exit", self._exit), 2)
        self.fix()
        self._on_pick

    def _on_pick(self):
        self._login_button.disabled = (self._email.is_valid is False) or (self._email.value == '') or (self._pass.value == '') or (self._pass.is_valid is False)

    def _login(self):
        self.save()
        self.writen_email = self.data["email"]
        self.written_pass = self.data["pass"]
        self.itr = 0
        self.usrs = self._model.get_summary()
        for row in self.usrs:
            self.id = row[2]
            self.email = row[0]
            self.passw = row[1]
            if (self.writen_email == self.email) and (self.written_pass == self.passw):
                self.itr += 1
                raise NextScene("User Menu")
            if self.itr == 0:
                self._scene.add_effect(
                PopUpDialog(self._screen,
                            "Incorrect email/pass",
                            ["Ok"]))

        

    
    def _reg(self):
        self._model.current_id = None
        raise NextScene("Register")
    
    def _exit(self):
        self._scene.add_effect(
        PopUpDialog(self._screen,
                    "Are you sure?",
                    ["Yes", "No"],
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
                                        title="Register menu",
                                        reduce_cpu=True)
        self._model = model

        layoutdiv = Layout([1])
        self.add_layout(layoutdiv)
        layoutdiv.add_widget(Label(label="Запись на прием", align="^", height=1))
        layoutdiv.add_widget(Divider(height=7, draw_line=False))

        self._email = Text("E-mail:", "email", max_length=20, validator=self._check_email, on_change=self._on_pick)
        self._pass = Text("Password:", "pass", hide_char='*', max_length=20, validator="^[a-zA-Z0-9]*$", on_change=self._on_pick)
        self._pass2 = Text("Re-enter Pass:", "pass2", hide_char='*', max_length=20, validator="^[a-zA-Z0-9]*$", on_change=self._on_pick)

        layout = Layout([20,30,20], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Divider(draw_line=False), 0)
        layout.add_widget(self._email, 1)
        layout.add_widget(self._pass, 1)
        layout.add_widget(self._pass2, 1)
        layout.add_widget(Divider(draw_line=False), 2)
        self.fix()
        self._reg_button = Button("Register", self._register)

        layout2 = Layout([1,1])
        self.add_layout(layout2)
        layout2.add_widget(self._reg_button, 0)
        layout2.add_widget(Button("Return", self._return), 1)
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
                                        title="User Menu",
                                        reduce_cpu=True)
        self._model = model

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Label(label="WELCOME TO MOZGOPRAWWW", align="^", height=1))
        layoutbutton = Layout([1,1])
        self.add_layout(layoutbutton)
        layoutbutton.add_widget(Button("Exit", self._exit), 0)
        layoutbutton.add_widget(Button("click", self._click), 1)
        self.fix()

    def _click(self):
        pass

    @staticmethod
    def _exit():
        raise StopApplication("User press exit")

def demo(screen, scene):
    scenes = [
        Scene([LoginMenu(screen, users)], -1, name="Login"),
        Scene([RegisterMenu(screen, users)], -1, name="Register"),
        Scene([UserMenu(screen, users)], -1, name="User Menu")
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