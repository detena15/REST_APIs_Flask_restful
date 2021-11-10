import sqlite3

# Create the connection obj
con = sqlite3.connect('data.db')

# Create a cursor object to move inside the database
cursor = con.cursor()

# Create the query
create_table = "CREATE TABLE users (id int, username text, password text)"

# Execute the query
cursor.execute(create_table)

# Create a new user to send to the database
user = (1, 'edu', '123')

# Create the insert query
insert_q = "INSERT INTO users VALUES (?, ?, ?)"

# Execute the query, while passing the user
cursor.execute(insert_q, user)

users = [
    (2, 'duende', '456'),
    (3, 'minotauro', '789'),
    (4, 'Ra', '101')
]

# Allows you to execute the same query multiple times
cursor.executemany(insert_q, users)

select_q = "SELECT * FROM users"

for row in cursor.execute(select_q):
    print(row)

# Tell the bbdd to save the changes
con.commit()

# Close the connection
con.close()
