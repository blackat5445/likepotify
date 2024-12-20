import csv
import os
import time
from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import src.utils

# Constants
REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'playlist-modify-public playlist-modify-private user-library-modify user-library-read'

def export_to_text_file(client_id, client_secret):
    """Export liked songs or a playlist to a text file."""
    src.utils.screen_clear()
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
        print("Returning to the menu.")
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


    write_to_file("liked songs", "Liked Songs", liked_tracks, total_songs)

def export_playlist(sp, playlist_url):
    """Export a playlist to a text file with support for pagination."""
    try:
        # Extract playlist ID from URL
        playlist_id = playlist_url.split("/")[-1].split("?")[0]

        # Fetch playlist details
        print("Fetching playlist details...")
        playlist = sp.playlist(playlist_id)
        playlist_name = playlist.get('name', 'Playlist')

        # Pagination: fetch all tracks
        offset = 0
        limit = 100
        total_songs = 0
        formatted_tracks = []

        while True:
            results = sp.playlist_items(playlist_id, offset=offset, limit=limit, fields="items.track,total")
            tracks = results.get('items', [])
            total_songs += len(tracks)

            for item in tracks:
                try:
                    track = item.get('track')
                    if track:
                        formatted_tracks.append(format_track_info(track))
                except Exception as e:
                    print(f"Error formatting track info: {e}")

            # Break the loop if there are no more items to fetch
            if len(tracks) < limit:
                break

            offset += limit  # Move to the next page

        # Write all tracks to the file
        write_to_file("playlist", playlist_name, formatted_tracks, total_songs)
    except Exception as e:
        print(f"Error fetching playlist: {e}")
        time.sleep(2)

def format_track_info(track):
    """Format track information for the text file and CSV file."""
    try:
        track_id = track.get('id', 'N/A')
        track_name = track.get('name', 'Unknown Title')
        track_artists = ", ".join([artist.get('name', 'Unknown Artist') for artist in track.get('artists', [])])
        track_duration = time.strftime('%M:%S', time.gmtime(track.get('duration_ms', 0) / 1000))
        track_url = track.get('external_urls', {}).get('spotify', 'N/A')
        return {
            "id": track_id,
            "title": track_name,
            "artists": track_artists,
            "duration": track_duration,
            "url": track_url,
        }
    except Exception as e:
        print(f"Error extracting track info: {e}")
        return {
            "id": "Error",
            "title": "Error",
            "artists": "Error",
            "duration": "Error",
            "url": "Error",
        }

def write_to_file(file_prefix, title, tracks, total_songs):
    """Write the formatted track list to both a text file and a CSV file."""
    try:
        # Generate the output file paths
        maindir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(maindir, 'Exported Playlists')
        os.makedirs(output_dir, exist_ok=True)

        # File paths
        txt_filename = os.path.join(output_dir, f"{file_prefix}.txt")
        csv_filename = os.path.join(output_dir, f"{file_prefix}.csv")

        # Write to the text file
        with open(txt_filename, "w", encoding="utf-8") as txt_file:
            txt_file.write("#Likepotify\n")
            txt_file.write("#Created by Kasra Falahati\n")
            txt_file.write(f"#Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            txt_file.write(f"#{title}\n")
            txt_file.write(f"#Total number of songs: {total_songs} songs\n")
            txt_file.write("#" * 30 + "\n")
            txt_file.write("ID | TITLE | NAME OF SINGER(S) | TIME | LINK\n")
            for track in tracks:
                txt_file.write(f"{track['id']} | {track['title']} | {track['artists']} | {track['duration']} | {track['url']}\n")

        # Write to the CSV file
        with open(csv_filename, "w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file)

            # Write headers
            writer.writerow(["ID", "TITLE", "NAME OF SINGER(S)", "TIME", "LINK"])

            # Write track data
            for track in tracks:
                writer.writerow([track['id'], track['title'], track['artists'], track['duration'], track['url']])

        print(f"Export complete! Files saved as:\n- {txt_filename}\n- {csv_filename}")

    except Exception as e:
        print(f"Error writing to file: {e}")
