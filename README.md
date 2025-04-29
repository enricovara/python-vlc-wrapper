# python-vlc-wrapper
Play video and audio from python with 1 line, on any platform (Window, Mac, Linux, etc)

A minimal cross-platform wrapper for [python-vlc](https://github.com/oaubert/python-vlc) for quick fullscreen playback of audio and video files.

This project provides an extremely lightweight tool to play media files cleanly, with one line.

## TO-DO
- Add fancy features so that it's equally easy to pause/stop playback with one line of code.

## Features

- Fullscreen video playback:
  - Windows/Linux: native VLC fullscreen.
  - macOS: frameless PyQt6 window covering the screen (avoiding macOS fullscreen Desktop switching).
- Audio playback with no window.
- Automatically detects media type based on file extension.
- Minimal dependencies.

## Installation

Install the required Python packages:

```bash
pip install python-vlc
pip install PyQt6  # Only needed on macOS (or conda install pyqt)
```

Also ensure you have VLC installed on your system.

## Usage

Organize your media files inside an `examples/` folder relative to the script.

Then run:

```bash
python play_with_vlc.py
```

The script will:
- Iterate through all files in the `examples/` directory.
- Play each file appropriately (audio or video).
- Close automatically at the end of each media.

## Supported Media Types

Video:
- .mp4
- .avi
- .mov
- .mkv
- .flv

Audio:
- .wav
- .mp3
- .aac
- etc. (any non-video extension)

## How It Works

- On Windows/Linux, VLC's native `set_fullscreen(1)` is used for videos.
- On macOS, a PyQt6 fullscreen frameless window is created and VLC renders into it.
- For audio files, no window is created at all — audio plays silently.

## Notes

- PyQt6 is only required on macOS.
- python-vlc is required on all platforms.
- This wrapper relies on simple file extension matching to detect video vs audio.
- For advanced users, VLC track analysis could be used for even more robustness.

## License

MIT License. See the LICENSE file for full details.

## Credits

- Built on top of [oaubert/python-vlc](https://github.com/oaubert/python-vlc).
