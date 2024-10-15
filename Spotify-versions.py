# #---------Authenticating the Spotify--------------
# # This will redirect you to spotify account and open a tab to ask from me to allow the spotify authentication
#
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
#
# # Replace these values with your actual app credentials
# CLIENT_ID = '73fd2279603045b49d68084af873086a'
# CLIENT_SECRET = 'c3ff6198efaa40ab9ceef968ade83f6a'
# REDIRECT_URI = 'http://localhost:8888/callback'  # or any valid redirect URI you specified in the dashboard
#
# # Set up the scope for accessing playlists
# scope = 'playlist-read-private'
#
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
#                                                client_secret=CLIENT_SECRET,
#                                                redirect_uri=REDIRECT_URI,
#                                                scope=scope))
#
# # Example: Fetching your playlists
# playlists = sp.current_user_playlists()
# for playlist in playlists['items']:
#     print(playlist['name'])


# #---------Version 2--------------
# # This will fetch the all liked song from the spotify and print them on console
#
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
#
# # Replace these values with your actual app credentials
# CLIENT_ID = '73fd2279603045b49d68084af873086a'
# CLIENT_SECRET = 'c3ff6198efaa40ab9ceef968ade83f6a'
# REDIRECT_URI = 'http://localhost:8888/callback'  # or any valid redirect URI you specified in the dashboard
#
# # Set up the scope for accessing saved tracks (liked songs)
# scope = 'user-library-read'
#
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
#                                                client_secret=CLIENT_SECRET,
#                                                redirect_uri=REDIRECT_URI,
#                                                scope=scope))
#
# # Function to fetch all liked songs using pagination
# def get_all_liked_songs(sp):
#     results = sp.current_user_saved_tracks(limit=50)
#     tracks = []
#     while results:
#         for item in results['items']:
#             track = item['track']
#             tracks.append(f"{track['name']} by {track['artists'][0]['name']}")
#         if results['next']:
#             results = sp.next(results)  # Fetch the next page of results
#         else:
#             results = None
#     return tracks
#
# # Fetch and print all liked songs
# liked_songs = get_all_liked_songs(sp)
# for idx, song in enumerate(liked_songs, 1):
#     print(f"{idx}. {song}")


# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
# import csv
#
# # Replace these values with your actual app credentials
# CLIENT_ID = '73fd2279603045b49d68084af873086a'
# CLIENT_SECRET = 'c3ff6198efaa40ab9ceef968ade83f6a'
# REDIRECT_URI = 'http://localhost:8888/callback'  # or any valid redirect URI you specified in the dashboard
#
# # Set up the scope for accessing saved tracks (liked songs)
# scope = 'user-library-read'
#
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
#                                                client_secret=CLIENT_SECRET,
#                                                redirect_uri=REDIRECT_URI,
#                                                scope=scope))
#
# # Function to fetch all liked songs using pagination
# def get_all_liked_songs(sp):
#     results = sp.current_user_saved_tracks(limit=50)
#     tracks = []
#     while results:
#         for item in results['items']:
#             track = item['track']
#             tracks.append([track['name'], track['artists'][0]['name']])  # Save song name and artist as a list
#         if results['next']:
#             results = sp.next(results)  # Fetch the next page of results
#         else:
#             results = None
#     return tracks
#
# # Save the liked songs to a CSV file
# def save_songs_to_csv(songs, filename='liked_songs.csv'):
#     with open(filename, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(['Song Name', 'Artist Name'])  # Header row
#         writer.writerows(songs)  # Write the list of songs
#
# # Fetch liked songs
# liked_songs = get_all_liked_songs(sp)
#
# # Save liked songs to a CSV file
# save_songs_to_csv(liked_songs)
#
# print(f"Saved {len(liked_songs)} songs to 'liked_songs.csv'")

#------------ Download the spotify song in webm format-----------------

# import csv
# import yt_dlp
# import os
#
#
# # Function to download song from YouTube using yt-dlp
# def download_song(song_name, artist_name, download_dir='songs'):
#     # Create the search query with song name and artist
#     query = f"{song_name} {artist_name} audio"
#
#     # Generate the expected file path
#     file_path = os.path.join(download_dir, f"{song_name} by {artist_name}.mp3")
#
#     # Check if the song is already downloaded
#     if os.path.exists(file_path):
#         print(f"'{song_name} by {artist_name}' is already downloaded. Skipping...")
#         return
#
#     # Set download options for yt-dlp
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }],
#         'outtmpl': os.path.join(download_dir, f'{song_name} by {artist_name}.%(ext)s'),
#         # Save with song name and artist
#         'noplaylist': True,  # Avoid downloading playlists
#         'quiet': True  # Suppress output
#     }
#
#     # Search and download the song from YouTube
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         try:
#             print(f"Searching and downloading: {query}")
#             ydl.download([f"ytsearch1:{query}"])
#         except Exception as e:
#             print(f"Error downloading {song_name} by {artist_name}: {e}")
#
#
# # Function to read songs from CSV and download them
# def download_songs_from_csv(csv_filename, download_dir='songs'):
#     # Create the download directory if it doesn't exist
#     if not os.path.exists(download_dir):
#         os.makedirs(download_dir)
#
#     # Read songs from CSV
#     with open(csv_filename, newline='', encoding='utf-8') as csvfile:
#         reader = csv.reader(csvfile)
#         next(reader)  # Skip the header row
#         for row in reader:
#             song_name, artist_name = row
#             download_song(song_name, artist_name, download_dir)
#
#
# # Specify the CSV file containing liked songs
# csv_filename = 'liked_songs.csv'
#
# # Start downloading songs
# download_songs_from_csv(csv_filename)



# #----------------Convert webm to mp3 (Covertor)---------------
#
# from moviepy.editor import AudioFileClip
#
# def convert_webm_to_mp3(input_file, output_file):
#     try:
#         # Load the .webm file
#         audio_clip = AudioFileClip(input_file)
#
#         # Write the audio to an .mp3 file
#         audio_clip.write_audiofile(output_file, codec='mp3')
#
#         # Close the audio file
#         audio_clip.close()
#
#         print(f"Conversion successful: {output_file}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#
# # Example usage
# input_webm_file = 'C:\\Users\\mehmo\\Downloads\\mp3downloader\\songs\\Gulabi Ankhen - From #The Train# by Mohammed Rafi.webm'  # Path to your .webm file
# output_mp3_file = 'output.mp3'    # Path where the .mp3 file will be saved
#
# convert_webm_to_mp3(input_webm_file, output_mp3_file)



#-------------------------Version 5----------------------------
# It will download the song in the webm and then convert the file to the mp3 format

# import csv
# import yt_dlp
# import os
# from moviepy.editor import AudioFileClip
# import re  # Import regex for sanitizing file names
#
#
# # Function to sanitize file names by removing/replacing problematic characters
# def sanitize_filename(filename):
#     return re.sub(r'[\\/*?:"<>|]', '_', filename)  # Replaces problematic characters with underscore
#
#
# # Function to convert WEBM to MP3 using moviepy
# def convert_webm_to_mp3(input_file, output_file_name, output_dir):
#     try:
#         # Load the .webm file
#         audio_clip = AudioFileClip(input_file)
#
#         # Generate full MP3 path
#         output_file_path = os.path.join(output_dir, output_file_name)
#
#         # Write the audio to an .mp3 file
#         audio_clip.write_audiofile(output_file_path, codec='mp3')
#
#         # Close the audio file
#         audio_clip.close()
#
#         print(f"Conversion successful: {output_file_path}")
#     except Exception as e:
#         print(f"An error occurred during conversion: {e}")
#
#
# # Function to download song from YouTube using yt-dlp
# def download_song(song_name, artist_name, download_dir='songs'):
#     # Create the search query with song name and artist
#     query = f"{song_name} {artist_name} audio"
#
#     # Sanitize the file names
#     sanitized_song_name = sanitize_filename(f"{song_name} by {artist_name}")
#
#     # Generate the expected file paths
#     webm_file_path = os.path.join(download_dir, f"{sanitized_song_name}.webm")
#     mp3_file_name = f"{sanitized_song_name}.mp3"  # Only the MP3 filename
#     mp3_file_path = os.path.join(download_dir, mp3_file_name)  # Full path for checking
#
#     # Check if the mp3 version of the song is already downloaded
#     if os.path.exists(mp3_file_path):
#         print(f"'{song_name} by {artist_name}' is already downloaded as MP3. Skipping...")
#         return
#
#     # Set download options for yt-dlp
#     ydl_opts = {
#         'format': 'bestaudio[ext=webm]/bestaudio',  # Explicitly download the best audio in webm format
#         'outtmpl': webm_file_path,  # Save as .webm
#         'noplaylist': True,  # Avoid downloading playlists
#         'quiet': True  # Suppress output
#     }
#
#     # Search and download the song from YouTube
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         try:
#             print(f"Searching and downloading: {query}")
#             ydl.download([f"ytsearch1:{query}"])
#             print(f"Downloaded: {webm_file_path}")
#
#             # Immediately convert the downloaded file to mp3
#             convert_webm_to_mp3(webm_file_path, mp3_file_name, download_dir)
#
#             # Optionally, delete the webm file after conversion
#             if os.path.exists(webm_file_path):
#                 os.remove(webm_file_path)
#                 print(f"Deleted temporary file: {webm_file_path}")
#         except Exception as e:
#             print(f"Error downloading {song_name} by {artist_name}: {e}")
#
#
# # Function to read songs from CSV and download them
# def download_songs_from_csv(csv_filename, download_dir='songs'):
#     # Create the download directory if it doesn't exist
#     if not os.path.exists(download_dir):
#         os.makedirs(download_dir)
#
#     # Read songs from CSV
#     with open(csv_filename, newline='', encoding='utf-8') as csvfile:
#         reader = csv.reader(csvfile)
#         next(reader)  # Skip the header row
#         for row in reader:
#             song_name, artist_name = row
#             download_song(song_name, artist_name, download_dir)
#
#
# # Specify the CSV file containing liked songs
# csv_filename = 'liked_songs.csv'
#
# # Start downloading songs and convert to MP3
# download_songs_from_csv(csv_filename)


# #------------------Version 6--------------------
# # Integrated code with the functionality. It will authenticate the spotify and then dispaly playlist and start downloading the playlists
#
# import csv
# import yt_dlp
# import os
# from moviepy.editor import AudioFileClip
# import re  # Import regex for sanitizing file names
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
#
# # Function to sanitize file names by removing/replacing problematic characters
# def sanitize_filename(filename):
#     return re.sub(r'[\\/*?:"<>|]', '_', filename)  # Replaces problematic characters with underscore
#
# # Function to convert WEBM to MP3 using moviepy
# def convert_webm_to_mp3(input_file, output_file_name, output_dir):
#     try:
#         # Load the .webm file
#         audio_clip = AudioFileClip(input_file)
#
#         # Generate full MP3 path
#         output_file_path = os.path.join(output_dir, output_file_name)
#
#         # Write the audio to an .mp3 file
#         audio_clip.write_audiofile(output_file_path, codec='mp3')
#
#         # Close the audio file
#         audio_clip.close()
#
#         print(f"Conversion successful: {output_file_path}")
#     except Exception as e:
#         print(f"An error occurred during conversion: {e}")
#
# # Function to download song from YouTube using yt-dlp
# def download_song(song_name, artist_name, download_dir='songs'):
#     # Create the search query with song name and artist
#     query = f"{song_name} {artist_name} audio"
#
#     # Sanitize the file names
#     sanitized_song_name = sanitize_filename(f"{song_name} by {artist_name}")
#
#     # Generate the expected file paths
#     webm_file_path = os.path.join(download_dir, f"{sanitized_song_name}.webm")
#     mp3_file_name = f"{sanitized_song_name}.mp3"  # Only the MP3 filename
#     mp3_file_path = os.path.join(download_dir, mp3_file_name)  # Full path for checking
#
#     # Check if the mp3 version of the song is already downloaded
#     if os.path.exists(mp3_file_path):
#         print(f"'{song_name} by {artist_name}' is already downloaded as MP3. Skipping...")
#         return
#
#     # Set download options for yt-dlp
#     ydl_opts = {
#         'format': 'bestaudio[ext=webm]/bestaudio',  # Explicitly download the best audio in webm format
#         'outtmpl': webm_file_path,  # Save as .webm
#         'noplaylist': True,  # Avoid downloading playlists
#         'quiet': True  # Suppress output
#     }
#
#     # Search and download the song from YouTube
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         try:
#             print(f"Searching and downloading: {query}")
#             ydl.download([f"ytsearch1:{query}"])
#             print(f"Downloaded: {webm_file_path}")
#
#             # Immediately convert the downloaded file to mp3
#             convert_webm_to_mp3(webm_file_path, mp3_file_name, download_dir)
#
#             # Optionally, delete the webm file after conversion
#             if os.path.exists(webm_file_path):
#                 os.remove(webm_file_path)
#                 print(f"Deleted temporary file: {webm_file_path}")
#         except Exception as e:
#             print(f"Error downloading {song_name} by {artist_name}: {e}")
#
# # Function to authenticate with Spotify and get playlists
# def authenticate_spotify():
#     CLIENT_ID = '73fd2279603045b49d68084af873086a'
#     CLIENT_SECRET = 'c3ff6198efaa40ab9ceef968ade83f6a'
#     REDIRECT_URI = 'http://localhost:8888/callback'  # or any valid redirect URI you specified in the dashboard
#
#     scope = 'playlist-read-private user-library-read'
#     sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
#                                                    client_secret=CLIENT_SECRET,
#                                                    redirect_uri=REDIRECT_URI,
#                                                    scope=scope))
#     return sp
#
# # Function to get user's playlists
# def get_user_playlists(sp):
#     playlists = sp.current_user_playlists()
#     return playlists['items']
#
# # Function to fetch songs from a selected playlist
# def fetch_songs_from_playlist(sp, playlist_id):
#     tracks = []
#     results = sp.playlist_items(playlist_id, limit=100)  # Adjust limit as needed
#     for item in results['items']:
#         track = item['track']
#         tracks.append([track['name'], track['artists'][0]['name']])  # Save song name and artist as a list
#     return tracks
#
# # Function to save songs to a CSV file
# def save_songs_to_csv(songs, filename='liked_songs.csv'):
#     with open(filename, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(['Song Name', 'Artist Name'])  # Header row
#         writer.writerows(songs)  # Write the list of songs
#
# # Function to download songs from a selected playlist
# def download_songs_from_playlist(sp, playlist_id, download_dir='songs'):
#     # Fetch songs from the selected playlist
#     songs = fetch_songs_from_playlist(sp, playlist_id)
#     # Save songs to CSV
#     save_songs_to_csv(songs)
#     # Download each song
#     for song_name, artist_name in songs:
#         download_song(song_name, artist_name, download_dir)
#
# # Main execution flow
# if __name__ == '__main__':
#     sp = authenticate_spotify()
#     playlists = get_user_playlists(sp)
#
#     # Display playlists to the user
#     print("Your Playlists:")
#     for i, playlist in enumerate(playlists):
#         print(f"{i + 1}. {playlist['name']} (ID: {playlist['id']})")
#
#     # Ask user to select a playlist
#     selected_index = int(input("Select a playlist by number: ")) - 1
#     selected_playlist_id = playlists[selected_index]['id']
#
#     # Start downloading songs from the selected playlist
#     download_songs_from_playlist(sp, selected_playlist_id)



# #-----------------Version 7-----------------
# # Ask from client about the CLient ID and CLient Key and then display the spotify playlists
# # Based on user input it will start downlaoding the playlist
#
# import csv
# import yt_dlp
# import os
# from moviepy.editor import AudioFileClip
# import re  # Import regex for sanitizing file names
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
#
#
# # Function to sanitize file names by removing/replacing problematic characters
# def sanitize_filename(filename):
#     return re.sub(r'[\\/*?:"<>|]', '_', filename)  # Replaces problematic characters with underscore
#
#
# # Function to convert WEBM to MP3 using moviepy
# def convert_webm_to_mp3(input_file, output_file_name, output_dir):
#     try:
#         # Load the .webm file
#         audio_clip = AudioFileClip(input_file)
#
#         # Generate full MP3 path
#         output_file_path = os.path.join(output_dir, output_file_name)
#
#         # Write the audio to an .mp3 file
#         audio_clip.write_audiofile(output_file_path, codec='mp3')
#
#         # Close the audio file
#         audio_clip.close()
#
#         print(f"Conversion successful: {output_file_path}")
#     except Exception as e:
#         print(f"An error occurred during conversion: {e}")
#
#
# # Function to download song from YouTube using yt-dlp
# def download_song(song_name, artist_name, download_dir='songs'):
#     # Create the search query with song name and artist
#     query = f"{song_name} {artist_name} audio"
#
#     # Sanitize the file names
#     sanitized_song_name = sanitize_filename(f"{song_name} by {artist_name}")
#
#     # Generate the expected file paths
#     mp3_file_name = f"{sanitized_song_name}.mp3"  # Only the MP3 filename
#     mp3_file_path = os.path.join(download_dir, mp3_file_name)  # Full path for checking
#
#     # Check if the mp3 version of the song is already downloaded
#     if os.path.exists(mp3_file_path):
#         print(f"'{song_name} by {artist_name}' is already downloaded as MP3. Skipping...")
#         return
#
#     # Set download options for yt-dlp
#     ydl_opts = {
#         'format': 'bestaudio[ext=webm]/bestaudio',  # Explicitly download the best audio in webm format
#         'outtmpl': os.path.join(download_dir, f"{sanitized_song_name}.webm"),  # Save as .webm
#         'noplaylist': True,  # Avoid downloading playlists
#         'quiet': True  # Suppress output
#     }
#
#     # Search and download the song from YouTube
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         try:
#             print(f"Searching and downloading: {query}")
#             ydl.download([f"ytsearch1:{query}"])
#             print(f"Downloaded: {mp3_file_name}")
#
#             # Immediately convert the downloaded file to mp3
#             convert_webm_to_mp3(os.path.join(download_dir, f"{sanitized_song_name}.webm"), mp3_file_name, download_dir)
#
#             # Optionally, delete the webm file after conversion
#             if os.path.exists(os.path.join(download_dir, f"{sanitized_song_name}.webm")):
#                 os.remove(os.path.join(download_dir, f"{sanitized_song_name}.webm"))
#                 print(f"Deleted temporary file: {sanitized_song_name}.webm")
#         except yt_dlp.utils.DownloadError as e:
#             print(f"Download error for {song_name} by {artist_name}: {e}")
#         except Exception as e:
#             print(f"An error occurred while downloading {song_name} by {artist_name}: {e}")
#
#
# # Function to authenticate with Spotify and get playlists
# def authenticate_spotify(client_id, client_secret):
#     REDIRECT_URI = 'http://localhost:8888/callback'  # or any valid redirect URI you specified in the dashboard
#     scope = 'playlist-read-private user-library-read'
#     sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
#                                                    client_secret=client_secret,
#                                                    redirect_uri=REDIRECT_URI,
#                                                    scope=scope))
#     return sp
#
#
# # Function to get user's playlists
# def get_user_playlists(sp):
#     playlists = sp.current_user_playlists()
#     return playlists['items']
#
#
# # Function to fetch songs from a selected playlist
# def fetch_songs_from_playlist(sp, playlist_id):
#     tracks = []
#     results = sp.playlist_items(playlist_id, limit=100)  # Fetch the first 100 tracks
#     while results:
#         for item in results['items']:
#             track = item['track']
#             tracks.append([track['name'], track['artists'][0]['name']])  # Save song name and artist as a list
#         if results['next']:
#             results = sp.next(results)  # Fetch the next page of results
#         else:
#             break
#     return tracks
#
#
# # Function to save songs to a CSV file
# def save_songs_to_csv(songs, filename='liked_songs.csv'):
#     with open(filename, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(['Song Name', 'Artist Name'])  # Header row
#         writer.writerows(songs)  # Write the list of songs
#
#
# # Function to download songs from a selected playlist
# def download_songs_from_playlist(sp, playlist_id, download_dir='songs'):
#     # Fetch songs from the selected playlist
#     songs = fetch_songs_from_playlist(sp, playlist_id)
#     # Save songs to CSV
#     save_songs_to_csv(songs)
#     # Download each song
#     for song_name, artist_name in songs:
#         download_song(song_name, artist_name, download_dir)
#
#
# # Main execution flow
# if __name__ == '__main__':
#     # Prompt user for Spotify credentials
#     client_id = input("Enter your Spotify Client ID: ")
#     client_secret = input("Enter your Spotify Client Secret: ")
#
#     sp = authenticate_spotify(client_id, client_secret)
#     playlists = get_user_playlists(sp)
#
#     # Display playlists to the user
#     print("Your Playlists:")
#     for i, playlist in enumerate(playlists):
#         print(f"{i + 1}. {playlist['name']} (ID: {playlist['id']})")
#
#     # Ask user to select a playlist
#     try:
#         selected_index = int(input("Select a playlist by number: ")) - 1
#         selected_playlist_id = playlists[selected_index]['id']
#
#         # Start downloading songs from the selected playlist
#         download_songs_from_playlist(sp, selected_playlist_id)
#     except (IndexError, ValueError):
#         print("Invalid selection. Please enter a valid playlist number.")



# #-----------------Version 8-----------------
# # Added functionality to save the CSV file with the playlist name
# # And ask the user if they want to start again after downloading.
# # More good exception handling
# # Skip aleady downlaoded
#
# import csv
# import yt_dlp
# import os
# from moviepy.editor import AudioFileClip
# import re  # Import regex for sanitizing file names
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
#
# # Function to sanitize file names by removing/replacing problematic characters
# def sanitize_filename(filename):
#     return re.sub(r'[\\/*?:"<>|]', '_', filename)  # Replaces problematic characters with underscore
#
# # Function to convert WEBM to MP3 using moviepy
# def convert_webm_to_mp3(input_file, output_file_name, output_dir):
#     try:
#         # Load the .webm file
#         audio_clip = AudioFileClip(input_file)
#
#         # Generate full MP3 path
#         output_file_path = os.path.join(output_dir, output_file_name)
#
#         # Write the audio to an .mp3 file
#         audio_clip.write_audiofile(output_file_path, codec='mp3')
#
#         # Close the audio file
#         audio_clip.close()
#
#         print(f"Conversion successful: {output_file_path}")
#     except Exception as e:
#         print(f"An error occurred during conversion: {e}")
#
# # Function to download song from YouTube using yt-dlp
# def download_song(song_name, artist_name, download_dir='songs'):
#     # Create the search query with song name and artist
#     query = f"{song_name} {artist_name} audio"
#
#     # Sanitize the file names
#     sanitized_song_name = sanitize_filename(f"{song_name} by {artist_name}")
#
#     # Generate the expected file paths
#     mp3_file_name = f"{sanitized_song_name}.mp3"  # Only the MP3 filename
#     mp3_file_path = os.path.join(download_dir, mp3_file_name)  # Full path for checking
#
#     # Check if the mp3 version of the song is already downloaded
#     if os.path.exists(mp3_file_path):
#         print(f"'{song_name} by {artist_name}' is already downloaded as MP3. Skipping...")
#         return
#
#     # Set download options for yt-dlp
#     ydl_opts = {
#         'format': 'bestaudio[ext=webm]/bestaudio',  # Explicitly download the best audio in webm format
#         'outtmpl': os.path.join(download_dir, f"{sanitized_song_name}.webm"),  # Save as .webm
#         'noplaylist': True,  # Avoid downloading playlists
#         'quiet': True  # Suppress output
#     }
#
#     # Search and download the song from YouTube
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         try:
#             print(f"Searching and downloading: {query}")
#             ydl.download([f"ytsearch1:{query}"])
#             print(f"Downloaded: {mp3_file_name}")
#
#             # Immediately convert the downloaded file to mp3
#             convert_webm_to_mp3(os.path.join(download_dir, f"{sanitized_song_name}.webm"), mp3_file_name, download_dir)
#
#             # Optionally, delete the webm file after conversion
#             if os.path.exists(os.path.join(download_dir, f"{sanitized_song_name}.webm")):
#                 os.remove(os.path.join(download_dir, f"{sanitized_song_name}.webm"))
#                 print(f"Deleted temporary file: {sanitized_song_name}.webm")
#         except yt_dlp.utils.DownloadError as e:
#             print(f"Download error for {song_name} by {artist_name}: {e}")
#         except Exception as e:
#             print(f"An error occurred while downloading {song_name} by {artist_name}: {e}")
#
# # Function to authenticate with Spotify and get playlists
# def authenticate_spotify(client_id, client_secret):
#     REDIRECT_URI = 'http://localhost:8888/callback'  # or any valid redirect URI you specified in the dashboard
#     scope = 'playlist-read-private user-library-read'
#     sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
#                                                    client_secret=client_secret,
#                                                    redirect_uri=REDIRECT_URI,
#                                                    scope=scope))
#     return sp
#
# # Function to get user's playlists
# def get_user_playlists(sp):
#     playlists = sp.current_user_playlists()
#     return playlists['items']
#
# # Function to fetch songs from a selected playlist
# def fetch_songs_from_playlist(sp, playlist_id):
#     tracks = []
#     results = sp.playlist_items(playlist_id, limit=100)  # Fetch the first 100 tracks
#     while results:
#         for item in results['items']:
#             track = item['track']
#             tracks.append([track['name'], track['artists'][0]['name']])  # Save song name and artist as a list
#         if results['next']:
#             results = sp.next(results)  # Fetch the next page of results
#         else:
#             break
#     return tracks
#
# # Function to save songs to a CSV file with the playlist name
# def save_songs_to_csv(songs, playlist_name):
#     filename = sanitize_filename(f"{playlist_name}.csv")  # Sanitize playlist name for filename
#     with open(filename, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(['Song Name', 'Artist Name'])  # Header row
#         writer.writerows(songs)  # Write the list of songs
#     print(f"Playlist saved to: {filename}")
#
# # Function to download songs from a selected playlist
# def download_songs_from_playlist(sp, playlist_id, playlist_name, download_dir='songs'):
#     # Fetch songs from the selected playlist
#     songs = fetch_songs_from_playlist(sp, playlist_id)
#     # Save songs to CSV
#     save_songs_to_csv(songs, playlist_name)
#     # Download each song
#     for song_name, artist_name in songs:
#         download_song(song_name, artist_name, download_dir)
#
# # Main execution flow
# if __name__ == '__main__':
#     while True:
#         # Prompt user for Spotify credentials
#         client_id = input("Enter your Spotify Client ID: ")
#         client_secret = input("Enter your Spotify Client Secret: ")
#
#         sp = authenticate_spotify(client_id, client_secret)
#         playlists = get_user_playlists(sp)
#
#         # Display playlists to the user
#         print("Your Playlists:")
#         for i, playlist in enumerate(playlists):
#             print(f"{i + 1}. {playlist['name']} (ID: {playlist['id']})")
#
#         # Ask user to select a playlist
#         try:
#             selected_index = int(input("Select a playlist by number: ")) - 1
#             selected_playlist = playlists[selected_index]
#             selected_playlist_id = selected_playlist['id']
#             selected_playlist_name = selected_playlist['name']
#
#             # Start downloading songs from the selected playlist
#             download_songs_from_playlist(sp, selected_playlist_id, selected_playlist_name)
#
#             # Ask the user if they want to download another playlist
#             restart = input("Do you want to download another playlist? (yes/no): ").strip().lower()
#             if restart != 'yes':
#                 print("Exiting the program. Goodbye!")
#                 break
#         except (IndexError, ValueError):
#             print("Invalid selection. Please enter a valid playlist number.")


# #-----------------Version 8-----------------
# # Added functionality to save the CSV file with the playlist name
# # And ask the user if they want to start again after downloading.
# # More good exception handling
# # Skip aleady downlaoded
# # Check for the custom csv file if user want to enter that or not
#
#
# import csv
# import yt_dlp
# import os
# from moviepy.editor import AudioFileClip
# import re  # Import regex for sanitizing file names
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
#
#
# # Function to sanitize file names by removing/replacing problematic characters
# def sanitize_filename(filename):
#     return re.sub(r'[\\/*?:"<>|]', '_', filename)  # Replaces problematic characters with underscore
#
#
# # Function to convert WEBM to MP3 using moviepy
# def convert_webm_to_mp3(input_file, output_file_name, output_dir):
#     try:
#         audio_clip = AudioFileClip(input_file)
#         output_file_path = os.path.join(output_dir, output_file_name)
#         audio_clip.write_audiofile(output_file_path, codec='mp3')
#         audio_clip.close()
#         print(f"Conversion successful: {output_file_path}")
#     except Exception as e:
#         print(f"An error occurred during conversion: {e}")
#
#
# # Function to download song from YouTube using yt-dlp
# def download_song(song_name, artist_name, download_dir='songs'):
#     query = f"{song_name} {artist_name} audio"
#     sanitized_song_name = sanitize_filename(f"{song_name} by {artist_name}")
#     mp3_file_name = f"{sanitized_song_name}.mp3"
#     mp3_file_path = os.path.join(download_dir, mp3_file_name)
#
#     if os.path.exists(mp3_file_path):
#         print(f"'{song_name} by {artist_name}' is already downloaded as MP3. Skipping...")
#         return
#
#     ydl_opts = {
#         'format': 'bestaudio[ext=webm]/bestaudio',
#         'outtmpl': os.path.join(download_dir, f"{sanitized_song_name}.webm"),
#         'noplaylist': True,
#         'quiet': True
#     }
#
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         try:
#             print(f"Searching and downloading: {query}")
#             ydl.download([f"ytsearch1:{query}"])
#             print(f"Downloaded: {mp3_file_name}")
#
#             convert_webm_to_mp3(os.path.join(download_dir, f"{sanitized_song_name}.webm"), mp3_file_name, download_dir)
#
#             if os.path.exists(os.path.join(download_dir, f"{sanitized_song_name}.webm")):
#                 os.remove(os.path.join(download_dir, f"{sanitized_song_name}.webm"))
#                 print(f"Deleted temporary file: {sanitized_song_name}.webm")
#         except yt_dlp.utils.DownloadError as e:
#             print(f"Download error for {song_name} by {artist_name}: {e}")
#         except Exception as e:
#             print(f"An error occurred while downloading {song_name} by {artist_name}: {e}")
#
#
# # Function to authenticate with Spotify and get playlists
# def authenticate_spotify(client_id, client_secret):
#     REDIRECT_URI = 'http://localhost:8888/callback'
#     scope = 'playlist-read-private user-library-read'
#     sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
#                                                    client_secret=client_secret,
#                                                    redirect_uri=REDIRECT_URI,
#                                                    scope=scope))
#     return sp
#
#
# # Function to get user's playlists
# def get_user_playlists(sp):
#     playlists = sp.current_user_playlists()
#     return playlists['items']
#
#
# # Function to fetch songs from a selected playlist
# def fetch_songs_from_playlist(sp, playlist_id):
#     tracks = []
#     results = sp.playlist_items(playlist_id, limit=100)
#     while results:
#         for item in results['items']:
#             track = item['track']
#             tracks.append([track['name'], track['artists'][0]['name']])
#         if results['next']:
#             results = sp.next(results)
#         else:
#             break
#     return tracks
#
#
# # Function to save songs to a CSV file
# def save_songs_to_csv(songs, playlist_name):
#     filename = sanitize_filename(f"{playlist_name}.csv")
#     with open(filename, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(['Song Name', 'Artist Name'])
#         writer.writerows(songs)
#     print(f"Playlist saved to: {filename}")
#
#
# # Function to download songs from a selected playlist
# def download_songs_from_playlist(sp, playlist_id, playlist_name, download_dir='songs'):
#     songs = fetch_songs_from_playlist(sp, playlist_id)
#     save_songs_to_csv(songs, playlist_name)
#     for song_name, artist_name in songs:
#         download_song(song_name, artist_name, download_dir)
#
#
# # Function to download songs from a user-provided CSV file
# def download_songs_from_csv(csv_file_path, download_dir='songs'):
#     try:
#         with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 song_name = row.get('Song Name', '').strip()
#                 artist_name = row.get('Artist Name', '').strip()
#                 if song_name and artist_name:
#                     download_song(song_name, artist_name, download_dir)
#                 else:
#                     print(f"Invalid entry in CSV: {row}")
#     except FileNotFoundError:
#         print(f"CSV file '{csv_file_path}' not found.")
#     except Exception as e:
#         print(f"An error occurred while processing CSV file: {e}")
#
#
# # Main execution flow
# if __name__ == '__main__':
#     while True:
#         choice = input(
#             "Do you want to (1) use Spotify playlist or (2) provide your own CSV file? Enter 1 or 2: ").strip()
#
#         if choice == '1':
#             client_id = input("Enter your Spotify Client ID: ")
#             client_secret = input("Enter your Spotify Client Secret: ")
#             sp = authenticate_spotify(client_id, client_secret)
#             playlists = get_user_playlists(sp)
#
#             print("Your Playlists:")
#             for i, playlist in enumerate(playlists):
#                 print(f"{i + 1}. {playlist['name']} (ID: {playlist['id']})")
#
#             try:
#                 selected_index = int(input("Select a playlist by number: ")) - 1
#                 selected_playlist = playlists[selected_index]
#                 selected_playlist_id = selected_playlist['id']
#                 selected_playlist_name = selected_playlist['name']
#
#                 download_songs_from_playlist(sp, selected_playlist_id, selected_playlist_name)
#
#                 restart = input("Do you want to download another playlist? (yes/no): ").strip().lower()
#                 if restart != 'yes':
#                     print("Exiting the program. Goodbye!")
#                     break
#             except (IndexError, ValueError):
#                 print("Invalid selection. Please enter a valid playlist number.")
#         elif choice == '2':
#             csv_file_path = input("Enter the full path to your CSV file: ").strip()
#             download_songs_from_csv(csv_file_path)
#
#             restart = input("Do you want to start the SpotiFly again? (yes/no): ").strip().lower()
#             if restart != 'yes':
#                 print("Exiting the program. Goodbye!")
#                 break
#         else:
#             print("Invalid choice. Please enter 1 or 2.")



# #-----------------Version 9-----------------
# # Added functionality to save the CSV file with the playlist name
# # And ask the user if they want to start again after downloading.
# # More good exception handling
# # Skip aleady downlaoded
# # Check for the custom csv file if user want to enter that or not
# # Skip asking for the key if the .cache file already exist in the directory.
#
# import csv
# import yt_dlp
# import os
# from moviepy.editor import AudioFileClip
# import re  # Import regex for sanitizing file names
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
#
# # Function to sanitize file names by removing/replacing problematic characters
# def sanitize_filename(filename):
#     return re.sub(r'[\\/*?:"<>|]', '_', filename)  # Replaces problematic characters with underscore
#
#
# # Function to convert WEBM to MP3 using moviepy
# def convert_webm_to_mp3(input_file, output_file_name, output_dir):
#     try:
#         audio_clip = AudioFileClip(input_file)
#         output_file_path = os.path.join(output_dir, output_file_name)
#         audio_clip.write_audiofile(output_file_path, codec='mp3')
#         audio_clip.close()
#         print(f"Conversion successful: {output_file_path}")
#     except Exception as e:
#         print(f"An error occurred during conversion: {e}")
#
#
# # Function to download song from YouTube using yt-dlp
# def download_song(song_name, artist_name, download_dir='songs'):
#     query = f"{song_name} {artist_name} audio"
#     sanitized_song_name = sanitize_filename(f"{song_name} by {artist_name}")
#     mp3_file_name = f"{sanitized_song_name}.mp3"
#     mp3_file_path = os.path.join(download_dir, mp3_file_name)
#
#     if os.path.exists(mp3_file_path):
#         print(f"'{song_name} by {artist_name}' is already downloaded as MP3. Skipping...")
#         return
#
#     ydl_opts = {
#         'format': 'bestaudio[ext=webm]/bestaudio',
#         'outtmpl': os.path.join(download_dir, f"{sanitized_song_name}.webm"),
#         'noplaylist': True,
#         'quiet': True
#     }
#
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         try:
#             print(f"Searching and downloading: {query}")
#             ydl.download([f"ytsearch1:{query}"])
#             print(f"Downloaded: {mp3_file_name}")
#
#             convert_webm_to_mp3(os.path.join(download_dir, f"{sanitized_song_name}.webm"), mp3_file_name, download_dir)
#
#             if os.path.exists(os.path.join(download_dir, f"{sanitized_song_name}.webm")):
#                 os.remove(os.path.join(download_dir, f"{sanitized_song_name}.webm"))
#                 print(f"Deleted temporary file: {sanitized_song_name}.webm")
#         except yt_dlp.utils.DownloadError as e:
#             print(f"Download error for {song_name} by {artist_name}: {e}")
#         except Exception as e:
#             print(f"An error occurred while downloading {song_name} by {artist_name}: {e}")
#
#
# # Function to authenticate with Spotify and get playlists
# def authenticate_spotify():
#     # Check if the .cache file exists
#     cache_file_path = '.cache'
#
#     if os.path.exists(cache_file_path):
#         # If the cache file exists, skip asking for client credentials
#         print("Using stored credentials from .cache. No need to provide client ID and secret.")
#         sp = spotipy.Spotify(auth_manager=SpotifyOAuth())
#     else:
#         # If no cache file, ask for client credentials
#         client_id = input("Enter your Spotify Client ID: ")
#         client_secret = input("Enter your Spotify Client Secret: ")
#         REDIRECT_URI = 'http://localhost:8888/callback'
#         scope = 'playlist-read-private user-library-read'
#         sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
#                                                        client_secret=client_secret,
#                                                        redirect_uri=REDIRECT_URI,
#                                                        scope=scope))
#     return sp
#
#
# # Function to get user's playlists
# def get_user_playlists(sp):
#     playlists = sp.current_user_playlists()
#     return playlists['items']
#
#
# # Function to fetch songs from a selected playlist
# def fetch_songs_from_playlist(sp, playlist_id):
#     tracks = []
#     results = sp.playlist_items(playlist_id, limit=100)
#     while results:
#         for item in results['items']:
#             track = item['track']
#             tracks.append([track['name'], track['artists'][0]['name']])
#         if results['next'] != None:
#             results = sp.next(results)
#         else:
#             break
#     return tracks
#
#
# # Function to save songs to a CSV file
# def save_songs_to_csv(songs, playlist_name):
#     filename = sanitize_filename(f"{playlist_name}.csv")
#     with open(filename, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(['Song Name', 'Artist Name'])
#         writer.writerows(songs)
#     print(f"Playlist saved to: {filename}")
#
#
# # Function to download songs from a selected playlist
# def download_songs_from_playlist(sp, playlist_id, playlist_name, download_dir='songs'):
#     songs = fetch_songs_from_playlist(sp, playlist_id)
#     save_songs_to_csv(songs, playlist_name)
#     for song_name, artist_name in songs:
#         download_song(song_name, artist_name, download_dir)
#
#
# # Function to download songs from a user-provided CSV file
# def download_songs_from_csv(csv_file_path, download_dir='songs'):
#     try:
#         with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 song_name = row.get('Song Name', '').strip()
#                 artist_name = row.get('Artist Name', '').strip()
#                 if song_name and artist_name:
#                     download_song(song_name, artist_name, download_dir)
#                 else:
#                     print(f"Invalid entry in CSV: {row}")
#     except FileNotFoundError:
#         print(f"CSV file '{csv_file_path}' not found.")
#     except Exception as e:
#         print(f"An error occurred while processing CSV file: {e}")
#
#
# # Main execution flow
# if __name__ == '__main__':
#     while True:
#         choice = input(
#             "Do you want to (1) use Spotify playlist or (2) provide your own CSV file? Enter 1 or 2: ").strip()
#
#         if choice == '1':
#             sp = authenticate_spotify()
#             playlists = get_user_playlists(sp)
#
#             print("Your Playlists:")
#             for i, playlist in enumerate(playlists):
#                 print(f"{i + 1}. {playlist['name']} (ID: {playlist['id']})")
#
#             try:
#                 selected_index = int(input("Select a playlist by number: ")) - 1
#                 selected_playlist = playlists[selected_index]
#                 selected_playlist_id = selected_playlist['id']
#                 selected_playlist_name = selected_playlist['name']
#
#                 download_songs_from_playlist(sp, selected_playlist_id, selected_playlist_name)
#
#                 restart = input("Do you want to download another playlist? (yes/no): ").strip().lower()
#                 if restart != 'yes':
#                     print("Exiting the program. Goodbye!")
#                     break
#             except (IndexError, ValueError):
#                 print("Invalid selection. Please enter a valid playlist number.")
#         elif choice == '2':
#             csv_file_path = input("Enter the full path to your CSV file: ").strip()
#             download_songs_from_csv(csv_file_path)
#
#             restart = input("Do you want to start the SpotiFly again? (yes/no): ").strip().lower()
#             if restart != 'yes':
#                 print("Exiting the program. Goodbye!")
#                 break
#         else:
#             print("Invalid choice. Please enter 1 or 2.")


