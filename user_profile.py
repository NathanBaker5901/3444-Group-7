import sqlite3

class ProfileDB:
    @staticmethod
    def create_profile(user_id, bio, profile_pic):
        with sqlite3.connect('profiles.db') as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO profiles (user_id, bio, profile_pic) 
                VALUES (?, ?, ?)
            ''', (user_id, bio, profile_pic))
            conn.commit()

    @staticmethod
    def get_profile(user_id):
        with sqlite3.connect('profiles.db') as conn:
            c = conn.cursor()
            c.execute('''
                SELECT * FROM profiles WHERE user_id=?
            ''', (user_id,))
            return c.fetchone()

    @staticmethod
    def update_profile(user_id, bio, profile_pic):
        with sqlite3.connect('profiles.db') as conn:
            c = conn.cursor()
            if profile_pic:
                c.execute('''
                    UPDATE profiles SET bio=?, profile_pic=? WHERE user_id=?
                ''', (bio, profile_pic, user_id))
            else:
                c.execute('''
                    UPDATE profiles SET bio=? WHERE user_id=?
                ''', (bio, user_id))
            conn.commit()
