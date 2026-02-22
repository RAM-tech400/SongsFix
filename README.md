# SongsFit

A command-line utility for displaying audio file metadata and renaming audio files based on their embedded tags (e.g. artist, title). Supports single files as well as recursive batch processing of directories.

## Features

- Display detailed song information (duration, bitrate, channels, sample rate, title)
- Fix audio file names using embedded metadata tags
- Process single files or entire directories recursively
- Copy files to output directory or rename in place

## Requirements

- Python 3.6+
- [mutagen](https://mutagen.readthedocs.io/) — for metadata extraction

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```
fix_audio_file_name.py [OPTIONS] FILE
```

### Arguments

| Option | Short | Description |
|--------|-------|-------------|
| `--song-info` | `-i` | Show song information in the output |
| `--recursive` | `-r` | Process all items under a directory recursively |
| `--output-dir DIR` | `-o DIR` | Output directory when used with `--recursive` |
| `--copy` | `-c` | Copy files instead of renaming them (uses more storage) |

### Examples

Show song information for a single file:

```bash
python fix_audio_file_name.py --song-info song.mp3
```

Fix a single file (creates `NameFixedSongs/` subdirectory with renamed copy):

```bash
python fix_audio_file_name.py song.mp3
```

Process all audio files in a directory recursively, copying to a flat output directory:

```bash
python fix_audio_file_name.py --recursive --output-dir output_dir --copy input_dir/
```

## License

MIT
