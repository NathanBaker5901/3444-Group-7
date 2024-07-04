import sqlite3

def init_profile_db():
    with sqlite3.connect('profiles.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                bio TEXT,
                profile_pic TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        conn.commit()

if __name__ == '__main__':
    init_profile_db()
