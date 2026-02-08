import random
import time
import os
import webbrowser

import pyfiglet
from colorama import Fore, init, just_fix_windows_console

import src.Settings as Settings
import src.LikedSongsOperations as LikedSongsOps
import src.ExportPlaylist as ExportPlaylist
from src.LikedSongsToPlaylist import liked_songs_to_playlist
from src.utils import load_settings, screen_clear

just_fix_windows_console()
init(autoreset=True)

# ── Constants ─────────────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLAYLIST_FILE = os.path.join(BASE_DIR, "Import Playlists", "import.txt")
TUTORIAL_URL = "https://github.com/blackat5445/likepotify"

# Optional startup sound (Windows only, silent elsewhere)
STARTUP_SOUND = os.path.join(BASE_DIR, "assets", "sounds", "Startup.wav")


def _play_startup_sound():
    """Play the startup sound if available (Windows only)."""
    try:
        import winsound
        if os.path.exists(STARTUP_SOUND):
            winsound.PlaySound(STARTUP_SOUND, winsound.SND_ASYNC)
    except ImportError:
        pass  # Not on Windows — just skip


# ── UI helpers ────────────────────────────────────────────────────────────────

def display_banner():
    fonts = pyfiglet.FigletFont.getFonts()
    art = pyfiglet.figlet_format("Likepotify", font=random.choice(fonts))
    print(Fore.GREEN + art)


def about():
    print(Fore.LIGHTGREEN_EX + "\n--- About ---")
    print(Fore.LIGHTBLACK_EX + "Likepotify: Transfer playlists to liked songs & more.")
    print(Fore.YELLOW + "Version: 1.1")
    print(Fore.LIGHTRED_EX + "Developed by: KASRA FALAHATI")
    print(Fore.CYAN + "Sponsored by: WWW.AGENZIAMAGMA.IT")
    input("\nPress Enter to return.")
    screen_clear()


def tutorial():
    print(Fore.LIGHTGREEN_EX + "Opening tutorial in your browser...")
    webbrowser.open(TUTORIAL_URL)
    time.sleep(1)
    screen_clear()


# ── Credential check ─────────────────────────────────────────────────────────

def _require_credentials():
    """Return (client_id, client_secret) or None if not configured."""
    data = load_settings()
    cid, csec = data.get("client_id"), data.get("client_secret")
    if not cid or not csec:
        print(Fore.RED + "\nSpotify credentials not configured.")
        print(Fore.YELLOW + "Please set them in the Settings menu first.")
        input("\nPress Enter to return.")
        return None
    return cid, csec


# ── Operations ────────────────────────────────────────────────────────────────

def start_playlist_to_liked():
    """Import a playlist (or multiple) into liked songs."""
    creds = _require_credentials()
    if not creds:
        return
    client_id, client_secret = creds

    data = load_settings()
    multi = data.get("multi_playlist_mode", False)
    direction = data.get("reorder_direction", "bottom-to-top")

    if multi and os.path.exists(PLAYLIST_FILE):
        print(Fore.BLUE + "Multi-playlist mode: processing import file...")
        with open(PLAYLIST_FILE, "r") as f:
            urls = [line.strip() for line in f if line.strip()]
        for url in urls:
            print(Fore.YELLOW + f"\n→ Processing: {url}")
            LikedSongsOps.reorder_liked_songs_from_playlist(url, client_id, client_secret, direction)
    else:
        url = input("\nEnter the Spotify playlist link: ").strip()
        if not url:
            print(Fore.RED + "No link provided.")
            input("\nPress Enter to return.")
            return
        print(Fore.GREEN + "\nProcessing playlist...")
        LikedSongsOps.reorder_liked_songs_from_playlist(url, client_id, client_secret, direction)

    input(Fore.GREEN + "\nDone! Press Enter to return.")
    screen_clear()


def start_export():
    """Export liked songs or a playlist."""
    creds = _require_credentials()
    if not creds:
        return
    try:
        ExportPlaylist.export_to_text_file(*creds)
    except Exception as e:
        print(Fore.RED + f"\nExport error: {e}")
        input("\nPress Enter to return.")


def start_liked_to_playlist():
    """Copy liked songs into a new playlist."""
    creds = _require_credentials()
    if not creds:
        return
    try:
        liked_songs_to_playlist(*creds)
    except Exception as e:
        print(Fore.RED + f"\nError: {e}")
        input("\nPress Enter to return.")


# ── Menus (loop-based, no recursion) ─────────────────────────────────────────

def menu_operations():
    """Operations sub-menu."""
    while True:
        display_banner()
        print("1 - Playlist → Liked Songs")
        print("2 - Export playlist / liked songs to file")
        print("3 - Liked Songs → New Playlist")
        print("4 - Back")
        choice = input("\nEnter your choice: ").strip()

        screen_clear()
        if choice == "1":
            start_playlist_to_liked()
        elif choice == "2":
            start_export()
        elif choice == "3":
            start_liked_to_playlist()
        elif choice == "4":
            return  # back to main menu (no recursion!)
        else:
            print(Fore.RED + "Invalid choice.")
            input("\nPress Enter to try again.")
            screen_clear()


def main_menu():
    """Main menu loop."""
    _play_startup_sound()
    while True:
        display_banner()
        print("1 - Operations")
        print("2 - Settings")
        print("3 - About")
        print("4 - Tutorial")
        print("5 - Exit")
        choice = input("\nEnter your choice: ").strip()

        screen_clear()
        if choice == "1":
            menu_operations()
        elif choice == "2":
            Settings.settings()
        elif choice == "3":
            about()
        elif choice == "4":
            tutorial()
        elif choice == "5":
            print(Fore.GREEN + "\nGoodbye!")
            break
        else:
            print(Fore.RED + "Invalid choice.")
            input("\nPress Enter to try again.")
            screen_clear()


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    data = load_settings()
    if data["client_id"] and data["client_secret"]:
        print(Fore.GREEN + "Settings loaded.")
    else:
        print(Fore.YELLOW + "No credentials found — please configure them in Settings.")
    print()
    main_menu()
