import pyfiglet
import time
import os
import webbrowser
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Constants
SETTINGS_FILE = "settings.json"
TUTORIAL_URL = "https://www.example.com/tutorial"  # Replace with your tutorial URL
REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'playlist-modify-public playlist-modify-private user-library-modify user-library-read'


def save_settings(client_id, client_secret):
    """Save Spotify credentials to a JSON file."""
    with open(SETTINGS_FILE, "w") as file:
        json.dump({"client_id": client_id, "client_secret": client_secret}, file)


def load_settings():
    """Load Spotify credentials from a JSON file."""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    return {"client_id": "", "client_secret": ""}


def display_banner():
    """Display the banner."""
    banner = pyfiglet.figlet_format("Likepotify")
    print(banner)


def about():
    """Display information about the program."""
    print("\n--- About ---")
    print("Likepotify: A tool to manage your Spotify liked songs.")
    print("Version: 1.0")
    print("Developed by: Your Name")
    input("\nPress Enter to return to the menu.")


def tutorial():
    """Redirect to the tutorial page."""
    print("Please wait while we are opening the tutorial...")
    time.sleep(2)
    webbrowser.open(TUTORIAL_URL)
    print("\nTutorial opened. Returning to menu...")
    time.sleep(2)


def settings():
    """Prompt for client_id and client_secret and save them."""
    print("\n--- Settings ---")
    client_id = input("Enter your Spotify Client ID: ").strip()
    client_secret = input("Enter your Spotify Client Secret: ").strip()
    save_settings(client_id, client_secret)
    print("\nSettings saved successfully!")
    input("\nPress Enter to return to the menu.")


def reorder_liked_songs_from_playlist(playlist_url, client_id, client_secret):
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
    print(f"Total tracks in playlist: {total_tracks}")

    # Loop through playlist from bottom to top
    for i in range(total_tracks - 1, -1, -1):
        track = all_tracks[i].get('track')  # Safely get 'track' field
        if not track:  # Skip if 'track' is None
            print(f"Skipped invalid track at position {i}")
            continue

        track_id = track.get('id')  # Safely get 'id' field
        track_name = track.get('name', "Unknown Track")  # Default to "Unknown Track" if 'name' is missing

        if not track_id:  # Skip if 'id' is None
            print(f"Skipped track without ID: {track_name}")
            continue

        # Like the song
        sp.current_user_saved_tracks_add([track_id])
        print(f"Liked song: {track_name}")

    print("Reordering complete! Check your liked songs on Spotify.")


def start():
    """Start the Spotify reordering process."""
    settings_data = load_settings()
    client_id = settings_data.get("client_id")
    client_secret = settings_data.get("client_secret")

    if not client_id or not client_secret:
        print("\nSpotify credentials are missing. Please configure them in the Settings menu first.")
        input("\nPress Enter to return to the menu.")
        return

    playlist_url = input("\nEnter the Spotify playlist link: ").strip()
    if not playlist_url:
        print("\nNo playlist link provided. Returning to menu.")
        input("\nPress Enter to return to the menu.")
        return

    print("\nProcessing playlist. This may take a while...")
    reorder_liked_songs_from_playlist(playlist_url, client_id, client_secret)
    input("\nReordering complete! Press Enter to return to the menu.")


def menu():
    """Display the main menu and handle user input."""
    while True:
        display_banner()
        print("1 - Start")
        print("2 - Settings")
        print("3 - About")
        print("4 - Tutorial")
        print("5 - Exit")
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            start()
        elif choice == "2":
            settings()
        elif choice == "3":
            about()
        elif choice == "4":
            tutorial()
        elif choice == "5":
            print("\nExiting... Goodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")
            input("\nPress Enter to return to the menu.")


if __name__ == "__main__":
    # Load settings at the start of the program
    settings_data = load_settings()
    if settings_data["client_id"] and settings_data["client_secret"]:
        print("Settings loaded successfully.")
    else:
        print("No settings found. Please configure your Spotify credentials in the Settings menu.")

    # Start the menu
    menu()