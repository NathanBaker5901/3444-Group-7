import sqlite3

class FollowDB:
    @staticmethod
    def follow_user(follower_username, followee_username):
        with sqlite3.connect('follow.db') as conn:
            c = conn.cursor()
            c.execute('''
                INSERT OR IGNORE INTO follows (follower_username, followee_username) 
                VALUES (?, ?)
            ''', (follower_username, followee_username))
            conn.commit()

    @staticmethod
    def unfollow_user(follower_username, followee_username):
        with sqlite3.connect('follow.db') as conn:
            c = conn.cursor()
            c.execute('''
                DELETE FROM follows WHERE follower_username=? AND followee_username=?
            ''', (follower_username, followee_username))
            conn.commit()

    @staticmethod
    def get_followers(username):
        with sqlite3.connect('follow.db') as conn:
            c = conn.cursor()
            c.execute('''
                SELECT follower_username FROM follows WHERE followee_username=?
            ''', (username,))
            return c.fetchall()

    @staticmethod
    def get_following(username):
        with sqlite3.connect('follow.db') as conn:
            c = conn.cursor()
            c.execute('''
                SELECT followee_username FROM follows WHERE follower_username=?
            ''', (username,))
            return c.fetchall()
# This function is used to get another users followers        
    @staticmethod
    def get_other_user_followers(username):
        with sqlite3.connect('follow.db') as conn:
            c = conn.cursor()
            c.execute('''
                SELECT COUNT(*) FROM follows WHERE followee_username=?
            ''', (username,))
            return c.fetchone()[0]

# This function is used to get another users following   
    @staticmethod
    def get_other_user_following(username):
        with sqlite3.connect('follow.db') as conn:
            c = conn.cursor()
            c.execute('''
                SELECT COUNT(*) FROM follows WHERE follower_username=?
            ''', (username,))
            return c.fetchone()[0]