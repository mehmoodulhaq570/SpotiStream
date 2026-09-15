# spoti_stream/__main__.py

import sys

def ask_video_quality():
    print("\nChoose video quality:")
    print("1. Best available / HD")
    print("2. 4K")
    print("3. 1440p")
    print("4. 1080p")
    print("5. 720p")
    print("6. 480p")
    print("7. 360p")
    quality = input("Please enter 1, 2, 3, 4, 5, 6 or 7: ").strip()
    if quality not in ('1', '2', '3', '4', '5', '6', '7'):
        print("Invalid quality. Using 720p.")
        return '720'
    return quality


def print_cli_help():
    print("Usage: spotistream [COMMAND]")
    print("\nCommands:")
    print("  doctor    Check Python, yt-dlp, FFmpeg, Deno, and Spotify setup")
    print("  help      Show this help message")
    print("\nRun without a command to open the interactive menu.")


def main(args=None):
    args = list(sys.argv[1:] if args is None else args)
    if args:
        command = args[0].lower()
        if command == 'doctor' and len(args) == 1:
            from .diagnostics import run_doctor
            return run_doctor()
        if command in ('help', '-h', '--help') and len(args) == 1:
            print_cli_help()
            return 0
        print(f"Unknown command: {' '.join(args)}\n")
        print_cli_help()
        return 2

    from .spotify_utils import authenticate_spotify, get_user_playlists
    from .downloader import (
        download_song,
        download_songs_from_csv,
        download_songs_from_playlist,
        download_songs_from_txt,
        download_songs_from_youtube_playlist,
        download_video_by_song,
        download_videos_from_youtube_playlist,
    )

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
        print("4. Download audio from YouTube input")
        print("5. Download a video by song name")
        print("6. Download videos from YouTube input")
        print("7. Exit from SpotiStream")

        choice = input("Please enter 1, 2, 3, 4, 5, 6 or 7: ").strip()

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
            youtube_input = input("Enter a YouTube URL, playlist, channel, or search query: ").strip()
            download_songs_from_youtube_playlist(youtube_input)

        elif choice == '5':
            song_name = input("Enter the song name: ").strip()
            artist_name = input(f"Enter the artist name for '{song_name}': ").strip()
            quality = ask_video_quality()
            download_video_by_song(song_name, artist_name, quality)

        elif choice == '6':
            youtube_input = input("Enter a YouTube URL, playlist, channel, or search query: ").strip()
            quality = ask_video_quality()
            download_videos_from_youtube_playlist(youtube_input, quality)

        elif choice == '7':
            print("\n    *-------------------------------*    ")
            print("Thank you for using SpotiStream Music! Goodbye!")
            print("    *-------------------------------*    ")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6 or 7.")

        if input("Do you want to continue? (y/n): ").strip().lower() != 'y':
            print("\n    *-------------------------------*    ")
            print("Thank you for using SpotiStream Music! Goodbye!")
            print("    *-------------------------------*    ")
            break

    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\n\nSpotiStream package has stopped.")
