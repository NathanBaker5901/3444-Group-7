import sqlite3 # This portions is for the importation of the sqlite3 module to work with the sqlite database

# Function to initialize the profiles database
def init_profile_db():
    # Using context managaer to connect ti the SQL database with the name "profiles.db"
    # This will automatically commit and close connection
    with sqlite3.connect('profiles.db') as conn:

        # Creates a curser object for database interactions
        c = conn.cursor()

        # Executes an SQL statement to make a table called "profiles" if there is not one
        # Will contain 4 columns
        # "id" : integer that funstions as primary key and increments automatically 
        # "username" : This will house the user username and it cannot be null
        # "bio" : This is a text box the houses the user entered bio
        # "profile_pic" : Text field to store the URL path to the image *Work In Progress*
        c.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                bio TEXT,
                profile_pic TEXT
            )
        ''')
        # Commit the changes to database
        conn.commit()

# If this script is run as the main module then call the init_profile_db function to initialize the database
if __name__ == '__main__':
    init_profile_db()
