# spoti_fly/spotify_utils.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def save_credentials_to_file(client_id, client_secret, file_path='spotify_credentials.txt'):
    try:
        with open(file_path, 'w') as f:
            f.write(f"{client_id}\n{client_secret}\n")
        print(f"Spotify credentials saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving credentials: {e}")

def read_credentials_from_file(file_path='spotify_credentials.txt'):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            client_id = lines[0].strip()
            client_secret = lines[1].strip()
            return client_id, client_secret
    except Exception as e:
        print(f"An error occurred while reading credentials: {e}")
        return None, None

def authenticate_spotify():
    client_id, client_secret = read_credentials_from_file()

    if client_id is None or client_secret is None:
        client_id = input("Enter your Spotify Client ID: ")
        client_secret = input("Enter your Spotify Client Secret: ")
        save_credentials_to_file(client_id, client_secret)

    REDIRECT_URI = 'http://localhost:8888/callback'
    scope = 'playlist-read-private user-library-read'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=REDIRECT_URI,
                                                   scope=scope))
    return sp

def get_user_playlists(sp):
    try:
        playlists = sp.current_user_playlists()
        return playlists['items']
    except Exception as e:
        print(f"An error occurred while fetching playlists: {e}")
        return []

def fetch_songs_from_playlist(sp, playlist_id):
    tracks = []
    try:
        results = sp.playlist_items(playlist_id, limit=100)
        while results:
            for item in results['items']:
                track = item['track']
                tracks.append([track['name'], track['artists'][0]['name']])
            if results['next'] is not None:
                results = sp.next(results)
            else:
                break
    except Exception as e:
        print(f"An error occurred while fetching songs from the playlist: {e}")
    return tracks

def save_songs_to_csv(songs, playlist_name):
    import csv
    from .downloader import sanitize_filename
    filename = sanitize_filename(f"{playlist_name}.csv")
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Song Name', 'Artist Name'])
        writer.writerows(songs)
    print(f"Playlist saved to: {filename}")
