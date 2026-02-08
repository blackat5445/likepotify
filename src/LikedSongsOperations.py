import time
import spotipy
from colorama import Fore
from .utils import screen_clear, get_spotify_client, retry_request, extract_playlist_id


def get_all_liked_songs(sp):
    """Fetch all currently liked songs and return their IDs as a set."""
    liked_tracks = set()
    offset = 0
    limit = 50

    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        items = results.get("items", [])
        if not items:
            break
        for item in items:
            track = item.get("track")
            if track and track.get("id"):
                liked_tracks.add(track["id"])
        offset += limit

    return liked_tracks


def reorder_liked_songs_from_playlist(playlist_url, client_id, client_secret, reorder_direction="bottom-to-top"):
    """Like every song from the given playlist (preserving order)."""
    sp = get_spotify_client(client_id, client_secret)

    playlist_id = extract_playlist_id(playlist_url)

    # Fetch all currently liked songs so we can skip duplicates
    print(Fore.CYAN + "Fetching your liked songs to detect duplicates...")
    liked_songs = get_all_liked_songs(sp)
    print(f"  Found {len(liked_songs)} already-liked songs.")

    # Fetch all tracks in the playlist (paginated)
    offset = 0
    limit = 100
    all_tracks = []

    while True:
        results = sp.playlist_items(
            playlist_id, offset=offset, limit=limit,
            fields="items.track.id,items.track.name,total",
        )
        items = results.get("items", [])
        if not items:
            break
        all_tracks.extend(items)
        offset += limit

    total_tracks = len(all_tracks)
    print(Fore.GREEN + f"Total tracks in playlist: {total_tracks}\n")
    time.sleep(1)

    # Determine iteration order
    if reorder_direction == "bottom-to-top":
        track_range = range(total_tracks - 1, -1, -1)
    else:
        track_range = range(total_tracks)

    liked_count = 0
    skipped_count = 0

    for i in track_range:
        track = all_tracks[i].get("track")
        if not track:
            print(Fore.LIGHTRED_EX + f"  Skipped invalid entry at position {i}")
            continue

        track_id = track.get("id")
        track_name = track.get("name", "Unknown Track")

        if not track_id:
            print(Fore.LIGHTRED_EX + f"  Skipped track without ID: {track_name}")
            continue

        if track_id in liked_songs:
            skipped_count += 1
            continue

        try:
            retry_request(sp.current_user_saved_tracks_add, [track_id], retries=3, delay=10)
            liked_count += 1
            print(Fore.LIGHTGREEN_EX + f"  [{liked_count}] Liked: {track_name}")
        except spotipy.exceptions.SpotifyException as e:
            print(Fore.RED + f"  Error liking '{track_name}': {e}")

    print(Fore.BLUE + f"\nDone! Liked {liked_count} new songs, skipped {skipped_count} already-liked.")
    time.sleep(2)
