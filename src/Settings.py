from colorama import Fore, Style, init, just_fix_windows_console
from .utils import save_settings, load_settings

def settings():
    """Manage Spotify settings and multi-playlist mode."""
    print(Fore.CYAN + "\n--- Settings ---")
    settings_data = load_settings()

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

    print(
        Fore.YELLOW +
        "\nIt's better to use bottom-to-top if you want to maintain the same order.\n"
    )
    reorder_direction = input(
        "Choose reordering direction:\n1 - Bottom-to-Top (default)\n2 - Top-to-Bottom\nEnter your choice (1/2): "
    ).strip()
    reorder_direction = "bottom-to-top" if reorder_direction != "2" else "top-to-bottom"

    save_settings(client_id, client_secret, multi_playlist_mode, reorder_direction)
    print(Fore.GREEN + "\nSettings saved successfully!")
    input("\nPress Enter to return to the menu.")