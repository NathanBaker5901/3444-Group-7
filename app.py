from flask import Flask, request, render_template, redirect, url_for, flash, session
import sqlite3
import os #for uploading files
from werkzeug.utils import secure_filename #for securing the files making sure theres no dangerous characters 
from user_profile import ProfileDB  # Import ProfileDB for functionality
from follow_db import FollowDB #for the followers and following database 
import re #regular expressions for python
from itsdangerous import URLSafeTimedSerializer #Used to make a reset token to reset password
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages
UPLOAD_FOLDER = os.path.join('static', 'uploads') #Path to folder where uploaded files are stored
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} #files user can upload
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #set path to the folder

#File validation function to check if the file is an allowed image
def allowed_file(filename):
    #checks if the file has a '.' in the filename
    #checks if the name after '.' is in ALLOWED_EXTENSIONS uses lower() function to comapare to the names in ALLOWED_EXTENSIONS 
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to check login credentials for email or username
def check_login(identifier, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Check if the identifier is an email or username
    cursor.execute("SELECT * FROM users WHERE email=? OR username=?", (identifier, identifier))
    user = cursor.fetchone()

    print(f"Debug: Retrieved user: {user}")  # Debug output
    
    if user and user[3] == password: 
        return user
    return None

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
    # Part of the forget password, gets the email first
    @staticmethod
    def get_user_by_email(email):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=?", (email,))
        user = c.fetchone()
        conn.close()
        return user
    # Made a new password into the users.db
    @staticmethod
    def update_password(email, new_password):
        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("UPDATE users SET password=? WHERE email=?", (new_password, email))
            conn.commit()
            
            return "Password changed successfully"
        except sqlite3.IntegrityError:
            return "Password changed failed"
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

    #static method to get each item from a user in order to correctly display the items
    @staticmethod
    def get_user_items(user_id):
        conn = sqlite3.connect('items.db')
        c = conn.cursor()
        c.execute("SELECT * FROM items WHERE user_id=?", (user_id,))
        items = c.fetchall()
        conn.close()
        return items
    
    @staticmethod
    def update_item(item_id, new_name, new_description):
        conn = None
        try:
            conn = conn = sqlite3.connect('items.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('UPDATE items SET item_name = ?, item_description = ? WHERE item_id = ?', (new_name, new_description, item_id))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

    @staticmethod
    def delete_item(item_id):
        conn = None
        try:
            conn = conn = sqlite3.connect('items.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('DELETE FROM items WHERE id = ?', (item_id))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()





@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']
        
        user = check_login(identifier, password)
        print(f"Debug: User after check_login: {user}")  # Debug output

        if user:
            # Perform login actions 
            session['userID'] = user[0]  
            session['username'] = user[1]  

            return redirect(url_for('mainMenu'))
        else:
            flash('Login failed. Please check your identifier and password.', 'danger')
    
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
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')
                file.save(file_path)
                #set the relative path for the image to be added
                relative_path = os.path.join('uploads', filename).replace('\\', '/')
                #call the create item function from the item class 
                Item.create_item(item_name, item_description, relative_path, user_id)
                #Let user know item was added successfully
                flash("Item successfully added", "success") 
            else:
                #Let user know they uploaded an invalid file and to use these file types
                flash("Invalid file type. Please upload a PNG, JPG, or JPEG image.", "danger")
        else:
            flash("user not logged in")
        return render_template('add.html')
    return render_template('add.html')


@app.route('/update_delete', methods=['GET', 'POST'])
def update_delete():
    if request.method == 'POST':
        item_id = request.form['item_id']
        Item.delete_item(item_id)

        return redirect(url_for('update_delete'))
    if 'username' in session:
        username = session['username']
        items = Item.get_user_items(username)
        processed_items = []
        for item in items:
            processed_items.append({
                'item_id': item[0],
                'item_name': item[1],
                'item_description': item[2],
                'item_picture': item[3].replace('\\', '/'),  # Normalize path separators
            })
        return render_template('update_delete.html', items=processed_items, username=username)
    return render_template('update_delete.html', items=items)




#Makes a forgot_password in the html
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        message = User.update_password(email, password)
        if message == "Password changed successfully":
            flash(message, "info")
            return redirect(url_for('login'))
        else:
            flash(message, "danger")
            return redirect(url_for('login'))
    return render_template('forgot_password.html')

@app.route('/show_collectable')
def show_collectable():
    if 'username' in session:
        username = session['username']
        items = Item.get_user_items(username)
        processed_items = []
        for item in items:
            processed_items.append({
                'item_name': item[1],
                'item_description': item[2],
                'item_picture': item[3].replace('\\', '/'),  # Normalize path separators
            })
        return render_template('show_Collectable.html', items=processed_items, username=username)
    else:
        flash("User not logged in")
        return redirect(url_for('login'))
    
@app.route('/single_Collectable/<item_name>')
def single_Collectable(item_name):
    if 'username' in session:
        username = session['username']
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute("SELECT * FROM items WHERE item_name=?", (item_name,))
    item = c.fetchone()
    conn.close()
    if item:
        item_dict = {
            'id': item[0],
            'item_name': item[1],
            'item_description': item[2],
            'item_picture': item[3].replace('\\', '/'),
            'user_id': item[4]
        }
        return render_template('single_Collectable.html', item=item_dict, username=username)
    else:
        flash('Item not found', 'danger')
        return redirect(url_for('show_collectable'))  

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