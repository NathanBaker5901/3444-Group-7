from flask import Flask, request, render_template, redirect, url_for, flash, session
import sqlite3
import os #for uploading files
from werkzeug.utils import secure_filename #for securing the files making sure theres no dangerous characters 

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages
#Need to make an upload folder that stores the item pictures uploaded by users

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

#create item listing function need to create a database to store the item name, description, and picture
def create_item (item_name, item_description, item_picture, user_id):
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        #item_id is assigned based on the users name in the user database
        c.execute("INSERT INTO items (item_name, item_description, item_picture, user_id) VALUES (?, ?, ?, ?)", (item_name, item_description, item_picture, user_id))
        conn.commit()
    except sqlite3.IntegrityError:
        return "Item name already exists for this user"
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
            flash("Login successful", "success")
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

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        item_name = request.form['item_name']
        item_description = request.form['item_description']
        file = request.files['item_picture']
        #check for username in session
        if 'username' in session:
            user_id = session['username']
            #check if file is uploaded
            if file:
                filename = secure_filename(file.filename) #secure the filename so no errors
                #NEED TO ADD FILE VALIDATION ONCE FILE LOCATION IS DEFINED
            else:
                flash("No file uploaded")
        else:
            flash("user not logged in")
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
