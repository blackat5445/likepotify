import random
import pyfiglet
from colorama import Fore
import time
import os
import webbrowser
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import src.Settings
from src import *

# Constants
SETTINGS_FILE = "settings.json"
TUTORIAL_URL = "https://www.example.com/tutorial"  # Replace with your tutorial URL
REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'playlist-modify-public playlist-modify-private user-library-modify user-library-read'

#helper function to clear CUI
def screen_clear():
    _ = os.system('cls')

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
    """Display the banner with thick and random art."""
    fonts = pyfiglet.FigletFont.getFonts()  # Get a list of all available fonts
    random_font = random.choice(fonts)  # Choose a random font
    art = pyfiglet.figlet_format("Likepotify", font=random_font)  # Generate art with the random font
    print(Fore.GREEN + art + Fore.RESET)


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
    src.LikedSongsOperations.py.reorder_liked_songs_from_playlist(playlist_url, client_id, client_secret)
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
            src.Settings.settings()
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