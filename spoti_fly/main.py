# spoti_fly/main.py
import os
from .spotify_utils import authenticate_spotify, get_user_playlists, fetch_songs_from_playlist
from .downloader import download_songs_from_playlist, download_songs_from_csv

def main():
    # Welcome message
    print("Welcome to SpotiFly!")
    print("Download and listen to non-stop Spotify music with our tool.")
    print("A piece of music that reaches your soul.... :)")
    print("---------------------------------")

    # Check for existing Spotify credentials
    sp = authenticate_spotify()

    while True:
        print("\nWhat would you like to do?")
        print("1. Use a Spotify playlist")
        print("2. Provide your own CSV file")

        choice = input("Please enter 1 or 2: ").strip()

        if choice == '1':
            playlists = get_user_playlists(sp)

            if playlists:
                print("Your Playlists:")
                for i, playlist in enumerate(playlists):
                    print(f"{i + 1}. {playlist['name']} (ID: {playlist['id']})")
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
            csv_file_path = input("Enter the full path to your CSV file: ").strip()
            download_songs_from_csv(csv_file_path)


        elif choice == '3':
            print("Thank you for using SpotiFly Music! Goodbye!")
            print("--------------------------------------------")
            break

        else:
            print("Invalid choice. Please enter 1, 2 or 3.")

        if input("Do you want to continue? (y/n): ").strip().lower() != 'y':
            print("Thank you for using SpotiFly Music! Goodbye!")
            print("--------------------------------------------")
            break

if __name__ == '__main__':
    main()
