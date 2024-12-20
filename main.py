import random
import pyfiglet
import time
import os
import webbrowser
import json
import winsound
from colorama import Fore, Style, init, just_fix_windows_console
import src.Settings
import src.LikedSongsOperations
import src.utils
import src.ExportPlaylist
just_fix_windows_console()
init(autoreset=True)

# Constants
maindir = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(maindir, r'settings.json')
START_SOUND = os.path.join(maindir, r'assets\sounds\start.wav')
PLAYLIST_FILE = os.path.join(maindir, r'Import Playlists\import.txt')
PLAYLIST_FILE_EXPORT = os.path.join(maindir, r'Exported Playlists')
TUTORIAL_URL = "https://www.example.com/tutorial"  # Replace with your tutorial URL
REORDER_OPERATION = src.LikedSongsOperations
EXPORT_OPERATION = src.ExportPlaylist
SETTINGS_OPERATION = src.Settings
UTILITY = src.utils


#helper function to clear CUI

def display_banner():
    """Display the banner with thick and random art."""
    fonts = pyfiglet.FigletFont.getFonts()  # Get a list of all available fonts
    random_font = random.choice(fonts)  # Choose a random font
    art = pyfiglet.figlet_format("Likepotify", font=random_font)  # Generate art with the random font
    print(Fore.GREEN + art + Fore.RESET)


def about():
    """Display information about the program."""
    print(Fore.LIGHTGREEN_EX + "\n--- About ---")
    print(Fore.LIGHTBLACK_EX + "Likepotify: A tool to transfer your play list to liked songs.")
    print(Fore.YELLOW + "Version: 1.0")
    print(Fore.LIGHTRED_EX + "Developed by: KASRA FALAHATI")
    print(Fore.CYAN + "Sponsored by: WWW.AGENZIAMAGMA.IT")
    input("\nPress Enter to return to the menu.")
    UTILITY.screen_clear()


def tutorial():
    """Redirect to the tutorial page."""
    print(Fore.LIGHTGREEN_EX + "Please wait while we are opening the tutorial...")
    time.sleep(2)
    webbrowser.open(TUTORIAL_URL)
    print("\nTutorial opened. Returning to menu...")
    time.sleep(2)
    UTILITY.screen_clear()



def start_playlist_to_liked():
    """Start the Spotify reordering process."""
    settings_data = UTILITY.load_settings()
    client_id = settings_data.get("client_id")
    client_secret = settings_data.get("client_secret")
    multi_playlist_mode = settings_data.get("multi_playlist_mode", False)
    reorder_direction = settings_data.get("reorder_direction", "bottom-to-top")

    if not client_id or not client_secret:
        print(Fore.RED + "\nSpotify credentials are missing. Please configure them in the Settings menu first.")
        print(Fore.YELLOW + "\nIf you need to import more than 1 playlist you can fill the Import Playlists/imports.txt")
        input("\nPress Enter to return to the menu.")
        return

    if multi_playlist_mode and os.path.exists(PLAYLIST_FILE):
        print(Fore.BLUE + "Processing multiple playlists...")
        with open(PLAYLIST_FILE, "r") as file:
            playlist_urls = [line.strip() for line in file if line.strip()]
            for playlist_url in playlist_urls:
                print(Fore.YELLOW + f"\nProcessing playlist: {playlist_url}")
                REORDER_OPERATION.reorder_liked_songs_from_playlist(playlist_url, client_id, client_secret, reorder_direction)
    else:
        playlist_url = input("\nEnter the Spotify playlist link: ").strip()
        if not playlist_url:
            print(Fore.RED + "\nNo playlist link provided. Returning to menu.")
            input("\nPress Enter to return to the menu.")
            return

        print(Fore.GREEN + "\nProcessing playlist. This may take a while...")
        REORDER_OPERATION.reorder_liked_songs_from_playlist(playlist_url, client_id, client_secret, reorder_direction)

    input(Fore.GREEN + "\nReordering complete! Press Enter to return to the menu.")
    UTILITY.screen_clear()
    menu()


def menu():
    winsound.PlaySound(START_SOUND, winsound.SND_ASYNC)
    """Display the main menu and handle user input."""
    while True:
        display_banner()
        print("1 - Operations")
        print("2 - Settings")
        print("3 - About")
        print("4 - Tutorial")
        print("5 - Exit")
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            menu_operations()
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

def menu_operations():
    """Display the operation menu."""
    while True:
        display_banner()
        print("1 - Playlists to liked songs")
        print("2 - Export playlist or liked songs to text file")
        print("3 - Liked songs to play list")
        print("4 - Back to main menu.")
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            start_playlist_to_liked()
        elif choice == "2":
            # Load settings
            settings_datas = UTILITY.load_settings()
            client_id = settings_datas.get("client_id")
            client_secret = settings_datas.get("client_secret")

            # Check if credentials are available
            if not client_id or not client_secret:
                print("\nSpotify credentials not found. Please configure them in the Settings menu first.")
                input("\nPress Enter to return to the menu.")
            else:
                # Proceed with export operation
                try:
                    EXPORT_OPERATION.export_to_text_file(client_id, client_secret)
                except Exception as e:
                    print(f"\nAn error occurred during export: {e}")
                    input("\nPress Enter to return to the menu.")
        elif choice == "3":
            about()
        elif choice == "4":
            menu()
        else:
            print("\nInvalid choice. Please try again.")
            input("\nPress Enter to return to the menu.")

if __name__ == "__main__":
    # Load settings at the start of the program
    settings_data =  UTILITY.load_settings()
    if settings_data["client_id"] and settings_data["client_secret"]:
        print(Fore.GREEN + "Settings loaded successfully.")
    else:
        print(Fore.RED + "No settings found. Please configure your Spotify credentials in the Settings menu.")

    # Start the menu
    menu()