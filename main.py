import tkinter.messagebox
from tkinter import *
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from pprint import pprint
from functools import partial

CURRENT_USER = 'Mina'

# TODO 1 - Create a GUI for the program
# Graphical user interface setup with tkinter
window = Tk()
window.config(width=1920, height=1080)

start_image = PhotoImage(file="./data/images/under_construction.png")
total_points_image = PhotoImage(file="./data/images/total_points.png")
points_by_category_image = PhotoImage(file="./data/images/points_by_category.png")
point_details_image = PhotoImage(file="./data/images/point_details.png")
canvas = Canvas(width=800, height=600)
GUI_image = canvas.create_image(400, 300, image=start_image)
canvas.grid(column=0, row=0, columnspan=4, padx=20, pady=20)

# TODO 2 - Create databases for user information, for achievements to track (start with a log for times gym visited)

user_db = sqlite3.connect("./data/databases/users.db")
cur = user_db.cursor()


# ------------- Run once to create the databases and insert information there for testing -----------

# cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name varchar(250) NOT NULL UNIQUE, password varchar(250) "
#             "NOT NULL UNIQUE)")
# cur.execute("INSERT INTO users VALUES(1, 'Harri Moisala', 'password')")
# user_db.commit()
# ---------------------------------------------------------------------------------------------------
# cur.execute("CREATE TABLE categories (id INTEGER PRIMARY KEY, name varchar(250) NOT NULL UNIQUE, total INTEGER,"
#             " clean_living INTEGER, studies INTEGER, gym_visits INTEGER, jobs INTEGER)")
# ---------------------------------------------------------------------------------------------------
# Delete all rows from database
# user_db = sqlite3.connect("./data/databases/users.db")
# cur = user_db.cursor()
# cur.execute("DELETE FROM users")
# cur.execute("DELETE FROM categories")
# user_db.commit()


def check_info():
    """Checks database information, for code writers diagnostic purposes."""
    cur.execute("SELECT name,password FROM users")
    pprint(cur.fetchall())
    # user_db.close()


# TODO 11 What if username or password already exists? contingency plan,
#  Should the program automatically log the new user in?
def add_user():
    """Adds the new user to users database, hashes and salts the password, creates starting info for points table"""
    user = new_user.get()
    password = new_password.get()
    if len(password) < 10:
        tkinter.messagebox.showwarning(title="Password is too short.", message="Please insert at least 10 characters "
                                                                               "for your password.")
    else:
        hashed_and_salted_password = generate_password_hash(
            password,
            "pbkdf2",
            salt_length=16)
        user_data = [(user, hashed_and_salted_password)]
        points_data = [(user, 0, 0, 0, 0, 0)]
        cur.executemany(f"INSERT INTO users(name, password) VALUES(?, ?)", user_data)
        cur.executemany(f"INSERT INTO categories(name, total, clean_living, studies, gym_visits, jobs)"
                        f" VALUES(?, ?, ?, ?, ?, ?)", points_data)
        user_db.commit()
        check_info()


def login_user():
    """Logs the user in if the username and password match the ones in the users database."""
    global CURRENT_USER
    username = login_user_entry.get()
    password = user_password.get()
    data = cur.execute(f"SELECT password FROM users WHERE name=?", (username,))
    hashed_password = data.fetchall()[0][0]
    if check_password_hash(hashed_password, password):
        canvas.itemconfig(GUI_image, image=total_points_image)
        categories_button = Button(text="Details by category", width=20, command=show_categories)
        categories_button.grid(column=1, row=2)
        CURRENT_USER = username


def show_categories():
    """Shows achievement points by category."""
    category_details_with_arg = [partial(category_details, "total"),
                                 partial(category_details, "clean_living"),
                                 partial(category_details, "studies"),
                                 partial(category_details, "gym_visits"),
                                 partial(category_details, "jobs"),
                                 ]
    canvas.itemconfig(GUI_image, image=points_by_category_image)
    clean_living_button = Button(text="details", command=category_details_with_arg[1])
    clean_living_button.grid(column=0, row=1)
    studies_button = Button(text="details", command=category_details_with_arg[2])
    studies_button.grid(column=1, row=1)
    gym_visits_button = Button(text="details", command=category_details_with_arg[3])
    gym_visits_button.grid(column=2, row=1)
    jobs_button = Button(text="details", command=category_details_with_arg[4])
    jobs_button.grid(column=3, row=1)


def category_details(category):
    """Shows point details in a single category."""
    canvas.itemconfig(GUI_image, image=point_details_image)
    points_in_category = cur.execute(f"SELECT {category} FROM categories WHERE name=?", (CURRENT_USER,))
    print(points_in_category.fetchall()[0][0])

    add_points_entry.grid(column=1, row=5, pady=10)
    add_points_button = Button(text="Click to add points", command=partial(add_points, category))
    add_points_button.grid(column=2, row=5, pady=10)


# Updates data in the database PLACEHOLDER STUFF
# data_2 = (220, 15, 30, 200, CURRENT_USER)
# cur.execute("UPDATE categories SET total = ?, clean_living = ?, gym_visits = ?, jobs = ? WHERE name = ?", data_2)
# user_db.commit()


# TODO 12 Remove buttons when going upwards in the database hierarchy, update current category(make a global variable)
# button_forget.grid() (removes grid configuration) or button_grid_remove() (keeps config -> can call .grid() again
# without arguments

def add_points(category):
    """Updates the added points to the database"""
    points_to_add = add_points_entry.get()
    if tkinter.messagebox.askokcancel(title="Confirm point addition",
                                      message=f"This will add {points_to_add} points to {category}."):
        old_points = cur.execute(f"SELECT {category} FROM categories WHERE name = ?", (CURRENT_USER,)).fetchall()[0][0]
        new_points = int(old_points) + int(points_to_add)
        data = [str(new_points), CURRENT_USER]
        cur.execute(f"UPDATE categories SET {category} = ? WHERE name = ?", data)

        old_total_points = cur.execute(f"SELECT total FROM categories WHERE name = ?", (CURRENT_USER,)).fetchall()[0][0]
        new_total_points = int(old_total_points + int(points_to_add))
        data_2 = [str(new_total_points), CURRENT_USER]
        cur.execute(f"UPDATE categories SET total = ? WHERE name = ?", data_2)

        user_db.commit()


# Entries and buttons for registering new users
new_user = Entry()
new_user.insert(0, "New user")
new_user.grid(column=0, row=3, pady=20, padx=20)
new_password = Entry()
new_password.insert(0, "Password")
new_password.grid(column=1, row=3, padx=20, pady=20)
add_user_button = Button(text="Add new user", width=15, command=add_user)
add_user_button.grid(column=2, row=3, padx=20, pady=20)

# Entries and buttons for logging in registered users.
login_user_entry = Entry()
login_user_entry.insert(0, "Mina")
login_user_entry.grid(column=0, row=4)
user_password = Entry()
user_password.insert(0, "qwertyqwerty")
user_password.grid(column=1, row=4)
login_button = Button(text="Login user", width=15, command=login_user)
login_button.grid(column=2, row=4)

# TESTING---------------------------------
add_points_entry = Entry()


# TODO 5 - Create a visual feedback on the GUI for every achievement (a bar to fill)

# TODO 6 - Possibly add tracking progress over time periods (weeks, months, years)


# TODO 8 - Create a screensaver for fun (Amstrad like)

# TODO 9 - Check to use OOP when prudent

window.mainloop()
