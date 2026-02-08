import csv
import os
import time
from datetime import datetime
from colorama import Fore
from .utils import screen_clear, get_spotify_client, extract_playlist_id, BASE_DIR


def export_to_text_file(client_id, client_secret):
    """Export liked songs or a playlist to text + CSV files."""
    screen_clear()
    sp = get_spotify_client(client_id, client_secret)

    print("Would you like to export:")
    print("  1 - Liked Songs")
    print("  2 - A Playlist")
    print("  3 - Back to Operation Menu")
    choice = input("\nEnter your choice (1/2/3): ").strip()

    if choice == "1":
        export_liked_songs(sp)
    elif choice == "2":
        playlist_url = input("Enter the Spotify playlist URL: ").strip()
        if playlist_url:
            export_playlist(sp, playlist_url)
        else:
            print(Fore.RED + "No URL provided.")
    elif choice == "3":
        return
    else:
        print(Fore.RED + "Invalid choice.")


def export_liked_songs(sp):
    """Export all liked songs."""
    liked_tracks = []
    offset = 0
    limit = 50

    print(Fore.CYAN + "Fetching liked songs...")
    while True:
        try:
            results = sp.current_user_saved_tracks(limit=limit, offset=offset)
            items = results.get("items", [])
            if not items:
                break
            for item in items:
                track = item.get("track")
                if track:
                    liked_tracks.append(_format_track(track))
            print(f"  Fetched {len(liked_tracks)} songs so far...")
            offset += limit
        except Exception as e:
            print(Fore.RED + f"  Error fetching songs: {e}")
            time.sleep(2)
            break

    _write_files("liked_songs", "Liked Songs", liked_tracks)


def export_playlist(sp, playlist_url):
    """Export a playlist to text + CSV."""
    try:
        playlist_id = extract_playlist_id(playlist_url)
        playlist = sp.playlist(playlist_id)
        playlist_name = playlist.get("name", "Playlist")

        tracks = []
        offset = 0
        limit = 100

        print(Fore.CYAN + f"Fetching playlist '{playlist_name}'...")
        while True:
            results = sp.playlist_items(
                playlist_id, offset=offset, limit=limit,
                fields="items.track,total",
            )
            items = results.get("items", [])
            if not items:
                break
            for item in items:
                track = item.get("track")
                if track:
                    tracks.append(_format_track(track))
            offset += limit

        _write_files(playlist_name, playlist_name, tracks)

    except Exception as e:
        print(Fore.RED + f"Error exporting playlist: {e}")
        time.sleep(2)


# ── Private helpers ───────────────────────────────────────────────────────────

def _format_track(track: dict) -> dict:
    """Return a clean dict with the fields we want to export."""
    duration_sec = track.get("duration_ms", 0) / 1000
    return {
        "id": track.get("id", "N/A"),
        "title": track.get("name", "Unknown Title"),
        "artists": ", ".join(a.get("name", "Unknown") for a in track.get("artists", [])),
        "duration": time.strftime("%M:%S", time.gmtime(duration_sec)),
        "url": track.get("external_urls", {}).get("spotify", "N/A"),
    }


def _write_files(file_prefix: str, title: str, tracks: list[dict]):
    """Write tracks to both a .txt and .csv file."""
    output_dir = os.path.join(BASE_DIR, "Exported Playlists")
    os.makedirs(output_dir, exist_ok=True)

    # Sanitise filename
    safe_prefix = "".join(c if c.isalnum() or c in " _-" else "_" for c in file_prefix)
    txt_path = os.path.join(output_dir, f"{safe_prefix}.txt")
    csv_path = os.path.join(output_dir, f"{safe_prefix}.csv")

    # ── TXT ──
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("#Likepotify\n")
        f.write("#Created by Kasra Falahati\n")
        f.write(f"#Date: {datetime.now():%Y-%m-%d %H:%M:%S}\n")
        f.write(f"#{title}\n")
        f.write(f"#Total songs: {len(tracks)}\n")
        f.write("#" * 30 + "\n")
        f.write("ID | TITLE | ARTIST(S) | DURATION | LINK\n")
        for t in tracks:
            f.write(f"{t['id']} | {t['title']} | {t['artists']} | {t['duration']} | {t['url']}\n")

    # ── CSV ──
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "TITLE", "ARTIST(S)", "DURATION", "LINK"])
        for t in tracks:
            writer.writerow([t["id"], t["title"], t["artists"], t["duration"], t["url"]])

    print(Fore.GREEN + f"\nExported {len(tracks)} songs!")
    print(f"  TXT: {txt_path}")
    print(f"  CSV: {csv_path}")
    input("\nPress Enter to continue.")
    screen_clear()
