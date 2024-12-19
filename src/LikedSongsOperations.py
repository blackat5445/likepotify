import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from colorama import Fore, Style, init, just_fix_windows_console

# Constants
REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'playlist-modify-public playlist-modify-private user-library-modify user-library-read'

def reorder_liked_songs_from_playlist(playlist_url, client_id, client_secret, reorder_direction="bottom-to-top"):
    """Reorder liked songs from the given playlist URL."""
    # Initialize Spotify client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    ))

    # Extract playlist ID from URL
    playlist_id = playlist_url.split("/")[-1].split("?")[0]

    # Fetch all tracks in the playlist (handle pagination)
    offset = 0
    limit = 100
    all_tracks = []
    while True:
        results = sp.playlist_items(playlist_id, offset=offset, limit=limit, fields="items.track.id,items.track.name,total")
        all_tracks.extend(results['items'])
        offset += limit
        if len(results['items']) == 0:
            break

    total_tracks = len(all_tracks)
    print(Fore.GREEN + f"Total tracks in playlist: {total_tracks}")
    time.sleep(2)
    # Determine iteration order based on direction
    if reorder_direction == "bottom-to-top":
        track_range = range(total_tracks - 1, -1, -1)
    else:
        track_range = range(total_tracks)

    # Loop through tracks in the chosen order
    for i in track_range:
        track = all_tracks[i].get('track')  # Safely get 'track' field
        if not track:  # Skip if 'track' is None
            print(Fore.LIGHTRED_EX + f"Skipped invalid track at position {i}")
            continue

        track_id = track.get('id')  # Safely get 'id' field
        track_name = track.get('name', "Unknown Track")  # Default to "Unknown Track" if 'name' is missing

        if not track_id:  # Skip if 'id' is None
            print(Fore.LIGHTRED_EX + f"Skipped track without ID: {track_name}")
            continue

        # Like the song
        sp.current_user_saved_tracks_add([track_id])
        print(Fore.LIGHTGREEN_EX + f"Liked song: {track_name}")

    print(Fore.BLUE +"Reordering complete! Check your liked songs on Spotify.")