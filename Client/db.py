import sqlite3


class LoginModel(object):
    def __init__(self):
        self._db = sqlite3.connect('basenewtest.db')
        self._db.row_factory = sqlite3.Row

        #self._db.cursor().execute('''
        #    CREATE TABLE users(
        #    id INTEGER PRIMARY KEY,
        #    email TEXT,
        #    pass TEXT,
        #    is_admin TEXT,
        #    number INTEGER,
        #    polis INTEGER,
        #    name TEXT,
        #    surname TEXT,
        #    age INTEGER,
        #    priem BLOB,
        #    priemtime FLOAT
        #    )
        #''')
        #self._db.commit()
        #
        #self._db.cursor().execute('''
        #    CREATE TABLE medics(
        #    id INTEGER PRIMARY KEY,
        #    name TEXT,
        #    surname TEXT,
        #    specialty TEXT,
        #    cabinet INTEGER
        #    )
        #''')
        #self._db.commit()
        #
        #self._db.cursor().execute('''
        #    CREATE TABLE priemtimes(
        #    id INTEGER PRIMARY KEY,
        #    medic_id INTEGER,
        #    time TEXT
        #    )
        #''')
        #self._db.commit()
        #
        #self._db.cursor().execute('''
        #CREATE TABLE user_priems(
        #id INTEGER PRIMARY KEY,
        #user_id INTEGER,
        #priem TEXT
        #)
        #''')
        #self._db.commit()

        # Current contact when editing.
        self.current_id = None
        self.current_time_id = None

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
        self._db.cursor().execute('''
        UPDATE users SET name=:name, surname=:surname, number=:number, polis=:polis, age =:age WHERE id=:id''', details)
        self._db.commit()

    def get_summary(self):
        return self._db.cursor().execute(
            "SELECT email, name, surname, number, polis, age, id from users").fetchall()

    def get_user(self, user_id):
        return self._db.cursor().execute(
            "SELECT email, name, surname, number, polis, age from users WHERE id=:id", {"id": user_id}).fetchone()

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
            return {"email": "", "pass": "", "name": "", "surname": "", "number": "", "polis": "", "age": ""}
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

    def admin_get_medic_time(self, medic_id):
        return self._db.cursor().execute(
            "SELECT time, id from priemtimes WHERE medic_id=:id", {"id": medic_id}).fetchall()

    def admin_get_time(self, time_id):
        return self._db.cursor().execute(
            "SELECT * from priemtimes WHERE id=:id", {"id": time_id}).fetchone()

    def admin_get_current_time(self):
        if self.current_time_id is None:
            return {"time": "", "is_used": ""}
        else:
            return self.admin_get_time(self.current_time_id)

    def admin_add_time(self, time):
        self._db.cursor().execute('''
            INSERT INTO priemtime(medic_id, time, is_used)
            VALUES(:medic_id, :time, :is_used)''',
                                  time)
        self._db.commit()

    def admin_update_current_time(self, details):
        if self.current_id is None:
            self.admin_add_time(details)
        else:
            self._db.cursor().execute('''
                UPDATE priemtimes SET medic_id=:medic_id, time=:time, is_used=:is_used WHERE id=:id''', details)
            self._db.commit()

    def delete_time(self, time_id):
        self._db.cursor().execute('''
            DELETE FROM priemtimes WHERE id=:id''', {"id": time_id})
        self._db.commit()
