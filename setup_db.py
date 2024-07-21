import sqlite3 # This portions is for the importation of the sqlite3 module to work with the sqlite database

# Connect to the database "users.db" or create if it does not exist
conn = sqlite3.connect('users.db')

# Creates a curser object for database interactions
c = conn.cursor()

# Executes an SQL statement to make a table called "users" if there is not one
# Will contain 4 columns
# "id" : integer that funstions as primary key and increments automatically 
# "username" : This will house the user username and it cannot be null
# "email" : This will house the user email and cannot be null
# "password" : This houses the user made password and cannot be null
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, 
              username TEXT UNIQUE NOT NULL, 
              email TEXT UNIQUE NOT NULL, 
              password TEXT NOT NULL)''')

#These are not necessary due to the script doing it autamatically but i read that it is best practice
# Commits changes to the database
conn.commit()
# Close the connection to the database
conn.close()
