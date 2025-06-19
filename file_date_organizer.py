#!/usr/bin/env python3

import os
import argparse
import shutil
from datetime import datetime

def parse_sorted_list(file_path):
    entries = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                date_str, path = line.strip().split(maxsplit=1)
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                entries.append((date_obj, path))
            except ValueError:
                print(f"Skipping malformed line: {line.strip()}")
    return entries

def organize_files(entries, dest_root, dry_run=False, copy_mode=False):
    for date_obj, src_path in entries:
        yyyy = f"{date_obj.year:04d}"
        mm = f"{date_obj.month:02d}"
        dd = f"{date_obj.day:02d}"

        dest_dir = os.path.join(dest_root, yyyy, mm, dd)
        os.makedirs(dest_dir, exist_ok=True)

        filename = os.path.basename(src_path)
        dest_path = os.path.join(dest_dir, filename)

        if os.path.exists(dest_path):
            print(f"SKIP (already exists): {dest_path}")
            continue

        if dry_run:
            print(f"[DRY-RUN] Would {'COPY' if copy_mode else 'MOVE'}: {src_path} → {dest_path}")
        else:
            try:
                if copy_mode:
                    shutil.copy2(src_path, dest_path)
                    print(f"COPY: {src_path} → {dest_path}")
                else:
                    shutil.move(src_path, dest_path)
                    print(f"MOVE: {src_path} → {dest_path}")
            except Exception as e:
                print(f"ERROR moving {src_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Organize images by date into folders (YYYY/MM/DD)")
    parser.add_argument("input_list", help="Sorted images list file (from file_date_sorter.py)")
    parser.add_argument("--dest", required=True, help="Destination root folder")
    parser.add_argument("--dry-run", action="store_true", help="Dry run (show what would happen)")
    parser.add_argument("--copy", action="store_true", help="Copy instead of move")

    args = parser.parse_args()

    print(f"Reading list: {args.input_list}")
    print(f"Destination: {args.dest}")
    if args.dry_run:
        print("DRY-RUN enabled")
    if args.copy:
        print("COPY mode (default is MOVE)")

    entries = parse_sorted_list(args.input_list)
    print(f"Found {len(entries)} files to process.")

    organize_files(entries, args.dest, dry_run=args.dry_run, copy_mode=args.copy)

if __name__ == "__main__":
    main()
