import sqlite3

def init_profile_db():
    with sqlite3.connect('profiles.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                bio TEXT,
                profile_pic TEXT
            )
        ''')
        conn.commit()

if __name__ == '__main__':
    init_profile_db()
