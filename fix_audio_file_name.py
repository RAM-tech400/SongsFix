#!/usr/bin/env python3

import sys
import argparse
import mutagen

song_title = "Unknow"

def print_help():
    help_text = """
Usage: fix_audio_file_name.py [OPTIONS] FILE

Show audio information for the specified audio file.

Positional arguments:
  FILE                  Path to the audio file

Optional arguments:
  --song-info           Showing song information in output.
  -h, --help            Show this help message and exit.
"""
    print(help_text)


def get_song_title(audio):
    if audio.tags:
        song_title = audio.tags.get("TIT2") or audio.tags.get("\xa9nam")
        if song_title:
            # For ID3 (MP3), title is a TextFrame object
            try:
                song_title = song_title.text[0]
            except AttributeError:
                pass
    return song_title

def show_audio_info(file_path):
    try:
        audio = mutagen.File(file_path)
        print("File: " + audio.filename)
        print("Duration: " + str(audio.info.length) + " seconds")
        print("Bitrate: " + str(audio.info.bitrate) + " kbps")
        print("Channels: " + str(audio.info.channels))
        print("Sample Rate: " + str(audio.info.sample_rate) + " Hz")
        print("Title: " + str(get_song_title(audio)) if get_song_title(audio) else "Title: Unknown")
    except Exception as e:
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Show audio information")
    parser.add_argument("file", help="Path to the audio file")
    parser.add_argument("--song-info", help="Showing song information in output.", action="store_true")
    args = parser.parse_args()
    if args.song_info:
        show_audio_info(args.file)
    else:
        print_help()

if __name__ == "__main__":
    main()