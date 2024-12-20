import os
import time
from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import main

# Constants
REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'playlist-modify-public playlist-modify-private user-library-modify user-library-read'

def export_to_text_file(client_id, client_secret):
    """Export liked songs or a playlist to a text file."""
    main.screen_clear()
    # Initialize Spotify client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    ))

    # Ask user whether to export liked songs or a playlist
    print("Would you like to export:\n1 - Liked Songs\n2 - Playlist\n3 - Back to Operation Menu")
    choice = input("Enter your choice (1/2/3): ").strip()

    if choice == "1":
        # Export liked songs
        export_liked_songs(sp)
    elif choice == "2":
        # Export a playlist
        playlist_url = input("Enter the Spotify playlist URL: ").strip()
        export_playlist(sp, playlist_url)
    elif choice == "3":
        main.menu_operations()
    else:
        print("Invalid choice. Returning to the menu.")

def export_liked_songs(sp):
    """Export liked songs to a text file."""
    liked_tracks = []
    offset = 0
    limit = 50
    total_songs = 0

    print("Fetching liked songs...")
    while True:
        try:
            results = sp.current_user_saved_tracks(limit=limit, offset=offset)
            items = results.get('items', [])
            for item in items:
                track = item.get('track')
                if track:
                    try:
                        liked_tracks.append(format_track_info(track))
                    except Exception as e:
                        print(f"Error formatting track info: {e}")
            total_songs += len(items)
            if len(items) == 0:
                break
            offset += limit
        except Exception as e:
            print(f"Error fetching liked songs: {e}")
            time.sleep(2)
            main.menu()


    write_to_file("liked songs", "Liked Songs", liked_tracks, total_songs)

def export_playlist(sp, playlist_url):
    """Export a playlist to a text file."""
    try:
        # Extract playlist ID from URL
        playlist_id = playlist_url.split("/")[-1].split("?")[0]

        # Fetch playlist details
        print("Fetching playlist details...")
        playlist = sp.playlist(playlist_id)
        playlist_name = playlist.get('name', 'Playlist')
        tracks = playlist.get('tracks', {}).get('items', [])
        total_songs = len(tracks)

        formatted_tracks = []
        for item in tracks:
            try:
                track = item.get('track')
                if track:
                    formatted_tracks.append(format_track_info(track))
            except Exception as e:
                print(f"Error formatting track info: {e}")

        write_to_file("playlist", playlist_name, formatted_tracks, total_songs)
    except Exception as e:
        print(f"Error fetching playlist: {e}")
        time.sleep(2)
        main.menu()

def format_track_info(track):
    """Format track information for the text file."""
    try:
        track_id = track.get('id', 'N/A')
        track_name = track.get('name', 'Unknown Title')
        track_artists = ", ".join([artist.get('name', 'Unknown Artist') for artist in track.get('artists', [])])
        track_duration = time.strftime('%M:%S', time.gmtime(track.get('duration_ms', 0) / 1000))
        track_url = track.get('external_urls', {}).get('spotify', 'N/A')
        return f"{track_id} | {track_name} by {track_artists} | Duration: {track_duration} | {track_url}"
    except Exception as e:
        print(f"Error extracting track info: {e}")
        return "Error extracting track info"

def write_to_file(file_prefix, title, tracks, total_songs):
    """Write the formatted track list to a text file."""
    # Generate the output file path
    try:
        maindir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(maindir, 'Exported Playlists/')
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, f"{file_prefix}.txt")

        # Write to the file
        with open(filename, "w", encoding="utf-8") as file:
            file.write("#Likepotify\n")
            file.write("#Created by Kasra Falahati\n")
            file.write(f"#Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"#{title}\n")
            file.write(f"#Total number of songs: {total_songs} songs\n")
            file.write("#" * 30 + "\n")
            file.write("ID | TITLE | NAME OF SONG by NAME OF SINGER(S) | DURATION | LINK \n")
            file.write("")
            for track in tracks:
                file.write(track + "\n")

        print(f"Export complete! File saved as {filename}")
    except Exception as e:
        print(f"Error writing to file: {e}")
        time.sleep(2)
        main.menu()
