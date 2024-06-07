import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

# Check if the users table exists
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
table_exists = c.fetchone()

if table_exists:
    print("Table 'users' exists.")
else:
    print("Table 'users' does not exist.")

conn.close()
