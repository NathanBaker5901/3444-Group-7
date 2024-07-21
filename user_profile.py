import sqlite3 # Import the SQLite3 module to work with the SQLite database

# Class to interact with the profiles database
class ProfileDB:
    @staticmethod
    def create_profile(username, bio, profile_pic):
    # Using context managaer to connect ti the SQL database with the name "profiles.db"
    # This will automatically commit and close connection
        with sqlite3.connect('profiles.db') as conn:
            # Creates a curser object for database interactions
            c = conn.cursor()

            # Execute an SQL statement to insert a new profile into the "profiles" table
            # The values for "username, bio, and profile_pic" are provided to be parameters
            c.execute('''
                INSERT INTO profiles (username, bio, profile_pic) 
                VALUES (?, ?, ?)
            ''', (username, bio, profile_pic))

            # Commit changes to database
            conn.commit()

    @staticmethod
    def get_profile(username):
        # Connects using context managaer to the SQLite database named "profiles.db"
        with sqlite3.connect('profiles.db') as conn:

            # Creates a curser object for database interactions
            c = conn.cursor()

            # Execute an SQL statement that selects a profile from the "profiles" table
            # The profile is selected based on "username"
            c.execute('''
                SELECT * FROM profiles WHERE username=?
            ''', (username,))

            # This returns the first row of the result
            return c.fetchone()

    @staticmethod
    def update_profile(username, bio, profile_pic):
        # Connects using context managaer to the SQLite database named "profiles.db"
        with sqlite3.connect('profiles.db') as conn:
            
            # Creates a curser object for database interactions
            c = conn.cursor()

            # Checks if "profile_pic" is provided
            if profile_pic:
                # If "profile_pic" is provided, update both "bio" and "profile_pic" for the given "username" *Work in Progress*
                c.execute('''
                    UPDATE profiles SET bio=?, profile_pic=? WHERE username=?
                ''', (bio, profile_pic, username))
            else:
                # If "profile_pic" is not provided, update only "bio" for the given "username" *Work in Progress*
                c.execute('''
                    UPDATE profiles SET bio=? WHERE username=?
                ''', (bio, username))

            # Commit changes to database
            conn.commit()

    @staticmethod
    def ensure_profile_exists_for_all_users():
        # Connects using context managaer to the SQLite database named "profiles.db"
        with sqlite3.connect('profiles.db') as conn:
            
            # Creates a curser object for database interactions
            c = conn.cursor()

            # Execute an SQL statement to select all usernames from the "users" table
            c.execute("SELECT username FROM users")

            # Fetch all results as a list of tuples
            users = c.fetchall()

            # This will Iterate through each user in list
            for user in users:
                # Gets the username from the tuple
                username = user[0]

                # Checking if a profile exists for the given username
                c.execute("SELECT username FROM profiles WHERE username=?", (username,))
                profile = c.fetchone()

                # If no profile exists this will create a default profile with an empty "bio" and "profile_pic" *Profile pic in progress*
                if not profile:
                    c.execute("INSERT INTO profiles (username, bio, profile_pic) VALUES (?, '', '')", (username,))

            # Commit the changes to the database
            conn.commit()
            