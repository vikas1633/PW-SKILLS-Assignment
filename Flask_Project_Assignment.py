1. Build a Flask app that scrapes data from multiple websites and displays it on your site.
You can try to scrap websites like youtube , amazon and show data on output pages and deploy it on cloud
platform .

###################################################
Installing  necessary libraries:

pip install Flask beautifulsoup4 requests
Create a Flask app:

################### app.py
from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    # Scraping YouTube videos' titles
    youtube_url = 'https://www.youtube.com/feed/trending'
    response = requests.get(youtube_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extracting video titles
    video_titles = [title.text for title in soup.select('h3')]
    
    return render_template('index.html', video_titles=video_titles)

if __name__ == '__main__':
    app.run(debug=True)


############## Creating a template:

html
<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Scraping App</title>
</head>
<body>
    <h1>YouTube Trending Videos</h1>
    <ul>
        {% for title in video_titles %}
            <li>{{ title }}</li>
        {% endfor %}
    </ul>
</body>
</html>
Running Flask app:

###################################
python app.py
using  http://127.0.0.1:5000/ in  web browser to see the scraped YouTube video titles.

############### Deploying on a cloud platform :

Create a requirements.txt file containing the required libraries:

Flask==2.1.0
beautifulsoup4==4.10.0
requests==2.26.0
gunicorn==20.1.0
Creating a Procfile to tell Heroku how to run your app:

web: gunicorn app:app
Commit your changes to a version control system (e.g., Git).


####################################
2. Create a Flask app that consumes data from external APIs and displays it to users.
Try to find an public API which will give you a data and based on that call it and deploy it on cloud platform


Installing necessary libraries:

pip install Flask requests
########## Creating a Flask app:

# app.py
from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # Consume data from JSONPlaceholder API
    api_url = 'https://jsonplaceholder.typicode.com/posts'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        posts = response.json()
    else:
        posts = []
    
    return render_template('index_api.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)
############ Creating a template:
html

<!-- templates/index_api.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Data App</title>
</head>
<body>
    <h1>Posts from JSONPlaceholder API</h1>
    <ul>
        {% for post in posts %}
            <li>{{ post.title }}</li>
        {% endfor %}
    </ul>
</body>
</html>
########## Running your Flask app:

python app.py
using  http://127.0.0.1:5000/ in  web browser to see the data fetched from the JSONPlaceholder API.

############### Deploying on a cloud platform :
Creating a requirements.txt file containing the required libraries:
plaintext

Flask==2.1.0
requests==2.26.0
gunicorn==20.1.0
Creating a Procfile  how to run  app:
plaintext


web: gunicorn app:app

######################################################
3. Implement OAuth2 authentication to allow users to log in using their Google or Facebook accounts.


############ Installing necessary libraries:

pip install Flask Flask-OAuthlib
############ Creating a Flask app:

# app.py
from flask import Flask, redirect, url_for, session
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# OAuth configuration for Google
oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key='your_google_client_id',
    consumer_secret='your_google_client_secret',
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

# OAuth configuration for Facebook
facebook = oauth.remote_app(
    'facebook',
    consumer_key='your_facebook_app_id',
    consumer_secret='your_facebook_app_secret',
    request_token_params={'scope': 'email'},
    base_url='https://graph.facebook.com/v12.0/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
)

@app.route('/')
def index():
    return 'Welcome to OAuth2 Authentication Example!'

@app.route('/login')
def login():
    return redirect(url_for('google_login'))

@app.route('/google_login')
def google_login():
    return google.authorize(callback=url_for('google_authorized', _external=True))

@app.route('/google_authorized')
def google_authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')
    return 'Logged in as: ' + user_info.data['email']

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

if __name__ == '__main__':
    app.run(debug=True)


############################  Running Flask app:
python app.py
using http://127.0.0.1:5000/login in  web browser to initiate the OAuth2 authentication with Google.



##############################################################
4. Develop a recommendation system using Flask that suggests content to users based on their preferences.


######## Installing necessary libraries:

pip install Flask pandas scikit-learn
#############  Creating a Flask app:

# app.py
from flask import Flask, render_template, request

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Sample data (user-item interactions)
data = {
    'user_id': ['User1', 'User1', 'User2', 'User2', 'User3'],
    'item_id': ['Movie1', 'Movie2', 'Movie2', 'Movie3', 'Movie1'],
    'rating': [5, 4, 3, 2, 1]
}

df = pd.DataFrame(data)

# Pivot the data to create a user-item matrix
user_item_matrix = df.pivot(index='user_id', columns='item_id', values='rating').fillna(0)

# Calculate cosine similarity between users
user_similarity = cosine_similarity(user_item_matrix)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_id = request.form['user_id']
    
    if user_id not in user_item_matrix.index:
        return render_template('index.html', error='User not found.')

    # Get user ratings
    user_ratings = user_item_matrix.loc[user_id].values.reshape(1, -1)

    # Calculate cosine similarity between the user and other users
    similarities = cosine_similarity(user_item_matrix, user_ratings)

    # Get the indices of users sorted by similarity
    similar_users = similarities.argsort(axis=0)[:-2:-1].flatten()

    # Get items that the user has not rated
    unrated_items = user_item_matrix.columns[user_item_matrix.loc[user_id] == 0].tolist()

    # Calculate the predicted ratings for unrated items
    predicted_ratings = user_item_matrix.iloc[similar_users].mean().loc[unrated_items].sort_values(ascending=False)

    recommendations = predicted_ratings.index.tolist()

    return render_template('index.html', user_id=user_id, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
############ Creating HTML templates:

html

<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recommendation System</title>
</head>
<body>
    <h1>Recommendation System</h1>
    <form method="post" action="/recommend">
        <label for="user_id">Enter User ID:</label>
        <input type="text" id="user_id" name="user_id" required>
        <button type="submit">Get Recommendations</button>
    </form>
    {% if error %}
        <p>{{ error }}</p>
    {% endif %}
    {% if recommendations %}
        <h2>Recommended Items:</h2>
        <ul>
            {% for item in recommendations %}
                <li>{{ item }}</li>
            {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
####### Running your Flask app:

python app.py
Using http://127.0.0.1:5000/ in  web browser to use the recommendation system. 










