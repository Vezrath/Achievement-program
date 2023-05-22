from tkinter import *
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from pprint import pprint

# TODO 1 - Create a GUI for the program
# Graphical user interface setup with tkinter
window = Tk()
window.config(width=1920, height=1080)

placeholder_sign = PhotoImage(file="./data/images/under_construction.png")
canvas = Canvas(width=800, height=600)
canvas.create_image(400, 300, image=placeholder_sign)
canvas.grid(column=0, row=0, columnspan=3)

# TODO 2 - Create databases for user information, for achievements to track (start with a log for times gym visited)

# user_db = sqlite3.connect("./data/databases/users.db")
# cur = user_db.cursor()

# ------------- Run once to create the user database and insert information there for testing --------------

# cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name varchar(250) NOT NULL UNIQUE, password varchar(250) "
#             "NOT NULL UNIQUE)")
# cur.execute("INSERT INTO users VALUES(1, 'Harri Moisala', 'password')")
# user_db.commit()
# ---------------------------------------------------------------------------------------------------
user_db = sqlite3.connect("./data/databases/users.db")
cur = user_db.cursor()


# Retrieve information from database
def check_info():
    """Checks database information, for code writers diagnostic purposes."""
    cur.execute("SELECT name,password FROM users")
    pprint(cur.fetchall())
    user_db.close()


def add_user():
    """Adds the new user to users database, hashes and salts the password"""
    hashed_and_salted_password = generate_password_hash(
        new_password.get(),
        "pbkdf2",
        salt_length=16)
    data = [(new_user.get(), hashed_and_salted_password)]
    cur.executemany(f"INSERT INTO users(name, password) VALUES(?, ?)", data)
    user_db.commit()
    check_info()


# TODO 3 - Add security for user information, hash and salt passwords (Mostly to show I can do this)
new_user = Entry()
new_user.insert(0, "New user")
new_user.grid(column=0, row=1)
new_password = Entry()
new_password.insert(0, "Password")
new_password.grid(column=1, row=1)
add_user_button = Button(text="Add new user", width=15, command=add_user)
add_user_button.grid(column=2, row=1)


# TODO 4 - Create GUI objects that the user can use to update achievement scores

# TODO 5 - Create a visual feedback on the GUI for every achievement (a bar to fill)

# TODO 6 - Possibly add tracking progress over time periods (weeks, months, years)

# TODO 7 - Add more achievements to track, create categories for achievements

# TODO 8 - Create a screensaver for fun (Amstrad like)

# TODO 9 - Check to use OOP when prudent


window.mainloop()
