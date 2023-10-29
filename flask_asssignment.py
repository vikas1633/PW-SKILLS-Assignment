########### Basics of Flask: #####################

# 1. Create a Flask app that displays "Hello, World!" on the homepage.
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()


#######################################
2. Build a Flask app with static HTML pages and navigate between them.

pip install Flask
Organiging project directory as follows:

project_folder/
    - app.py
    - templates/
        - home.html
        - about.html

########### home.html:

html
Copy code
<!DOCTYPE html>
<html>
<head>
    <title>Home Page</title>
</head>
<body>
    <h1>Welcome to the Home Page</h1>
    <p><a href="/about">Visit the About Page</a></p>
</body>
</html>


############ about.html:


<!DOCTYPE html>
<html>
<head>
    <title>About Page</title>
</head>
<body>
    <h1>About Us</h1>
    <p>This is the About Page.</p>
    <p><a href="/">Back to Home</a></p>
</body>
</html>

########## Creating Flask app in the app.py script:

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

##################################
3. Develop a Flask app that uses URL parameters to display dynamic content.

Creating a new directory 


project_folder/
    - app.py
    - templates/
        - dynamic_content.html

################# Creating a Flask app in the app.py script:

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Home Page"

@app.route('/greet/<name>')
def greet(name):
    return f"Hello, {name}!"

if __name__ == '__main__':
    app.run(debug=True)

########## Creating a template for the dynamic content (dynamic_content.html):

<!DOCTYPE html>
<html>
<head>
    <title>Greet User</title>
</head>
<body>
    <h1>Greeting Page</h1>
    <p>Hello, {{ name }}!</p>
</body>
</html>

########### Modifing the greet route in app.py to render the dynamic_content.html template with dynamic data:

@app.route('/greet/<name>')
def greet(name):
    return render_template('dynamic_content.html', name=name)



Run your Flask app using : python app.py

########################
4. Create a Flask app with a form that accepts user input and displays it.

Creating a new directory  and organize it as follows:

project_folder/
    - app.py
    - templates/
        - form.html

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        user_input = request.form['user_input']
        return render_template('form.html', user_input=user_input)
    return render_template('form.html', user_input='')

if __name__ == '__main__':
    app.run(debug=True)
In this code:


############# Create a template for the form (form.html):

<!DOCTYPE html>
<html>
<head>
    <title>Form Input</title>
</head>
<body>
    <h1>Form Input</h1>
    <form method="post">
        <label for="user_input">Enter something:</label>
        <input type="text" id="user_input" name="user_input" value="{{ user_input }}">
        <input type="submit" value="Submit">
    </form>
    {% if user_input %}
    <p>You entered: {{ user_input }}</p>
    {% endif %}
</body>
</html>


Running your Flask app: python app.py

####################################################
5. Implement user sessions in a Flask app to store and display user-specific data.

Install the required libraries:

pip install Flask Flask-Session
##########3 Creating a Flask app with session management:

from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session

app = Flask(__name__)

# Configure the session type to use in-memory storage
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Set a secret key for session management (replace 'your_secret_key' with a random, secure key)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        session['user_input'] = user_input
        return redirect(url_for('index'))
    user_input = session.get('user_input', '')
    return render_template('session.html', user_input=user_input)

if __name__ == '__main__':
    app.run(debug=True)


## Creating an HTML template (session.html) to display the user input:

<!DOCTYPE html>
<html>
<head>
    <title>Session Example</title>
</head>
<body>
    <h1>Session Example</h1>
    <form method="post">
        <label for="user_input">Enter something:</label>
        <input type="text" id="user_input" name="user_input" value="{{ user_input }}">
        <input type="submit" value="Submit">
    </form>
    {% if user_input %}
    <p>You entered: {{ user_input }}</p>
    {% endif %}
</body>
</html>
Run Flask app: python app.py

##############  Intermediate Flask Topics: ################
6. Build a Flask app that allows users to upload files and display them on the website.

Create a Flask app:

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

# Configure the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Helper function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file', filename=filename))

    return 'Invalid file type'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

########## Create an HTML template (index.html) for the homepage:
html
Copy code
<!DOCTYPE html>
<html>
<head>
    <title>File Upload Example</title>
</head>
<body>
    <h1>Upload a File</h1>
    <form method="post" action="/upload" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
</body>
</html>
Run your Flask app: python app.py

#######################################################################
7. Integrate a SQLite database with Flask to perform CRUD operations on a list of items.


########### Install Flask-SQLAlchemy, a Flask extension for working with SQLAlchemy:

pip install Flask-SQLAlchemy

#Create a Flask app that uses SQLite as the database:


from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'  # SQLite database file name
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    name = request.form.get('name')
    if name:
        item = Item(name=name)
        db.session.add(item)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_item(id):
    item = Item.query.get(id)
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)


## Create an HTML template (index.html) to display the list of items and allow users to add and delete items:


<!DOCTYPE html>
<html>
<head>
    <title>Item List</title>
</head>
<body>
    <h1>Item List</h1>
    <form method="POST" action="/add">
        <input type="text" name="name" placeholder="Add an item" required>
        <input type="submit" value="Add">
    </form>
    <ul>
        {% for item in items %}
            <li>
                {{ item.name }}
                <a href="/delete/{{ item.id }}">Delete</a>
            </li>
        {% endfor %}
    </ul>
</body>
</html>
Run the Flask app: python app.py

###################################################################
8. Implement user authentication and registration in a Flask app using Flask-Login.

## Install Flask-Login:


pip install Flask-Login
Set Up the Flask App:

###### Starting by creating a basic Flask app with the necessary configurations. 


from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database for users
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Add the User model here (next step).

@app.route('/')
def home():
    return 'Home Page'

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
Define the User Model:

###### Creating a User model to represent users in your application. This model should inherit from UserMixin provided by Flask-Login.


from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
User Registration and Login:

## Create routes and views for user registration and login. Users should be able to create an account and log in.


from flask import request, redirect, url_for
from flask_login import login_user

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Hash the password and create a new User object
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # Log in the user after registration
        login_user(user)
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html')
User Sessions and Login Manager:

### Configuring Flask-Login to manage user sessions. Creating user_loader and request_loader functions to load users based on their ID and request.


from flask_login import login_user, UserMixin, login_required

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)
User Authentication:

Use @login_required to protect routes that require authentication. Users who aren't logged in will be redirected to the login page.


@app.route('/protected')
@login_required
def protected():
    return 'Protected Page'
##Create Templates and Forms:

## Create HTML templates for the registration and login forms, as well as a home page and protected page.
## Registration Form Template (register.html):

<!DOCTYPE html>
<html>
<head>
    <title>Registration</title>
</head>
<body>
    <h1>Registration</h1>
    <form method="POST" action="/register">
        <label for="username">Username:</label>
        <input type="text" name="username" id="username" required><br>
        <label for="password">Password:</label>
        <input type="password" name="password" id="password" required><br>
        <input type="submit" value="Register">
    </form>
</body>
</html>
Login Form Template (login.html):
html
Copy code
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h1>Login</h1>
    <form method="POST" action="/login">
        <label for="username">Username:</label>
        <input type="text" name="username" id="username" required><br>
        <label for="password">Password:</label>
        <input type="password" name="password" id="password" required><br>
        <input type="submit" value="Login">
    </form>
</body>
</html>

## Home Page Template (home.html):

<!DOCTYPE html>
<html>
<head>
    <title>Home</title>
</head>
<body>
    <h1>Welcome to the Home Page</h1>
    <p>Hello, {{ current_user.username }}!</p>
    <a href="/protected">Visit Protected Page</a>
</body>
</html>
Protected Page Template (protected.html):
html
Copy code
<!DOCTYPE html>
<html>
<head>
    <title>Protected Page</title>
</head>
<body>
    <h1>Protected Page</h1>
    <p>This page is protected. Only authenticated users can access it.</p>
</body>
</html>

Run the Flask App: python app.py

########################################################################################################
9. Create a RESTful API using Flask to perform CRUD operations on resources like books or movies.

## Creating a  Flask application and setting up a virtual environment  by running:


mkdir flask_api
cd flask_api
python -m venv venv
source venv/bin/activate  
pip install Flask
## Creating your Flask app. 


from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data (in-memory storage)
books = [
    {"id": 1, "title": "Book 1", "author": "Author 1"},
    {"id": 2, "title": "Book 2", "author": "Author 2"},
]

@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books)

@app.route("/books/<int:id>", methods=["GET"])
def get_book(id):
    book = next((book for book in books if book["id"] == id), None)
    if book:
        return jsonify(book)
    return ("", 404)

@app.route("/books", methods=["POST"])
def create_book():
    data = request.get_json()
    new_book = {
        "id": len(books) + 1,
        "title": data["title"],
        "author": data["author"],
    }
    books.append(new_book)
    return jsonify(new_book), 201

@app.route("/books/<int:id>", methods=["PUT"])
def update_book(id):
    data = request.get_json()
    book = next((book for book in books if book["id"] == id), None)
    if book:
        book.update(data)
        return jsonify(book)
    return ("", 404)

@app.route("/books/<int:id>", methods=["DELETE"])
def delete_book(id):
    global books
    books = [book for book in books if book["id"] != id]
    return ("", 204)

if __name__ == "__main__":
    app.run(debug=True)
#######################################
10. Design a Flask app with proper error handling for 404 and 500 errors.

To design a Flask app with proper error handling for 404 (Not Found) and 500 (Internal Server Error) errors, we can use Flask's error handling features.


from flask import Flask, render_template

app = Flask(__name)

# Custom 404 error handler
@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404

# Custom 500 error handler
@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500

# Your routes and application logic
@app.route("/")
def index():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)


Creating the HTML templates for these error pages in the templates directory of your Flask project.


<!DOCTYPE html>
<html>
<head>
    <title>404 Not Found</title>
</head>
<body>
    <h1>404 - Not Found</h1>
    <p>The page you are looking for does not exist.</p>
</body>
</html>
And here's a simple 500.html page:


<!DOCTYPE html>
<html>
<head>
    <title>500 Internal Server Error</title>
</head>
<body>
    <h1>500 - Internal Server Error</h1>
    <p>Something went wrong on our end. Please try again later.</p>
</body>
</html>


######################################### Real-time Development: ########################################

Install the necessary libraries:

pip install flask flask-socketio

Create the Flask application:


from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# List to store messages
messages = []

# Route to the chat page
@app.route('/')
def chat():
    return render_template('chat.html', messages=messages)

# Socket.io event for new messages
@socketio.on('message')
def handle_message(data):
    messages.append(data)
    socketio.emit('message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
## Create the HTML template for the chat page (chat.html):


<!DOCTYPE html>
<html>
<head>
    <title>Chat</title>
</head>
<body>
    <ul id="message-list">
        {% for message in messages %}
            <li>{{ message }}</li>
        {% endfor %}
    </ul>
    <input id="message-input" autocomplete="off" />
    <button id="send-button">Send</button>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script>
        var socket = io.connect('http://' + document.domain + ':' + location.port);
        socket.on('message', function(data) {
            var messageList = document.getElementById('message-list');
            var messageItem = document.createElement('li');
            messageItem.textContent = data;
            messageList.appendChild(messageItem);
        });
        document.getElementById('send-button').onclick = function() {
            var messageInput = document.getElementById('message-input');
            var message = messageInput.value;
            if (message) {
                socket.emit('message', message);
                messageInput.value = '';
            }
        };
    </script>
</body>
</html>

################################################################
12. Build a Flask app that updates data in real-time using WebSocket connections.

Install the necessary libraries:

pip install flask flask-socketio eventlet
Create the Flask application:


from flask import Flask, render_template
from flask_socketio import SocketIO
import eventlet

eventlet.monkey_patch()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Counter variable
counter = 0

# Route to the real-time update page
@app.route('/')
def index():
    return render_template('realtime.html', counter=counter)

# Socket.io event for updating the counter
@socketio.on('update_counter')
def update_counter(data):
    global counter
    counter += 1
    socketio.emit('counter_updated', {'count': counter}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
## Create the HTML template for the real-time update page (realtime.html):


<!DOCTYPE html>
<html>
<head>
    <title>Real-Time Counter</title>
</head>
<body>
    <h1>Real-Time Counter</h1>
    <p id="counter">{{ counter }}</p>
    <button id="update-button">Update Counter</button>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script>
        var socket = io.connect('http://' + document.domain + ':' + location.port);
        socket.on('counter_updated', function(data) {
            document.getElementById('counter').textContent = data.count;
        });
        document.getElementById('update-button').onclick = function() {
            socket.emit('update_counter', {});
        };
    </script>
</body>
</html>
##################################################################################

13. Implement notifications in a Flask app using websockets to notify users of updates.

## Install the required libraries:

pip install flask flask-socketio eventlet
## Create the Flask application:


from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import eventlet

eventlet.monkey_patch()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Store notifications in a list
notifications = []

# Route for the chat page
@app.route('/')
def chat():
    return render_template('chat.html', notifications=notifications)

# Socket.io event for new messages
@socketio.on('new_notification')
def handle_notification(data):
    notification = data['message']
    notifications.append(notification)
    emit('new_notification', notification, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)

## Create the HTML template for the chat page (chat.html):


<!DOCTYPE html>
<html>
<head>
    <title>Notification System</title>
</head>
<body>
    <h1>Notification System</h1>
    
    <ul id="notification-list">
        {% for notification in notifications %}
        <li>{{ notification }}</li>
        {% endfor %}
    </ul>
    
    <input id="notification-input" type="text" placeholder="Enter a notification">
    <button id="send-notification">Send</button>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script>
        var socket = io.connect('http://' + document.domain + ':' + location.port);
        
        // Receive and display new notifications
        socket.on('new_notification', function(notification) {
            var notificationList = document.getElementById('notification-list');
            var listItem = document.createElement('li');
            listItem.textContent = notification;
            notificationList.appendChild(listItem);
        });

        // Send new notifications
        document.getElementById('send-notification').onclick = function() {
            var notificationInput = document.getElementById('notification-input');
            var notification = notificationInput.value;
            notificationInput.value = '';
            socket.emit('new_notification', { message: notification });
        };
    </script>
</body>
</html>










