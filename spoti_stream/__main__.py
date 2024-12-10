# spoti_stream/__main__.py

from .spotify_utils import authenticate_spotify, get_user_playlists
from .downloader import download_songs_from_playlist, download_songs_from_csv, download_songs_from_txt, download_song


def main():
    print("\n[INFO] Welcome to SpotiStream! ")
    print("Download and listen to non-stop Spotify music with our tool.")
    print("Music is an art which reaches your soul to pacify it..... :)")
    print("For more information visit: https://github.com/mehmoodulhaq570/SpotiStream")
    print("=---------------------------------=")

    while True:
        print("\nWhat would you like to do?")
        print("1. Use a Spotify playlist")
        print("2. Provide your own CSV or TXT file")
        print("3. Manually type in song names")
        print("4. Exit from SpotiStream")

        choice = input("Please enter 1, 2, 3 or 4: ").strip()

        if choice == '1':
            # Authenticate Spotify credentials only when option 1 is selected
            sp = authenticate_spotify()

            playlists = get_user_playlists(sp)

            # Debugging: Print the raw playlists data

            if playlists:
                print("Your Playlists:")
                for i, playlist in enumerate(playlists):
                    # Validate playlist data
                    if playlist and 'name' in playlist and 'id' in playlist:
                        print(f"{i + 1}. {playlist['name']} (ID: {playlist['id']})")
                    else:
                        print(f"{i + 1}. [Invalid Playlist Data]")
            else:
                print("No playlists found or an error occurred.")

            try:
                selected_index = int(input("Select a playlist by number: ")) - 1
                if selected_index < 0 or selected_index >= len(playlists):
                    print("Invalid selection. Please enter a valid playlist number.")
                    continue

                selected_playlist = playlists[selected_index]
                selected_playlist_id = selected_playlist['id']
                selected_playlist_name = selected_playlist['name']

                download_songs_from_playlist(sp, selected_playlist_id, selected_playlist_name)

            except ValueError:
                print("Invalid input. Please enter a valid number.")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == '2':
            file_path = input("Enter the full path to your CSV or TXT file: ").strip()

            if file_path.lower().endswith('.csv'):
                download_songs_from_csv(file_path)
            elif file_path.lower().endswith('.txt'):
                download_songs_from_txt(file_path)
            else:
                print("Invalid file format. Please provide a .csv or .txt file.")

        elif choice == '3':
            while True:
                song_name = input("Enter the song name (or 'q' to stop): ").strip()
                if song_name.lower() == 'q':
                    break
                artist_name = input(f"Enter the artist name for '{song_name}': ").strip()
                download_song(song_name, artist_name)

        elif choice == '4':
            print("\n    *-------------------------------*    ")
            print("Thank you for using SpotiStream Music! Goodbye!")
            print("    *-------------------------------*    ")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3 or 4.")

        if input("Do you want to continue? (y/n): ").strip().lower() != 'y':
            print("\n    *-------------------------------*    ")
            print("Thank you for using SpotiStream Music! Goodbye!")
            print("    *-------------------------------*    ")
            break


if __name__ == '__main__':
    main()
