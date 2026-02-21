import sys
import argparse
import mutagen

def show_audio_info(file_path):
    try:
        audio = mutagen.File(file_path)
        print(f"File: {file_path}")
        print(f"Format: {audio.mime}")
        print(f"Size: {audio.info.length} seconds")
        print(f"Bitrate: {audio.info.bitrate} kbps")
        print(f"Channels: {audio.info.channels}")
        print(f"Sample Rate: {audio.info.sample_rate} Hz")
        print(f"Tags: {audio.tags}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Show audio information")
    parser.add_argument("file", help="Path to the audio file")
    args = parser.parse_args()
    show_audio_info(args.file)

if __name__ == "__main__":
    main()