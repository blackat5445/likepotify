import json
import os

# Constants
SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../settings.json')

def save_settings(client_id, client_secret, multi_playlist_mode=False, reorder_direction="bottom-to-top"):
    """Save Spotify credentials and settings to a JSON file."""
    with open(SETTINGS_FILE, "w") as file:
        json.dump({
            "client_id": client_id,
            "client_secret": client_secret,
            "multi_playlist_mode": multi_playlist_mode,
            "reorder_direction": reorder_direction
        }, file)

def load_settings():
    """Load Spotify credentials and settings from a JSON file."""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    return {"client_id": "", "client_secret": "", "multi_playlist_mode": False, "reorder_direction": "bottom-to-top"}