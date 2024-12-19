import main


def settings():
    """Prompt for client_id and client_secret and save them."""
    print("\n--- Settings ---")
    client_id = input("Enter your Spotify Client ID: ").strip()
    client_secret = input("Enter your Spotify Client Secret: ").strip()
    main.save_settings(client_id, client_secret)
    print("\nSettings saved successfully!")
    input("\nPress Enter to return to the menu.")