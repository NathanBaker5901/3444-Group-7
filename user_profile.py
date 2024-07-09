import sqlite3

class ProfileDB:
    @staticmethod
    def create_profile(username, bio, profile_pic):
        with sqlite3.connect('profiles.db') as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO profiles (username, bio, profile_pic) 
                VALUES (?, ?, ?)
            ''', (username, bio, profile_pic))
            conn.commit()

    @staticmethod
    def get_profile(username):
        with sqlite3.connect('profiles.db') as conn:
            c = conn.cursor()
            c.execute('''
                SELECT * FROM profiles WHERE username=?
            ''', (username,))
            return c.fetchone()

    @staticmethod
    def update_profile(username, bio, profile_pic):
        with sqlite3.connect('profiles.db') as conn:
            c = conn.cursor()
            if profile_pic:
                c.execute('''
                    UPDATE profiles SET bio=?, profile_pic=? WHERE username=?
                ''', (bio, profile_pic, username))
            else:
                c.execute('''
                    UPDATE profiles SET bio=? WHERE username=?
                ''', (bio, username))
            conn.commit()

    @staticmethod
    def ensure_profile_exists_for_all_users():
        with sqlite3.connect('profiles.db') as conn:
            c = conn.cursor()
            c.execute("SELECT username FROM users")
            users = c.fetchall()
            for user in users:
                username = user[0]
                c.execute("SELECT username FROM profiles WHERE username=?", (username,))
                profile = c.fetchone()
                if not profile:
                    c.execute("INSERT INTO profiles (username, bio, profile_pic) VALUES (?, '', '')", (username,))
            conn.commit()
            