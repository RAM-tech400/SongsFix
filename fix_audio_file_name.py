#!/usr/bin/env python3
"""
A command-line utility for displaying audio file metadata and correcting audio file names based on their embedded tags.
Supports single files as well as recursive batch processing of directories. Provides options to copy or rename files,
specifying output directories, and displaying detailed song information.

Dependencies:
    - mutagen (for metadata extraction)
    - argparse (for argument parsing)
    - os, shutil (for file and directory operations)

Example usage:
    python fix_audio_file_name.py --song-info song.mp3
    python fix_audio_file_name.py --recursive --output-dir output_dir --copy input_dir/
"""

import argparse
import mutagen
import os
import shutil

song_title = "Unknow"

def init_args():
    parser = argparse.ArgumentParser(description="Show audio information")

    parser.add_argument("file", help="Path to the audio file")
    parser.add_argument("-i", "--song-info", help="Showing song information in output.", action="store_true")
    parser.add_argument("-r", "--recursive", help="It is needed if you want to working with all items under a directory.", action="store_true")
    parser.add_argument("-o", "--output-dir", help="Used with --recursive option to setting output directory. It ignores files tree or hierarchy.")
    parser.add_argument("-c", "--copy", help="Copying files instead of renaming those. If used take more storage space.", action="store_true")
    return parser.parse_args()

def print_help():
    help_text = """
Usage: fix_audio_file_name.py [OPTIONS] FILE

Show audio information or fix the audio file name based on tags.

Positional arguments:
  FILE                    Path to the audio file.

Optional arguments:
  --song-info, -i         Show song information in the output.
  --recursive, -r         Process all items under a directory recursively.
  --output-dir DIR, -o DIR
                          Output directory when used with --recursive.
  --copy, -c              Copy files instead of renaming them.
  -h, --help              Show this help message and exit.

Examples:
  fix_audio_file_name.py song.mp3
  fix_audio_file_name.py --song-info song.mp3
  fix_audio_file_name.py --recursive --output-dir output_dir --copy input_dir/
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

def fix_audio_file_name(file_path, override=False, output_dir=None):
    working_dir = os.path.dirname(file_path)
    original_file_name = file_path.split(os.sep)[-1]
    try:
        audio = mutagen.File(file_path)
        song_title = str(get_song_title(audio)).replace(" ", "")
        if original_file_name == song_title:
            print(original_file_name + " is the correct name. Do not need to change it.")
            return
        if song_title:
            new_file_name = song_title + "." + audio.filename.split(".")[-1]
            if not override:
                if output_dir == None:
                    output_dir = working_dir + "/NameFixedSongs"
                print(f"Creating a new file with fixed name into \"{output_dir}\" directory...")
                if not os.path.exists(output_dir):
                    print("Directory is not exists! Creating directory...")
                    os.makedirs(output_dir)
                new_file_path = output_dir + os.sep + new_file_name
                print("Coping from: " + file_path + " to " + new_file_path)
                shutil.copy(file_path, new_file_path)
            else:
                print("Renaming file to fixed name at: " + file_path)
                new_file_path = working_dir + os.sep + new_file_name
                print("Output file: " + new_file_path)
                os.rename(file_path, new_file_path)
    except Exception as e:
        print(f"Error: {e}")

def fix_audio_file_name_recursive(file_path, override=False, origin=None):
    for file in os.listdir(file_path):
        path = file_path + os.sep + file
        if os.path.isdir(path):
            fix_audio_file_name_recursive(path, override, origin=origin)
        else:
            if origin:
                fix_audio_file_name(path, override, output_dir=origin+"/NameFixedSongs")
            else:
                fix_audio_file_name(path, override)

def main():
    args = init_args()
    if args.song_info:
        show_audio_info(args.file)
    if os.path.isdir(args.file):
        if args.recursive:
            fix_audio_file_name_recursive(args.file, override=(not args.copy), origin=args.output_dir)
        else:
            print("Given path is a directory and should pass with \"recursive\" switch (-r or --recursive).")
    else:
        if args.recursive:
            print("For recursive working you should give a directory path. This given path indicates actully to a file!")
        else:
            fix_audio_file_name(args.file, override=(not args.copy))

if __name__ == "__main__":
    main()