from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
import sys

import frames
import db



def demo(screen, scene):
    scenes = [
        Scene([frames.LoginMenu(screen, gosuslugi_db)], -1, name="Login"),
        Scene([frames.RegisterMenu(screen, gosuslugi_db)], -1, name="Register"),
        Scene([frames.UserMenu(screen, gosuslugi_db)], -1, name="User Menu"),
        Scene([frames.UserChangeMenu(screen, gosuslugi_db)], -1, name="User change data"),
        Scene([frames.MakeAppointment(screen, gosuslugi_db)], -1, name="Make appointment"),
        Scene([frames.AdminPanel(screen, gosuslugi_db)], -1, name = "Admin panel"),
        Scene([frames.UserList(screen, gosuslugi_db)], -1, name = "User list"),
        Scene([frames.EditUser(screen, gosuslugi_db)], -1, name= "Edit user"),
        Scene([frames.MedicList(screen, gosuslugi_db)], -1, name="Medic list"),
        Scene([frames.EditMedic(screen, gosuslugi_db)], -1, name="Edit medic"),
        Scene([frames.PriemsList(screen, gosuslugi_db)], -1, name="Priems list"),
        Scene([frames.EditTime(screen, gosuslugi_db)], -1, name="Edit time")
    ]
    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)

gosuslugi_db = db.LoginModel()
last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene