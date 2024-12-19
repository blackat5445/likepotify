import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from colorama import Fore, Style, init, just_fix_windows_console

# Constants
REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'playlist-modify-public playlist-modify-private user-library-modify user-library-read'

def get_all_liked_songs(sp):
    """Fetch all currently liked songs and return their IDs as a set."""
    liked_tracks = set()
    offset = 0
    limit = 50  # Spotify API limits the number of items fetched per request

    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        items = results.get('items', [])
        for item in items:
            track = item.get('track')
            if track and track.get('id'):
                liked_tracks.add(track['id'])
        if len(items) == 0:  # No more items to fetch
            break
        offset += limit

    return liked_tracks
def retry_request(func, retries=3, delay=5, *args, **kwargs):
    """Retry a function call on failure."""
    for attempt in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt < retries - 1:
                print(f"Request failed: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"Request failed after {retries} attempts: {e}")
                raise

def reorder_liked_songs_from_playlist(playlist_url, client_id, client_secret, reorder_direction="bottom-to-top"):
    """Reorder liked songs from the given playlist URL."""
    # Initialize Spotify client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    ), requests_timeout=30)

    # Extract playlist ID from URL
    playlist_id = playlist_url.split("/")[-1].split("?")[0]

    # Fetch all currently liked songs
    liked_songs = get_all_liked_songs(sp)

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
        # Skip already liked songs
        if track_id in liked_songs:
            print(f"Track already liked: {track_name}")
            continue

        # Like the song
        try:
            retry_request(sp.current_user_saved_tracks_add, retries=3, delay=10, args=[[track_id]])
            print(Fore.LIGHTGREEN_EX + f"Liked song: {track_name}")
        except spotipy.exceptions.SpotifyException as e:
            print(f"Error liking song {track_name}: {e}")

    print(Fore.BLUE +"Reordering complete! Check your liked songs on Spotify.")