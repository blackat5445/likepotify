from colorama import Fore
from .utils import save_settings, load_settings, screen_clear, clear_auth_cache


def settings():
    """Manage Spotify settings and multi-playlist mode."""
    print(Fore.CYAN + "\n--- Settings ---\n")
    settings_data = load_settings()

    old_id = settings_data["client_id"]
    old_secret = settings_data["client_secret"]

    if old_id and old_secret:
        print(f"  Client ID:     {old_id[:8]}...{old_id[-4:]}")
        print(f"  Client Secret: {'*' * 12}")
        change = input("\nUpdate credentials? (yes/no): ").strip().lower()
        if change == "yes":
            client_id = input("Enter your Spotify Client ID: ").strip()
            client_secret = input("Enter your Spotify Client Secret: ").strip()
        else:
            client_id = old_id
            client_secret = old_secret
    else:
        client_id = input("Enter your Spotify Client ID: ").strip()
        client_secret = input("Enter your Spotify Client Secret: ").strip()

    # If credentials changed, clear the auth cache so we don't reuse an old token
    if client_id != old_id or client_secret != old_secret:
        clear_auth_cache()
        print(Fore.YELLOW + "  Auth cache cleared (credentials changed).")

    multi_playlist_mode = (
        input("\nEnable multi-playlist mode? (yes/no): ").strip().lower() == "yes"
    )

    print(
        Fore.YELLOW
        + "\nTip: 'bottom-to-top' preserves the original playlist order in your liked songs.\n"
    )
    direction_choice = input(
        "Reordering direction:\n"
        "  1 - Bottom-to-Top (default)\n"
        "  2 - Top-to-Bottom\n"
        "Enter (1/2): "
    ).strip()
    reorder_direction = "top-to-bottom" if direction_choice == "2" else "bottom-to-top"

    save_settings(client_id, client_secret, multi_playlist_mode, reorder_direction)
    print(Fore.GREEN + "\nSettings saved!")
    input("\nPress Enter to return to the menu.")
    screen_clear()
