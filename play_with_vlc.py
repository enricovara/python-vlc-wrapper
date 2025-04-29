#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 15:34:30 2025

@author: evaran

VLC wrapper – Player
----------

A minimal cross-platform player wrapper for python-vlc for quick fullscreen
playback of audio and video files.

- On Windows/Linux:
    - Video files are played in native VLC fullscreen mode.
    - Audio files are played without opening a window.
- On macOS:
    - Video files are displayed in a PyQt6 frameless window covering the full screen,
      avoiding macOS's "new desktop" fullscreen behavior.
    - Audio files are played headlessly without any GUI.

Dependencies:
    - python-vlc
    - PyQt6 (macOS only)

License: MIT

"""
import sys
import os
import vlc
from time import sleep
import platform

# Only import PyQt6 if on macOS
if platform.system() == "Darwin":
    from PyQt6 import QtWidgets, QtGui, QtCore
    from ctypes import c_void_p, cdll, util

class VLC_Player:
    """
    VLC_Player class
    ----------------
    Instantiates a VLC media player and plays the given media file.
    Handles platform-specific fullscreen behavior.
    Automatically distinguishes between video and audio files based on extension.
    
    Parameters:
    - filepath (str): Path to the media file.
    - log_file (str, optional): Path to a logfile to log audio/video delta warnings. Default is False (no logging).
    """

    def __init__(self, filepath, log_file=False):
        instance = vlc.Instance(["--mouse-hide-timeout=10"])
        media = instance.media_new(filepath)
        player = instance.media_player_new()
        player.set_media(media)

        # Determine if the file is video based on extension
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv']
        _, ext = os.path.splitext(filepath)
        is_video = ext.lower() in video_extensions

        if platform.system() == "Darwin" and is_video:
            self.app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
            self.window = QtWidgets.QMainWindow()

            # Set no window frame and fullscreen without macOS native fullscreen
            self.window.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
            screen_geometry = QtGui.QGuiApplication.primaryScreen().geometry()
            self.window.setGeometry(screen_geometry)
            self.window.show()

            # Set VLC video output to the Qt window
            libappkit = cdll.LoadLibrary(util.find_library('AppKit'))
            view_ptr = c_void_p(int(self.window.winId()))
            player.set_nsobject(view_ptr.value)
        
        elif platform.system() != "Darwin" and is_video:
            player.set_fullscreen(1)

        # --- Play ---
        player.play()
        sleep(0.5)

        # --- Different handling depending on whether it's a video ---
        if platform.system() == "Darwin" and is_video:
            # Poll for playback end while processing Qt events
            while player.get_state() not in (vlc.State.Ended, vlc.State.Error):
                self.app.processEvents()
                sleep(0.05)
            self.window.close()
        else:
            # Windows or Audio file
            while player.get_state() not in (vlc.State.Ended, vlc.State.Error):
                sleep(0.1)

        sleep(0.1)
        player.stop()
        media.release()
        player.release()
        instance.release()

if __name__ == "__main__":
    current_script_dir = os.path.dirname(os.path.realpath(__file__))

    for media_file in os.listdir('examples'):
        full_media_filepath = os.path.join(current_script_dir, 'examples', media_file)

        print(f"\nPlaying {media_file}")
        VLC_Player(full_media_filepath)
