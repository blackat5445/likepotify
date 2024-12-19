from colorama import Fore, Style, init
from .. import main

def settings():
    """Manage Spotify settings and multi-playlist mode."""
    print(Fore.CYAN + "\n--- Settings ---")
    settings_data =  main.py.load_settings()

    if settings_data["client_id"] and settings_data["client_secret"]:
        print("Spotify credentials already exist.")
        change = input("Do you want to update them? (yes/no): ").strip().lower()
        if change != "yes":
            client_id = settings_data["client_id"]
            client_secret = settings_data["client_secret"]
        else:
            client_id = input("Enter your Spotify Client ID: ").strip()
            client_secret = input("Enter your Spotify Client Secret: ").strip()
    else:
        client_id = input("Enter your Spotify Client ID: ").strip()
        client_secret = input("Enter your Spotify Client Secret: ").strip()

    multi_playlist_mode = input("Enable multi-playlist mode? (yes/no): ").strip().lower() == "yes"

    main.py.save_settings(client_id, client_secret, multi_playlist_mode)
    print(Fore.GREEN + "\nSettings saved successfully!")
    input("\nPress Enter to return to the menu.")