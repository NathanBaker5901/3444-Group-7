import sqlite3

def verify_profile_db():
    conn = sqlite3.connect('profiles.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='profiles';")
    result = c.fetchone()
    if result:
        print("Table 'profiles' exists.")
    else:
        print("Table 'profiles' does not exist.")
    conn.close()

if __name__ == '__main__':
    verify_profile_db()
