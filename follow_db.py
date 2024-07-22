import sqlite3 # This portions is for the importation of the sqlite3 module to work with the sqlite database

# Class to interact with the follows database
class FollowDB:
    @staticmethod
    def follow_user(follower_username, followee_username):
        # Using context managaer to connect to the SQL database with the name "follow.db"
        # This will automatically commit and close connection
        with sqlite3.connect('follow.db') as conn:

            # Creates a curser object for database interactions
            c = conn.cursor()

            # Executes a SQL statement that inserts a new follow into follows table
            #"INSERT OR IGNORE" used to ignore duplicate entries
            c.execute('''
                INSERT OR IGNORE INTO follows (follower_username, followee_username) 
                VALUES (?, ?)
            ''', (follower_username, followee_username))

            # Commit the changes to database
            conn.commit()

    @staticmethod
    def unfollow_user(follower_username, followee_username):

        # Using context managaer to connect to the SQL database with the name "follow.db"
        with sqlite3.connect('follow.db') as conn:

            # Creates a curser object for database interactions
            c = conn.cursor()

            # Executes a SQL statement that deletes a follow from the follows table
            c.execute('''
                DELETE FROM follows WHERE follower_username=? AND followee_username=?
            ''', (follower_username, followee_username))

            # Commit the changes to database
            conn.commit()

    @staticmethod
    def get_followers(username):
        # Using context managaer to connect to the SQL database with the name "follow.db"
        with sqlite3.connect('follow.db') as conn:

            # Creates a curser object for database interactions
            c = conn.cursor()

            # Executes a SQL statement that gets all the followers of a specified user
            # Followers = followee_username
            c.execute('''
                SELECT follower_username FROM follows WHERE followee_username=?
            ''', (username,))

            # Returns rows from result as list of tuples
            return c.fetchall()

    @staticmethod
    def get_following(username):
        # Using context managaer to connect to the SQL database with the name "follow.db"
        with sqlite3.connect('follow.db') as conn:

            # Creates a curser object for database interactions
            c = conn.cursor()

            # Executes a SQL statement that selects all followees of a specific user
            # followees = follower_username           
            c.execute('''
                SELECT followee_username FROM follows WHERE follower_username=?
            ''', (username,))

            # Returns rows from result as list of tuples
            return c.fetchall()
        
# This function is used to get another users follower count       
    @staticmethod
    def get_other_user_followers(username):
        # Using context managaer to connect to the SQL database with the name "follow.db"
        with sqlite3.connect('follow.db') as conn:

            # Creates a curser object for database interactions
            c = conn.cursor()

            # Executes a SQL statement that counts the number of followers for a specific user
            # followers = followee_username
            c.execute('''
                SELECT COUNT(*) FROM follows WHERE followee_username=?
            ''', (username,))

            # Return follower count
            return c.fetchone()[0]

# This function is used to get another users following count 
    @staticmethod
    def get_other_user_following(username):
        # Using context managaer to connect to the SQL database with the name "follow.db"
        with sqlite3.connect('follow.db') as conn:

            # Creates a curser object for database interactions
            c = conn.cursor()

            # Executes a SQL statement that counts the number of followees for a specific user
            # followee = follower_username
            c.execute('''
                SELECT COUNT(*) FROM follows WHERE follower_username=?
            ''', (username,))

            # Return followee count
            return c.fetchone()[0]