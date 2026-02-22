#!/usr/bin/env python3

import argparse
import mutagen
import os
import shutil

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

def fix_audio_file_name(file_path, override_orginal_file=False):
    working_dir = os.path.dirname(file_path)
    original_file_name = file_path.split(os.sep)[-1]
    try:
        audio = mutagen.File(file_path)
        song_title = get_song_title(audio)
        if song_title:
            new_file_name = song_title + "." + audio.filename.split(".")[-1]
            if not override_orginal_file:
                print("Creating a new file with fixed name into \"NameFixedSongs\" directory...")
                if not os.path.exists(working_dir + "/NameFixedSongs"):
                    print("Directory is not exists! Creating directory...")
                    os.makedirs(working_dir + "/NameFixedSongs")
                new_file_path = working_dir + "/NameFixedSongs/" + new_file_name
                print("Coping from: " + file_path + " to " + new_file_path)
                shutil.copy(file_path, new_file_path)
            else:
                print("Renaming file to fixed name at: " + file_path)
                os.rename(file_path, new_file_name)
    except Exception as e:
        print(f"Error: {e}")

def fix_audio_file_name_recursive(file_path, override_orginal_file=False):
    for file in os.listdir(file_path):
        path = file_path + os.sep + file
        if os.path.isdir(path):
            fix_audio_file_name_recursive(path, override_orginal_file)
        else:
            fix_audio_file_name(path, override_orginal_file)

def main():
    parser = argparse.ArgumentParser(description="Show audio information")
    parser.add_argument("file", help="Path to the audio file")
    parser.add_argument("--song-info", help="Showing song information in output.", action="store_true")
    parser.add_argument("--recursive", help="It is needed if you want to working with all items under a directory.", action="store_true")
    args = parser.parse_args()
    if args.song_info:
        show_audio_info(args.file)
    if os.path.isdir(args.file):
        if args.recursive:
            fix_audio_file_name_recursive(args.file)
        else:
            print("Given path is a directory and should pass with \"recursive\" switch (-r or --recursive).")
    else:
        if args.recursive:
            print("For recursive working you should give a directory path. This given path indicates actully to a file!")
        else:
            fix_audio_file_name(args.file)

if __name__ == "__main__":
    main()