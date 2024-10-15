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
# # Function to save Spotify credentials to a text file
# def save_credentials_to_file(client_id, client_secret, file_path='spotify_credentials.txt'):
#     try:
#         with open(file_path, 'w') as f:
#             f.write(f"Client ID: {client_id}\n")
#             f.write(f"Client Secret: {client_secret}\n")
#         print(f"Spotify credentials saved to {file_path}")
#     except Exception as e:
#         print(f"An error occurred while saving credentials: {e}")
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
#
#         # Save the credentials to a text file
#         save_credentials_to_file(client_id, client_secret)
#
#         REDIRECT_URI = 'http://localhost:8888/callback'
#         scope = 'playlist-read-private user-library-read'
#         sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
#                                                        client_secret=client_secret,
#                                                        redirect_uri=REDIRECT_URI,
#                                                        scope=scope))
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
# # Function to save songs to a CSV file
# def save_songs_to_csv(songs, playlist_name):
#     filename = sanitize_filename(f"{playlist_name}.csv")
#     with open(filename, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(['Song Name', 'Artist Name'])
#         writer.writerows(songs)
#     print(f"Playlist saved to: {filename}")
#
# # Function to download songs from a selected playlist
# def download_songs_from_playlist(sp, playlist_id, playlist_name, download_dir='songs'):
#     songs = fetch_songs_from_playlist(sp, playlist_id)
#     save_songs_to_csv(songs, playlist_name)
#     for song_name, artist_name in songs:
#         download_song(song_name, artist_name, download_dir)
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
#                 if selected_index < 0 or selected_index >= len(playlists):
#                     print("Invalid selection. Please enter a valid playlist number.")
#                     continue
#
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
#             except ValueError:
#                 print("Invalid input. Please enter a valid number.")
#             except Exception as e:
#                 print(f"An error occurred: {e}")
#
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


