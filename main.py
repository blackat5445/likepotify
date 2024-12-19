import random
import pyfiglet
import time
import os
import webbrowser
import json
import winsound
from colorama import Fore, Style, init
import src.Settings
import src.LikedSongsOperations

init()

# Constants
maindir = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(maindir, r'settings.json')
START_SOUND = os.path.join(maindir, r'assets/sounds/start.wav')
PLAYLIST_FILE = os.path.join(maindir, r'playlists/Import Playlists/import.txt')
TUTORIAL_URL = "https://www.example.com/tutorial"  # Replace with your tutorial URL
REORDER_OPERATION = src.LikedSongsOperations
SETTINGS_OPERATION = src.Settings


#helper function to clear CUI
def screen_clear():
    _ = os.system('cls')

def save_settings(client_id, client_secret, multi_playlist_mode):
    """Save Spotify credentials and settings to a JSON file."""
    with open(SETTINGS_FILE, "w") as file:
        json.dump({
            "client_id": client_id,
            "client_secret": client_secret,
            "multi_playlist_mode": multi_playlist_mode
        }, file)


def load_settings():
    """Load Spotify credentials and settings from a JSON file."""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    return {"client_id": "", "client_secret": "", "multi_playlist_mode": False}


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
    print("Developed by: Kasra Falahati")
    input("\nPress Enter to return to the menu.")
    screen_clear()


def tutorial():
    """Redirect to the tutorial page."""
    print("Please wait while we are opening the tutorial...")
    time.sleep(2)
    webbrowser.open(TUTORIAL_URL)
    print("\nTutorial opened. Returning to menu...")
    time.sleep(2)
    screen_clear()



def start():
    """Start the Spotify reordering process."""
    settings_data = load_settings()
    client_id = settings_data.get("client_id")
    client_secret = settings_data.get("client_secret")
    multi_playlist_mode = settings_data.get("multi_playlist_mode", False)

    if not client_id or not client_secret:
        print(Fore.RED + "\nSpotify credentials are missing. Please configure them in the Settings menu first.")
        input("\nPress Enter to return to the menu.")
        return

    if multi_playlist_mode and os.path.exists(PLAYLIST_FILE):
        print(Fore.BLUE + "Processing multiple playlists...")
        with open(PLAYLIST_FILE, "r") as file:
            playlist_urls = [line.strip() for line in file if line.strip()]
            for playlist_url in playlist_urls:
                print(Fore.YELLOW + f"\nProcessing playlist: {playlist_url}")
                REORDER_OPERATION.reorder_liked_songs_from_playlist(playlist_url, client_id, client_secret)
    else:
        playlist_url = input("\nEnter the Spotify playlist link: ").strip()
        if not playlist_url:
            print(Fore.RED + "\nNo playlist link provided. Returning to menu.")
            input("\nPress Enter to return to the menu.")
            return

        print(Fore.GREEN + "\nProcessing playlist. This may take a while...")
        REORDER_OPERATION.reorder_liked_songs_from_playlist(playlist_url, client_id, client_secret)

    input(Fore.GREEN + "\nReordering complete! Press Enter to return to the menu.")
    screen_clear()


def menu():
    winsound.PlaySound(START_SOUND, winsound.SND_ASYNC)
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
            SETTINGS_OPERATION.settings()
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