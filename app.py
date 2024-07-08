from flask import Flask, request, render_template, redirect, url_for, flash, session
import sqlite3
import os #for uploading files
from werkzeug.utils import secure_filename #for securing the files making sure theres no dangerous characters 
from user_profile import ProfileDB  # Import ProfileDB for functionality
from follow_db import FollowDB #for the followers and following database 

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
    return render_template('show_Collectable.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

class ProfileDB:
    @staticmethod
    def get_profile(username):
        conn = sqlite3.connect('profiles.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, bio FROM profiles WHERE username=?", (username,))
        profile = cursor.fetchone()
        conn.close()
        return profile

    @staticmethod
    def update_profile(username, bio, profile_pic):
        conn = sqlite3.connect('profiles.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE profiles SET bio=?, profile_pic=? WHERE username=?", (bio, profile_pic, username))
        conn.commit()
        conn.close()

    @staticmethod
    def create_profile(username, bio, profile_pic):
        conn = sqlite3.connect('profiles.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO profiles (username, bio, profile_pic) VALUES (?, ?, ?)", (username, bio, profile_pic))
        conn.commit()
        conn.close()

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' in session:
        username = session['username']
        if request.method == 'POST':
            bio = request.form['bio']
            profile = ProfileDB.get_profile(username)
            if profile:
                ProfileDB.update_profile(username, bio, None)
            else:
                ProfileDB.create_profile(username, bio, None)
            flash('Profile updated successfully!', 'success')
        
        profile = ProfileDB.get_profile(username)
        followers = FollowDB.get_followers(username)
        following = FollowDB.get_following(username)
        followers_count = len(followers)
        following_count = len(following)
        if profile:
            return render_template('userProfile.html', username=username, bio=profile[2], followers=followers, following=following, followers_count=followers_count, following_count=following_count)
        else:
            return render_template('userProfile.html', username=username, bio='', followers=followers, following=following, followers_count=followers_count, following_count=following_count)
    else:
        flash('You need to login first.', 'danger')
        return redirect(url_for('login'))

@app.route('/search_user', methods=['POST'])
def search_user():
    search_query = request.form['search_query']
    user_profile = ProfileDB.get_profile(search_query)
    if user_profile:
        return redirect(url_for('visit_user_profile', username=search_query))
    else:
        return "User not found", 404

@app.route('/visitUserProfile/<username>')
def visit_user_profile(username):
    user_profile = ProfileDB.get_profile(username)
    if user_profile:
        is_following = False
        if 'username' in session:
            current_username = session['username']
            following = FollowDB.get_following(current_username)
            if username in [user[0] for user in following]:
                is_following = True

        # Fetch the counts using the new functions
        following_count = FollowDB.get_other_user_following(username)
        followers_count = FollowDB.get_other_user_followers(username)

        return render_template('visitUserProfile.html', 
                               username=user_profile[1], 
                               bio=user_profile[2], 
                               is_following=is_following, 
                               following_count=following_count, 
                               followers_count=followers_count)
    else:
        return "User not found", 404
    
@app.route('/follow/<username>', methods=['POST'])
def follow(username):
    if 'username' in session:
        current_username = session['username']
        FollowDB.follow_user(current_username, username)
        flash(f'You are now following {username}!', 'success')
    else:
        flash('You need to login first.', 'danger')
    return redirect(url_for('visit_user_profile', username=username))

@app.route('/unfollow/<username>', methods=['POST'])
def unfollow(username):
    if 'username' in session:
        current_username = session['username']
        FollowDB.unfollow_user(current_username, username)
        flash(f'You have unfollowed {username}.', 'success')
    else:
        flash('You need to login first.', 'danger')
    return redirect(url_for('visit_user_profile', username=username))

@app.route('/following/<username>')
def following(username):
    following_list = FollowDB.get_following(username)
    return render_template('following.html', username=username, following=following_list)

@app.route('/followers/<username>')
def followers(username):
    followers_list = FollowDB.get_followers(username)
    return render_template('followers.html', username=username, followers=followers_list)


@app.route('/signout')
def signout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)