import sqlite3
import socket
import json
import time
#nc = connect('localhost', 1111)

class LoginModel(object):
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 1111
        self.client_socket = socket.socket()
        self.client_socket.connect((self.host, self.port))
        self._db = sqlite3.connect('basenewtest.db')
        self._db.row_factory = sqlite3.Row

        self._db.cursor().execute('''
            CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            email TEXT,
            pass TEXT,
            is_admin TEXT,
            number INTEGER,
            polis INTEGER,
            name TEXT,
            surname TEXT,
            age INTEGER,
            priem BLOB,
            priemtime FLOAT
            )
        ''')
        self._db.commit()


        self._db.cursor().execute('''
            CREATE TABLE IF NOT EXISTS medics(
            id INTEGER PRIMARY KEY,
            name TEXT,
            surname TEXT,
            specialty TEXT,
            cabinet INTEGER
            )
        ''')
        self._db.commit()

        self._db.cursor().execute('''
            CREATE TABLE IF NOT EXISTS priemtimes(
            id INTEGER PRIMARY KEY,
            medic_id INTEGER,
            time TEXT
            )
        ''')
        self._db.commit()

        self._db.cursor().execute('''
        CREATE TABLE IF NOT EXISTS user_priems(
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        priem TEXT
        )
        ''')
        self._db.commit()

        # Current contact when editing.
        self.current_id = None
        self.current_time_id = None
    
    def collect_data(self, db_name, method, param):
        data = {"db_name": db_name, "method": method, "param": param}
        return json.dumps(data)

    def send(self, data):
        self.client_socket.send(data.encode())
        time.sleep(0.1)

    def receive(self):
        received_data = self.client_socket.recv(1024).decode()
        print(received_data)
        parsed_data = json.loads(received_data)
        return parsed_data

    def add(self, user_data):
        query = self.collect_data("users", "INSERT", user_data)
        self.send(query)

    def get_auth_info(self):
        auth_info = {"email": "", "password": "", "id": "", "is_admin": ""}
        data = self.collect_data("users", "SELECT email, pass, id, is_admin", auth_info)
        self.send(data)
        return self.receive()

    def update_current(self, details):
        if self.current_id is None:
            self.add(details)
        else:
            update_query = self.collect_data("users", "UPDATE SET email=:email, pass=:pass WHERE id=:id", details)
            self.send(update_query)

    def update_user(self, user_details):
        user_data = self.collect_data("users", "UPDATE SET name=:name, surname=:surname, number=:number, polis=:polis, age =:age WHERE id=:id", user_details)
        self.send(user_data)

    def get_summary(self):
        user_fields = {"email": "", "name": "", "surname": "", "number": "", "polis": "", "age": "", "id": ""}
        users = self.collect_data("users", "SELECT email, name, surname, number, polis, age, id", user_fields)
        self.send(users)
        return self.receive()
            

    def get_user(self, user_id):
        user = {"id": user_id, "email": "", "name": "", "surname": "", "number": "", "polis": "", "age": ""}
        query = self.collect_data("users", "SELECT email, name, surname, number, polis, age WHERE id=:id", user)
        self.send(query)
        return self.receive()
        
    def get_current_user(self):
        if self.current_id is None:
            return {"email": "", "name": "", "surname": "", "number": "", "polis": "", "age": ""}
        else:
            return self.get_user(self.current_id)

    def get_medics_specialty(self):
        query_params = {"specialty": "", "id": ""}
        query_result = self.collect_data("medics", "SELECT specialty, id", query_params)
        self.send(query_result)
        return self.receive()

    def get_medic_name(self, medic_id):
        medic_data = {"id": medic_id, "name:": "", "surname": "", "cabinet": ""}
        query = self.collect_data("medics", "SELECT name, surname, cabinet WHERE id=:id", medic_data)
        self.send(query)
        return self.receive()
        
    def get_medic_time(self, medic_id):
        medic_data = {"medic_id": medic_id, "is_used": 0, "time": "", "id": ""}
        query = self.collect_data("priemtimes", "SELECT time, id WHERE medic_id=:id and is_used = 0", medic_data)
        self.send(query)
        answer = self.receive()
        return [(i["time"], i["id"]) for i in answer]

    def get_medic_specialty(self, medic_id):
        specialty = {"id": medic_id, "specialty": ""}
        query = self.collect_data("medics", "SELECT specialty WHERE id=:id", specialty)
        self.send(query)
        return self.receive()

    def get_medic_time_by_id(self, medic_id):
        medeic_time = {"medic_id": str(medic_id), "time": ""}
        query = self.collect_data("priemtimes", "SELECT time WHERE medic_id=:id", medeic_time)
        self.send(query)
        return self.receive()
        
    def make_appointment(self, priem):
        appointment = {"user_id": priem["user_id"], "priem": priem["priem"]}
        query = self.collect_data("user_priems", "INSERT", appointment)
        self.send(query)
        

    def make_priemtime_is_used(self, priem_id):
        is_used = {"id": priem_id, "is_used": 1}
        query = self.collect_data("priemtimes", "UPDATE SET is_used = 1 WHERE id=:id", is_used)
        self.send(query)


    def get_appointments(self, user_id):
        appointments = {"user_id": user_id, "priem": "", "id": ""}
        query = self.collect_data("user_priems", "SELECT priem, id WHERE user_id=:id", appointments)
        self.send(query)
        return self.receive()
    
    def get_users_list(self):
        users_list = {"email": "", "id": ""}
        query = self.collect_data("users", "SELECT email, id", users_list)
        self.send(query)
        return self.receive()
        
    def admin_get_user(self, user_id):
        get_user = {"id": user_id, "email": "", "pass": "", "is_admin": "", "name": "", "surname": "", "number": "", "polis": "", "age": ""}
        query = self.collect_data("users", "SELECT * WHERE id=:id", get_user)
        self.send(query)
        return self.receive()
        
    def admin_get_current_user(self):
        if self.current_id is None:
            return {"email": "", "pass": "", "name": "", "surname": "", "number": "", "polis": "", "age": ""}
        else:
            return self.admin_get_user(self.current_id)

    def admin_add_user(self, user):
        add_user = {"email": user["email"], "pass": user["pass"], "name": user["name"], "surname": user["surname"], "number": user["number"], "polis": user["polis"], "age": user["age"]}
        query = self.collect_data("users", "INSERT", add_user)
        self.send(query)

    def admin_update_current_user(self, details):
        if self.current_id is None:
            self.admin_add_user(details)
        else:
            update_user = {"id": self.current_id, "email": details["email"], "pass": details["pass"], "name": details["name"], "surname": details["surname"], "number": details["number"], "polis": details["polis"], "age": details["age"]}
            query = self.collect_data("users", "UPDATE WHERE id=:id", update_user)
            self.send(query)

    def delete_user(self, user_id):
        delete = {"id": user_id}
        query = self.collect_data("users", "DELETE WHERE id=:id", delete)
        self.send(query)

    def admin_get_medic(self, medic_id):
        get_medic = {"id": medic_id, "name": "", "surname": "", "specialty": "", "cabinet": ""}
        query = self.collect_data("medics", "SELECT * WHERE id=:id", get_medic)
        self.send(query)
        return self.receive()
    
    def admin_get_current_medic(self):
        if self.current_id is None:
            return {"name": "", "surname": "", "specialty": "", "cabinet": ""}
        else:
            return self.admin_get_medic(self.current_id)

    def admin_add_medic(self, medic):
        add_medic = {"name": medic["name"], "surname": medic["surname"], "specialty": medic["specialty"], "cabinet": medic["cabinet"]}
        query = self.collect_data("medics", "INSERT", add_medic)
        self.send(query)

    def admin_update_current_medic(self, details):
        if self.current_id is None:
            self.admin_add_medic(details)
        else:
            update_medic = {"id": self.current_id, "name": details["name"], "surname": details["surname"], "specialty": details["specialty"], "cabinet": details["cabinet"]}
            query = self.collect_data("medics", "UPDATE WHERE id=:id", update_medic)
            self.send(query)

    def delete_medic(self, medic_id):
        delete = {"id": medic_id}
        query = self.collect_data("medics", "DELETE WHERE id=:id", delete)
        self.send(query)

    def admin_get_medic_time(self, medic_id):
        medic_time = {"medic_id": medic_id, "time": "", "id": ""}
        query = self.collect_data("priemtimes", "SELECT time, id WHERE medic_id=:id", medic_time)
        self.send(query)
        return self.receive()

    def admin_get_time(self, time_id):
        time = {"id": time_id, "medic_id": "", "time": "", "is_used": ""}
        query = self.collect_data("priemtimes", "SELECT * WHERE id=:id", time)
        self.send(query)
        return self.receive()
    
    def admin_get_current_time(self):
        if self.current_time_id is None:
            return {"time": "", "is_used": ""}
        else:
            return self.admin_get_time(self.current_time_id)

    def admin_add_time(self, time):
        time = {"medic_id": time["medic_id"], "time": time["time"], "is_used": time["is_used"]}
        query = self.collect_data("priemtimes", "INSERT", time)
        self.send(query)
        

    def admin_update_current_time(self, details):
        if self.current_id is None:
            self.admin_add_time(details)
        else:
            time = {"id": self.current_time_id, "medic_id": details["medic_id"], "time": details["time"], "is_used": details["is_used"]}
            query = self.collect_data("priemtimes", "UPDATE WHERE id=:id", time)
            self.send(query)

    def delete_time(self, time_id):
        time = {"id": time_id}
        query = self.collect_data("priemtimes", "DELETE WHERE id=:id", time)
        self.send(query)