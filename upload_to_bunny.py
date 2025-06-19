#!/usr/bin/env python3

import os
import argparse
import requests

# Config — replace YOUR_API_KEY
BUNNY_STORAGE_NAME = "copy-images-app"
BUNNY_API_KEY = "YOUR_API_KEY"
BUNNY_API_URL = f"https://storage.bunnycdn.com/{BUNNY_STORAGE_NAME}/"
BUNNY_PUBLIC_URL = f"https://copy-images.b-cdn.net/"

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"]

def is_image_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in IMAGE_EXTENSIONS

def upload_file(local_path, remote_path, dry_run=False):
    url = BUNNY_API_URL + remote_path
    full_url = BUNNY_PUBLIC_URL + remote_path

    if dry_run:
        print(f"[DRY-RUN] Would upload: {remote_path}")
        return True

    headers = {
        "AccessKey": BUNNY_API_KEY
    }
    with open(local_path, 'rb') as f:
        resp = requests.put(url, data=f, headers=headers)
    if resp.status_code == 201:
        print(f"Uploaded: {remote_path}")
        return True
    else:
        print(f"ERROR uploading {remote_path}: {resp.status_code} - {resp.text}")
        return False

def scan_and_upload(root_dir, url_list_file, dry_run=False):
    url_list = []

    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if not is_image_file(fname):
                continue

            local_path = os.path.join(dirpath, fname)

            # Create relative path for remote (strip root_dir)
            rel_path = os.path.relpath(local_path, root_dir).replace("\\", "/")

            success = upload_file(local_path, rel_path, dry_run=dry_run)
            if success:
                full_url = BUNNY_PUBLIC_URL + rel_path
                url_list.append(full_url)

    # Save URL list
    with open(url_list_file, 'w', encoding='utf-8') as f:
        for url in url_list:
            f.write(url + '\n')

    print(f"\nDone. {'(Dry-run) ' if dry_run else ''}Uploaded {len(url_list)} files.")
    print(f"URL list saved to: {url_list_file}")

def main():
    parser = argparse.ArgumentParser(description="Upload images to Bunny CDN and generate URL list")
    parser.add_argument("source", help="Source directory to scan and upload")
    parser.add_argument("--output", default="uploaded_urls.txt", help="Output file for URL list")
    parser.add_argument("--dry-run", action="store_true", help="Dry run (show what would be uploaded)")

    args = parser.parse_args()

    print(f"Uploading from: {args.source}")
    print(f"Saving URL list to: {args.output}")
    if args.dry_run:
        print("DRY-RUN enabled — no files will be uploaded.")

    scan_and_upload(args.source, args.output, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
