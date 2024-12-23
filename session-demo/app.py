from flask import Flask, request, redirect, url_for, session, render_template
import os
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Directory to store user credentials
USER_DATA_DIR = './user_data'
if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)

# Helper function to hash passwords for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Helper function to store user credentials
def store_user(username, password):
    file_path = os.path.join(USER_DATA_DIR, f"{username}.txt")
    with open(file_path, 'w') as file:
        file.write(hash_password(password))

# Helper function to verify user credentials
def verify_user(username, password):
    file_path = os.path.join(USER_DATA_DIR, f"{username}.txt")
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            stored_password = file.read()
        return stored_password == hash_password(password)
    return False

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if user already exists
        if os.path.exists(os.path.join(USER_DATA_DIR, f"{username}.txt")):
            return "User already exists!"
        # Store user credentials
        store_user(username, password)
        return redirect(url_for('login'))
    return '''
        <form method="post">
            Username: <input type="text" name="username" required><br>
            Password: <input type="password" name="password" required><br>
            <button type="submit">Sign Up</button>
        </form>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Verify credentials
        if verify_user(username, password):
            session['user'] = username
            return redirect(url_for('dashboard'))
        return "Invalid credentials!"
    return '''
        <form method="post">
            Username: <input type="text" name="username" required><br>
            Password: <input type="password" name="password" required><br>
            <button type="submit">Login</button>
        </form>
    '''

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return f"Welcome, {session['user']}! <a href='/logout'>Logout</a>"
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
