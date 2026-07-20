import json
import os
import sys
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ── Path helpers ──────────────────────────────────────────────────────────────

def get_base_path():
    """Return the project root directory (works with PyInstaller too)."""
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    # Go up one level from src/ to project root
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


BASE_DIR = get_base_path()
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
CACHE_FILE = os.path.join(BASE_DIR, ".cache")

# ── Spotify constants ─────────────────────────────────────────────────────────

REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPES = (
    "playlist-modify-public "
    "playlist-modify-private "
    "playlist-read-private "
    "playlist-read-collaborative "
    "user-library-modify "
    "user-library-read"
)

# ── Settings I/O ──────────────────────────────────────────────────────────────

_DEFAULT_SETTINGS = {
    "client_id": "",
    "client_secret": "",
    "multi_playlist_mode": False,
    "reorder_direction": "bottom-to-top",
}


def load_settings() -> dict:
    """Load settings from disk, returning defaults for missing keys."""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {**_DEFAULT_SETTINGS, **data}
    return dict(_DEFAULT_SETTINGS)


def save_settings(client_id, client_secret, multi_playlist_mode=False, reorder_direction="bottom-to-top"):
    """Persist settings to disk."""
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "client_id": client_id,
            "client_secret": client_secret,
            "multi_playlist_mode": multi_playlist_mode,
            "reorder_direction": reorder_direction,
        }, f, indent=2)


# ── Spotify authentication (single source of truth) ──────────────────────────

def get_spotify_client(client_id: str, client_secret: str) -> spotipy.Spotify:
    """
    Return an authenticated Spotify client.

    Uses a single shared cache file and auto-refreshes tokens.
    If the cache is corrupt or the credentials changed, the old
    cache is deleted so a fresh auth flow can start.
    """
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=REDIRECT_URI,
        scope=SCOPES,
        cache_path=CACHE_FILE,
        open_browser=True,
    )

    # If there's a cached token, try to validate / refresh it
    token_info = auth_manager.cache_handler.get_cached_token()
    if token_info:
        cached_scopes = set((token_info.get("scope") or "").split())
        required_scopes = set(SCOPES.split())
        if not required_scopes.issubset(cached_scopes):
            # Cached token predates a scope change – nuke it so a fresh
            # browser auth (with the current scopes) runs below.
            _delete_cache()
            token_info = None
        elif auth_manager.is_token_expired(token_info):
            try:
                token_info = auth_manager.refresh_access_token(token_info["refresh_token"])
            except Exception:
                # Refresh failed – nuke cache so a fresh browser auth starts
                _delete_cache()
                token_info = None

    if not token_info:
        # Opens the browser for the user to authorize
        token_info = auth_manager.get_access_token(as_dict=True)

    # retries=0 disables spotipy's built-in urllib3 retry, which otherwise
    # blocks for however long Spotify's Retry-After header says (can be
    # many hours on a 429) before even raising. We handle retries/backoff
    # ourselves in retry_request() instead.
    return spotipy.Spotify(auth_manager=auth_manager, requests_timeout=30, retries=0, status_retries=0)


def clear_auth_cache():
    """Delete the cached token (useful when credentials change)."""
    _delete_cache()


def _delete_cache():
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)


# ── Helpers ───────────────────────────────────────────────────────────────────

def screen_clear():
    """Clear the terminal screen (cross-platform)."""
    os.system("cls" if os.name == "nt" else "clear")


MAX_RATE_LIMIT_WAIT = 60  # seconds – beyond this we give up instead of blocking


def retry_request(func, *args, retries=3, delay=5, **kwargs):
    """Call *func(*args, **kwargs)* with automatic retries on failure.

    A 429 (rate limit) is handled specially: short Spotify-requested
    cooldowns are honored, but if Spotify asks for a long wait (this can be
    hours) we stop immediately with a clear message instead of blocking.
    """
    for attempt in range(retries):
        try:
            return func(*args, **kwargs)
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 429:
                retry_after = int((e.headers or {}).get("Retry-After", delay))
                if retry_after > MAX_RATE_LIMIT_WAIT:
                    print(
                        f"  Spotify rate limit hit — it wants a {retry_after}s "
                        f"(~{retry_after / 3600:.1f}h) cooldown. That's too long to "
                        "wait here, so stopping. Please try again later."
                    )
                    raise
                print(f"  Rate limited by Spotify. Waiting {retry_after}s before retrying...")
                time.sleep(retry_after)
                continue
            if attempt < retries - 1:
                print(f"  Warning: Request failed: {e}. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                print(f"  Error: Request failed after {retries} attempts: {e}")
                raise
        except Exception as e:
            if attempt < retries - 1:
                print(f"  Warning: Request failed: {e}. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                print(f"  Error: Request failed after {retries} attempts: {e}")
                raise


def extract_playlist_id(url_or_id: str) -> str:
    """Extract a Spotify playlist ID from a URL or return the raw ID."""
    return url_or_id.split("/")[-1].split("?")[0]
