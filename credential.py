#---------Authenticating the Spotify and Storing Credentials in a Text File--------------
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Function to get Spotify credentials from the user and save them in a text file
def get_spotify_credentials():
    credentials_file = 'spotify_credentials.txt'
    print("Checking if credentials file exists...")

    # Check if the credentials file already exists
    if not os.path.exists(credentials_file):
        print("Spotify credentials file not found. Please provide your credentials.")
        CLIENT_ID = input("Enter your Spotify Client ID: ").strip()
        CLIENT_SECRET = input("Enter your Spotify Client Secret: ").strip()

        # Save the credentials in a text file
        print("Saving credentials to file...")
        with open(credentials_file, 'w') as file:
            file.write(f"{CLIENT_ID}\n{CLIENT_SECRET}\n")
        print(f"Credentials saved to {credentials_file}")
    else:
        print(f"Found existing credentials in {credentials_file}")
        with open(credentials_file, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 2:
                CLIENT_ID = lines[0].strip()
                CLIENT_SECRET = lines[1].strip()
                print("Using stored credentials from spotify_credentials.txt.")
            else:
                print("Credentials file is invalid. Please delete spotify_credentials.txt and restart.")
                exit()

    return CLIENT_ID, CLIENT_SECRET

# Function to authenticate with Spotify using credentials
def authenticate_spotify():
    print("Retrieving Spotify credentials...")
    CLIENT_ID, CLIENT_SECRET = get_spotify_credentials()

    REDIRECT_URI = 'http://localhost:8888/callback'  # Or any valid redirect URI you specified in the dashboard
    scope = 'playlist-read-private user-library-read'

    print("Attempting Spotify authentication...")
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                       client_secret=CLIENT_SECRET,
                                                       redirect_uri=REDIRECT_URI,
                                                       scope=scope))
        print("Authentication successful!")
        return sp
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None

# Fetch user's playlists directly
print("Starting Spotify authentication process...")
sp = authenticate_spotify()

# Check if authentication was successful
if sp:
    print("Fetching playlists...")
    try:
        playlists = sp.current_user_playlists()
        if playlists['items']:
            print("Your Playlists:")
            for playlist in playlists['items']:
                print(playlist['name'])
        else:
            print("No playlists found.")
    except Exception as e:
        print(f"Error fetching playlists: {e}")
else:
    print("Failed to authenticate with Spotify.")
