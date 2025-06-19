
# Copy Images App

This app scans a source directory for image files (JPG, PNG, GIF, BMP, TIF), recreates the directory structure, and copies them to a target directory.

Now with multi-threaded copy for speed.

## Usage

```bash
# Dry run
python3 copy_images.py --source /mnt/g/Drive/Images --target /mnt/e/Reference/Images --dry-run

# Actual copy
python3 copy_images.py --source /mnt/g/Drive/Images --target /mnt/e/Reference/Images

# Verbose debug
python3 copy_images.py --source /mnt/g/Drive/Images --target /mnt/e/Reference/Images --verbose 2

# Write log to file
python3 copy_images.py --source /mnt/g/Drive/Images --target /mnt/e/Reference/Images --log-file copy_log.txt

# Multi-threaded (16 workers)
python3 copy_images.py --source /mnt/g/Drive/Images --target /mnt/e/Reference/Images --workers 16
```

## Features

- Multi-threaded copying for speed (default: 8 workers)
- Preserves directory structure
- Skips duplicate files (same name & size)
- Supports dry-run mode
- Adjustable verbosity
- Optional log file
- Tested in WSL, Linux

## Requirements

- Python 3.8+
- No external dependencies
