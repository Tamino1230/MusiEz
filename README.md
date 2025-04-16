# babTomaMusic

Please use the [latest Version](https://github.com/Tamino1230/babTomaMusic/releases/latest)

babTomaMusic is a Python-based desktop music application created by **Tamino1230**. It provides an easy-to-use interface for managing playlists, downloading songs, and integrating with Discord Rich Presence. The application also includes features like hotkeys, sleep timers, and song information retrieval.

---

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Wrapped](#btm-wrapped)
6. [Hotkeys](#hotkeys)
7. [Known Issues](#known-issues)
8. [License](#license)
9. [Contact](#contact)

---

## Features

- **Music Playback**: Play, pause, stop, and skip songs in your playlist.
- **Playlist Management**: Load songs from folders and manage playlists easily.
- **Song Downloading**: Download songs directly from YouTube or other supported platforms.
- **Discord Rich Presence**: Show your current song and playback status on Discord.
- **Hotkeys**: Control playback using customizable hotkeys.
- **Sleep Timer**: Automatically stop playback after a specified time.
- **Song Information**: Fetch song details and lyrics from online sources.
- **Customizable Settings**: Adjust volume, shuffle, repeat, and more.
- **Error Handling**: Debugging tools to identify and resolve issues.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- FFmpeg (included in the project) (Install automaticly in setup.bat)
- Required Python libraries: (Install automaticly in setup.bat)
  ```
  mutagen
  yt-dlp
  pypresence
  pygame
  keyboard
  requests
  ```

### Steps
1. Download the project as a ZIP file from the [GitHub repository](https://github.com/Tamino1230/babTomaMusic).
2. Extract the ZIP file to a folder of your choice.
3. Run the `setup.bat` file to install dependencies.
4. After setup, run the `click and extract me.bat` file.
5. Launch the application by running `main.py`.

---

## Configuration

The application settings can be customized in the `config.py` file. Below are the key configuration options:

- **Background Color**: `bgcolor` (default: `"light blue"`)
- **Default Folder**: `default_folder` (default: `"download_folder"`)
- **Max Volume**: `max_volume` (default: `200`)
- **Sleep Timer**: `sleeptimer` (default: `True`)
- **Hotkeys**: Enable or disable hotkeys using `hotkeys_active`.

For more details, refer to the comments in the `config.py` file.

---

## Usage

### Main Features
1. **Load Songs**: Use the "Load Songs" option in the menu to load songs from a folder.
2. **Play Songs**: Double-click a song in the playlist or use the playback controls.
3. **Download Songs**: Enter a YouTube URL in the input field and click "Download MP3".
4. **Discord Integration**: Enable or disable Discord Rich Presence using the toggle button.
5. **Sleep Timer**: Start or cancel the sleep timer from the "Extra Functions" menu.

### Advanced Features
- **Song Information**: Fetch song details and lyrics using the "Info and Lyrics" option.
- **Share**: Share your current song on Twitter or other platforms.

---

## bTM Wrapped

The `wrapped.py` script is a standalone feature inspired by Spotify Wrapped, designed specifically for the **babTomaMusic (btM)** app. It provides users with a personalized summary of their music listening habits, offering insights into their most-played songs, total listening time, and more.

Example Output:
```
Your Top 10 Songs:
1. Song A - 669 Minuten
2. Song B - 555 Minuten
...

Total Playtime:
112 hours and 9 minutes

Songs Played Less Than 5 Minutes (Top 5):
- Song X (4 Minuten)
...

Your Least Played 5 Songs:
1. Song Y - 0 Minuten

Unique Songs Played:
269 unique songs
```

This feature is now part of a dedicated repository: [bTM-Wrapped](https://github.com/Tamino1230/bTM-Wrapped).


## Hotkeys

The following hotkeys are available (if enabled in `config.py`):

- **Pause/Unpause**: `Ctrl+F6`
- **Next Song**: `Ctrl+F7`
- **Previous Song**: `Ctrl+F5`
- **Start Sleep Mode**: `Shift+Ctrl+9`

---

## Known Issues

- **Incorrect Song Display**: Sometimes the wrong song is displayed in the playlist.
- **Python Installation in Setup**: The `setup.bat` file may fail to install Python. Restart the setup if this occurs.
  Please Install Python Manually.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## Contact

For questions, feedback, or support, contact **Tamino1230**:

- **Discord**: [@tamino1230](https://discord.com/users/702893526303637604)
- **GitHub**: [babTomaMusic Repository](https://github.com/Tamino1230/babTomaMusic)
- **Twitter**: [@NukeTamino](https://twitter.com/NukeTamino)

---

## Project Repository

Find the source code and updates at: [https://github.com/Tamino1230/babTomaMusic](https://github.com/Tamino1230/babTomaMusic)
