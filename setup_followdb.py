import sqlite3

def init_follow_db():
    with sqlite3.connect('follow.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS follows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                follower_username TEXT NOT NULL,
                followee_username TEXT NOT NULL,
                UNIQUE(follower_username, followee_username)
            )
        ''')
        conn.commit()

if __name__ == '__main__':
    init_follow_db()