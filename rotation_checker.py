#!/usr/bin/env python3

import os
import argparse
from PIL import Image, ExifTags

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"]

# EXIF tag ID for Orientation
EXIF_ORIENTATION_TAG = next(k for k, v in ExifTags.TAGS.items() if v == 'Orientation')

# Mapping EXIF orientation → rotation
ORIENTATION_TO_ROTATION = {
    1: 0,
    3: 180,
    6: 270,
    8: 90
}

def is_image_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in IMAGE_EXTENSIONS

def check_rotation(file_path):
    try:
        with Image.open(file_path) as img:
            exif = img._getexif()
            if exif and EXIF_ORIENTATION_TAG in exif:
                orientation = exif[EXIF_ORIENTATION_TAG]
                rotation = ORIENTATION_TO_ROTATION.get(orientation, 0)
                if rotation != 0:
                    return rotation
    except Exception as e:
        print(f"ERROR reading {file_path}: {e}")
    return 0

def scan_directory(root_dir):
    flagged = []

    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if not is_image_file(fname):
                continue

            full_path = os.path.join(dirpath, fname)
            rotation = check_rotation(full_path)

            # For PNG, BMP — no EXIF: heuristic
            if rotation == 0 and fname.lower().endswith(('.png', '.bmp')):
                try:
                    with Image.open(full_path) as img:
                        w, h = img.size
                        if h > w * 1.2:
                            # Portrait image — might need 90-degree rotation
                            rotation = 90
                except Exception as e:
                    print(f"ERROR reading {full_path}: {e}")

            if rotation != 0:
                flagged.append((full_path, rotation))

    return flagged

def main():
    parser = argparse.ArgumentParser(description="Check images for needed rotation")
    parser.add_argument("source", help="Source directory to scan")
    parser.add_argument("--output", help="Optional output CSV")

    args = parser.parse_args()

    print(f"Scanning: {args.source}")

    flagged = scan_directory(args.source)

    for path, rotation in flagged:
        print(f"{rotation}°: {path}")

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            for path, rotation in flagged:
                f.write(f"{path},{rotation}\n")
        print(f"Saved to: {args.output}")

if __name__ == "__main__":
    main()
