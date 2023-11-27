from flask import *
from flask_wtf import *
import pathlib
from app.models.signin import UserManager
from flask_dance.contrib.google import make_google_blueprint, google
import requests
from flask import Blueprint, render_template, request, session, abort, redirect, jsonify
from flask_mysql_connector import MySQL
import os
import google_auth_oauthlib.flow
import google.auth.transport.requests

mysql = MySQL()
user_bp = Blueprint('user', __name__)
UserManager.init_db(mysql)



signin_bp = Blueprint('signin', __name__)



# Set environment variable for insecure transport (for development only)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Getting client id from .env and load it on backend
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRETS_FILE = os.path.join(
    pathlib.Path(__file__).parent.parent.parent, "client_secret.json")


# Define Google OAuth flow with required scopes and redirect URI for authorization
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email", "openid"])
flow.redirect_uri = 'http://localhost:5000/callback'

@signin_bp.route('/get_client_key')
def get_client_key():
    return jsonify({'google_client_id': GOOGLE_CLIENT_ID})

# Define Google OAuth flow with required scopes and redirect URI for authorization
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email", "openid"])
flow.redirect_uri = 'http://localhost:5000/callback'


@signin_bp.route('/')  # Starting page
def index():
    # Check if the user is authenticated
    is_authenticated = 'user_details' in session
    if is_authenticated:
        # Render the template with user details
        return redirect('/home_authenticated')
    else:
        # Render a general version of the page and prompt the user to sign in
        return render_template('base.html', user={'is_authenticated': False})

@signin_bp.route('/user_auth_status')
def get_user_auth_status():
    # Check if the user is authenticated
    is_authenticated = 'credentials' in session
    return jsonify({'authenticated': is_authenticated})  


# Initiates the OAuth2 flow for the user to sign in with Google.
@signin_bp.route('/signin')
def authorize():
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    print('User signed in successfully.')
    return redirect(authorization_url)


# Route handling the callback after successful authentication
@signin_bp.route('/callback')
def callback():
    state = session.pop('state', None)
    if state is None or state != request.args.get('state'):
        return 'Invalid state parameter', 401

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store the credentials securely in the session
    credentials = flow.credentials
    session.permanent = True

    # Store credentials in the Flask session
    session['credentials'] = credentials_to_dict(credentials)
    print("credentials:", session['credentials'])

    # Call Google API to get user profile information
    user_info_endpoint = 'https://www.googleapis.com/oauth2/v3/userinfo'
    access_token = credentials.token

    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(user_info_endpoint, headers=headers)

    if response.status_code == 200:
        user_info = response.json()
        # Extract and store user details in the session
        userid = user_info['sub']  # USE USER ID AS AN IDENTIFIER IN DATABASE
        email = user_info['email']
        name = user_info['name']
        given_name = user_info['given_name']
        picture = user_info['picture']
        # Store user details in the session or perform other operations
        session['user_details'] = {
            'userid': userid,
            'email': email,
            'name': name,
            'given_name': given_name,
            'picture': picture
        }
        # print(session['user_details'])

        # Check if the user exists in the database
        user = UserManager.get_user_by_id(userid)

        if not user:
            # If the user does not exist, add them to the database
            UserManager.add_user(userid, email)
            print(f"User {userid} added to the database.")
        else:
            print(f"User {userid} already exists in the database.")

        return redirect('/home_authenticated')
    else:
        return 'Failed to fetch user info', 500


@signin_bp.route('/home_authenticated')
def home_authenticated():
    # Check if the user's details exist in the session
    if 'user_details' not in session:
        return 'Unauthorized', 401

    # Access the user's details from the session
    stored_user_details = session['user_details']
    print("HA Stored User details: ", stored_user_details)

    # Access stored saved routes here from database
    # Perform code operations here like saving routes, fetching user-saved routes from database

    # This route will be accessible when the user reloads the page or revisits the site
    return render_template('base.html', user={'is_authenticated': True, 'details': stored_user_details})

# Function to convert credentials to dictionary
def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}



@signin_bp.route('/signout')  # Signout route to clear the session data
def signout():
    session.clear()
    return redirect("/")


@signin_bp.route('/')
def home():
    return render_template('signin.html')

