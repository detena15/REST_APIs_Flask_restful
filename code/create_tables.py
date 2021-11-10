import sqlite3

con = sqlite3.connect('data.db')

cursor = con.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"  # al usar INTEGER, se crea id de forma incremental

cursor.execute(create_table)

con.commit()

con.close()
