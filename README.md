
# LIKEPOTIFY 🎶💚

Likepotify is a handy script that allows you to manage your Spotify playlists and liked songs effortlessly. With this mini script, you can:

- Add a playlist to your Spotify liked songs in the correct order.
- Export your playlists or liked songs into CSV and TXT formats.
- Create a Spotify playlist from your liked songs.


## Features ✨

**Playlists to Liked Songs**
 - Add all the tracks from a Spotify playlist to your liked songs in the order they appear in the playlist.

**Export Playlists and Liked Songs**

Export any Spotify playlist or your liked songs to a CSV or TXT file. The exported data includes:

- Song ID
- Title
- Artist(s)
- Duration
- Spotify Link
**Liked Songs to Playlist** 

- Automatically create a Spotify playlist from all your liked songs and add them in one click.


## Installation 🛠️

**Prerequisites**
- Python 3.9 or later
- A Spotify Developer account to generate Client ID and Client Secret (Same account that you are going to manage the playlist / liked songs).

Create your Spotify app [here](https://www.developer.spotify.com/).

**Clone the Repository**

```bash
git clone https://github.com/yourusername/likepotify.git
cd likepotify
```
**Libraries**

Install the required libraries using `pip`:

```bash
pip install -r requirements.txt
```
    
## Usage 🚀

**Run the Script**
```bash
python main.py
```
Now simply use in menu items to navigate. (1-5 depends on the menu)

## Tutorials 📚
You must already create a developer account associated with your spotify account.

Go to you developer account.

Go to your dashboard.

Click on **Create app**.
- App name: anything you like.
- App description: anything you like.
- **Redirect URIs: http://localhost:8080**

Check the check box and click on Save.

Click on your created app.

In top right click on settings and the basic information.

Write down Client ID and Client Secret.

Now open up the script.

Enter "2" and go to settings.

Enter your Client ID.

Enter your Client Secret.

Enable multi-playlist mode? (yes/no)

In this part if you have a unique play list click on no, if you have more than 1 play list enter yes.

- if you enabled multi play list go to Import playlists DIR and enter your playlist links like:
```
https://open.spotify.com/playlist/this-is-an-example1
https://open.spotify.com/playlist/this-is-an-example2
https://open.spotify.com/playlist/this-is-an-example3
https://open.spotify.com/playlist/this-is-an-example4
https://open.spotify.com/playlist/this-is-an-example5
```
Now Choose reordering direction:

- 1 - Bottom-to-Top (default)
- 2 - Top-to-Bottom

It's better to use bottom-to-top if you want to maintain the same order.

**now we are ready!**

Enter "1" for Operation menu.

**Playlists to Liked Songs**

- Add tracks from a Spotify playlist to your liked songs:

Select option 1 in the main menu.

Provide the playlist link.

Enjoy your tracks added to your liked songs in order.

**Export Playlists or Liked Songs**
- Export playlists or liked songs to CSV or TXT files:
Select option 2 in the main menu.

Choose to export liked songs or a specific playlist.

Find your exported files in the Exported Playlists/ directory.

**Liked Songs to Playlist**

- Create a playlist from your liked songs:
Select option 3 in the main menu.

The script will fetch your liked songs and add them to the playlist.
## File Structure 📁

```
likepotify/
│
├── main.py                     # Entry point of the script
├── src/
│   ├── Settings.py             # Settings management
│   ├── ExportPlaylist.py       # Export functionality
│   ├── LikedSongsToPlaylist.py # Liked songs to playlist
│   ├── LikedSongsOperations.py # Playlist to liked songs
│   └── utils.py                # Utility functions
├── assets/
│   ├── sounds/                 # Audio files
│   └── icon/                   # Application icon
├── Exported Playlists/         # Directory for exported files
├── Import Playlists/           # For mass Import playlists to liked songs
├── LICENSE                     # MIT LICENSE
└── README.md                   # Documentation
```
## Known Issues & Limitations 🛠️

- API Rate Limits: Spotify limits the number of requests. If you encounter issues, try again after some time.
- Large Playlists: The script fetches playlists in batches of 100. Ensure your internet connection is stable for large playlists.
- Authentication Timeout: If your session expires, you'll need to re-authenticate via the browser.
## Future Improvements 🌟

- Automatic API fetching from spotify.
- Automatic Playlist transfer between Stream platforms like amazon and apple.
- Progress bar? Maybe IDK


## License 📝

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)


## Author 👨‍💻

Someone who hates Spotify's limitations in transferring playlists to liked songs.

Someone who is frustrated by Spotify's lack of attention to user needs for exporting and transferring songs within and outside the platform.

- Kasra Falahati [@blackat5445](https://www.github.com/blackat5445)
- [Agenzia Magma](https://www.agenziamagma.it)
