from flask import Flask, request, render_template, redirect, url_for, flash, session
import sqlite3
import os #for uploading files
from werkzeug.utils import secure_filename #for securing the files making sure theres no dangerous characters 
from user_profile import ProfileDB  # Import ProfileDB for functionality

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages
UPLOAD_FOLDER = 'uploads' #Path to folder where uploaded files are stored
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} #files user can upload
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #set path to the folder

#File validation function to check if the file is an allowed image
def allowed_file(filename):
    #checks if the file has a '.' in the filename
    #checks if the name after '.' is in ALLOWED_EXTENSIONS uses lower() function to comapare to the names in ALLOWED_EXTENSIONS 
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#User class to create a user and check a user
class User:
    #User constructor intitializes username, email, and password
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    #static method to check if a user exists in the database
    @staticmethod
    def check_user(email, password):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()
        return user

    #static method to create a user in the database
    @staticmethod
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
class Item:
    #Item constructor to intitialize item_name, item_description, item_picture, and user_id
    def __init__(self, item_name, item_description, item_picture, user_id):
        self.item_name = item_name
        self.item_description = item_description
        self.item_picture = item_picture
        self.user_id = user_id
#static method tocreate item listing function need to create a database to store the item name, description, and picture
    @staticmethod
    def create_item (item_name, item_description, item_picture, user_id):
        try:
            conn = sqlite3.connect('items.db')
            c = conn.cursor()
            #item_id is assigned based on the users name in the user database
            c.execute("INSERT INTO items (item_name, item_description, item_picture, user_id) VALUES (?, ?, ?, ?)", (item_name, item_description, item_picture, user_id))
            conn.commit()
            return "Item created successfully"
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
        user = User.check_user(email, password)
        if user:
            #set the session for the user_id and username
            session['userID'] = user[0] #need to make sure this is the right collumn in the database
            session['username'] = user[1] #need to make sure thsi is the right collumn in the database
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
        message = User.create_user(username, email, password)
        if message == "User created successfully":
            flash(message, "info")
            return redirect(url_for('mainMenu'))
        else:
            flash(message, "danger")
            return redirect(url_for('register'))
    return render_template('createUser.html')

@app.route('/mainMenu')
def mainMenu():
    if 'username' in session:
        username = session['username']
        return render_template('mainMenu.html', username=username)
    else:
        return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        item_name = request.form['item_name']
        item_description = request.form['item_description']
        file = request.files['item_picture']
        #check for username in session
        if 'username' in session:
            user_id = session['username']
            #file validation and upload to uploads folder
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                Item.create_item(item_name, item_description, file_path, user_id)
                #Let user know item was added successfully
                flash("Item successfully added", "success") 
            else:
                #Let user know they uploaded an invalid file and to use these file types
                flash("Invalid file type. Please upload a PNG, JPG, or JPEG image.", "danger")
        else:
            flash("user not logged in")
        return render_template('add.html')
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

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'userID' in session:
        user_id = session['userID']
        if request.method == 'POST':
            bio = request.form['bio']
            profile = ProfileDB.get_profile(user_id)
            if profile:
                ProfileDB.update_profile(user_id, bio, None)
            else:
                ProfileDB.create_profile(user_id, bio, None)
            flash('Profile updated successfully!', 'success')
        
        profile = ProfileDB.get_profile(user_id)
        if profile:
            return render_template('userProfile.html', username=session['username'], bio=profile[2])
        else:
            return render_template('userProfile.html', username=session['username'], bio='')
    else:
        flash('You need to login first.', 'danger')
        return redirect(url_for('login'))


@app.route('/signout')
def signout():
    session.pop('userID', None)
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)