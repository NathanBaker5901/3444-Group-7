import sqlite3

conn = sqlite3.connect('profiles.db')
cursor = conn.cursor()

# Check the columns in the profiles table
cursor.execute("PRAGMA table_info(profiles)")
columns = cursor.fetchall()
print(columns)

conn.close()
