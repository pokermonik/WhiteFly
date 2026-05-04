# database.py
import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, surname TEXT)')
    conn.close()

def save_to_db(name, surname):
    conn = sqlite3.connect('users.db')
    conn.execute('INSERT INTO users VALUES (?, ?)', (name, surname))
    conn.commit()
    conn.close()