import sqlite3 # This portions is for the importation of the sqlite3 module to work with the sqlite database

# Function to initialize the follow database
def init_follow_db():
    # Using context managaer to connect ti the SQL database with the name "profiles.db"
    # This will automatically commit and close connection
    with sqlite3.connect('follow.db') as conn:

        # Creates a curser object for database interactions
        c = conn.cursor()

        # Executes an SQL statement to make a table called "follows" if there is not one
        # Will contain 3 columns
        # "id" : integer that functions as primary key and increments automatically 
        # "follower_username" : houses follower username and cannot be null
        # "followee_username" : houses followeee username and cannot be null
        c.execute('''
            CREATE TABLE IF NOT EXISTS follows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                follower_username TEXT NOT NULL,
                followee_username TEXT NOT NULL,
                UNIQUE(follower_username, followee_username)
            )
        ''')
        # Commit changes to database
        conn.commit()

# If this script is run as the main module then call the init_follow_db function to initialize the database
if __name__ == '__main__':
    init_follow_db()