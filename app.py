from flask import Flask, request, render_template, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

def check_user(email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()
    conn.close()
    return user

def create_user(username, email, password):
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        return "User created successfully"
    except sqlite3.IntegrityError:
        return "Username or email already exists"
    finally:
        conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = check_user(email, password)
        if user:
            return redirect(url_for('mainMenu'))
        else:
            flash("Invalid credentials", "danger")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        message = create_user(username, email, password)
        if message == "User created successfully":
            flash(message, "info")
            return redirect(url_for('mainMenu'))
        else:
            flash(message, "danger")
            return redirect(url_for('register'))
    return render_template('createUser.html')

@app.route('/mainMenu')
def mainMenu():
    return render_template('mainMenu.html')

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/update_delete')
def update_delete():
    return render_template('Update_Delete.html')

@app.route('/show_collectable')
def show_collectable():
    return render_template('showColletable.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/profile')
def profile():
    return render_template('userProfile.html')

@app.route('/signout')
def signout():
    session.pop('userID', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
