#!/usr/bin/env python3

import os
import re
import argparse
from datetime import datetime

# Extended list of date patterns to match
DATE_PATTERNS = [
    re.compile(r'(\d{4})[-_\.]?(\d{2})[-_\.]?(\d{2})'),    # 2023-06-05 or 2023.06.05 or 2023_06_05
    re.compile(r'(\d{4})(\d{2})(\d{2})'),                  # 20230605
    re.compile(r'IMG[_-](\d{4})(\d{2})(\d{2})'),           # IMG_20230605
    re.compile(r'(\d{4})\.(\d{2})\.(\d{2})'),              # 2023.06.05
]

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff", ".psd"]

def extract_date_from_filename(filename):
    name = os.path.basename(filename).lower()

    for pattern in DATE_PATTERNS:
        match = pattern.search(name)
        if match:
            year, month, day = match.groups()
            try:
                return datetime(int(year), int(month), int(day))
            except ValueError:
                return None
    return None

def is_image_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in IMAGE_EXTENSIONS

def scan_directory(root_dir):
    dated_files = []

    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if not is_image_file(fname):
                continue

            date = extract_date_from_filename(fname)
            if date:
                full_path = os.path.join(dirpath, fname)
                dated_files.append((date, full_path))

    return sorted(dated_files, key=lambda x: x[0])

def main():
    parser = argparse.ArgumentParser(description="Sort image files by date extracted from filename.")
    parser.add_argument("source", help="Source directory to scan")
    parser.add_argument("--output", help="Optional output file")

    args = parser.parse_args()

    print(f"Scanning: {args.source}")

    files = scan_directory(args.source)

    for date, path in files:
        print(f"{date.date()}  {path}")

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            for date, path in files:
                f.write(f"{date.date()}  {path}\n")
        print(f"Saved to: {args.output}")

if __name__ == "__main__":
    main()
