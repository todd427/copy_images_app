# BunnyGo.md

# Bunny CDN for `copy_images_app`

This file explains how to use **Bunny CDN + Storage** for production use of the image pipeline.

---

## Why Bunny CDN

- 🌟 Super cheap: $0.01/GB storage, ~$0.01/GB egress
- 🌟 Global CDN included
- 🌟 Simple API and great GUI
- 🌟 Built-in Image Optimizer (optional, $9/mo)
- 🌟 No S3 complexity

**Perfect for:**

- Batch images
- Public image delivery
- Archival
- Reference image hosting

---

## Setup Steps

### 1. Create Account

- [https://bunny.net/storage/](https://bunny.net/storage/)
- Add "Storage Zone": `copy-images-app`
- Enable Bunny CDN for this zone
- Pull Zone example: `copy-images.b-cdn.net`

### 2. Upload Options

- Web GUI
- CLI: `bunnycdn-cli`
- Python API (see below)

### 3. Django Settings Example

```python
# settings.py

BUNNY_STORAGE_NAME = "copy-images-app"
BUNNY_STORAGE_API_KEY = "YOUR_API_KEY"
BUNNY_STORAGE_REGION = "de"  # or your region

BUNNY_STORAGE_URL = "https://copy-images.b-cdn.net"
```

### 4. Python Upload Example

```python
import requests
import os

BUNNY_API_URL = "https://storage.bunnycdn.com/copy-images-app/"
BUNNY_API_KEY = "YOUR_API_KEY"

def upload_file(local_path, remote_path):
    url = BUNNY_API_URL + remote_path
    headers = {
        "AccessKey": BUNNY_API_KEY
    }
    with open(local_path, 'rb') as f:
        resp = requests.put(url, data=f, headers=headers)
    if resp.status_code == 201:
        print(f"Uploaded: {remote_path}")
    else:
        print(f"ERROR uploading {remote_path}: {resp.status_code} - {resp.text}")

# Example:
upload_file("/mnt/e/SortedImages/2025/06/19/image1.jpg", "2025/06/19/image1.jpg")
```

### 5. Public URL

```text
https://copy-images.b-cdn.net/2025/06/19/image1.jpg
```

### 6. Pricing (2025-06)

| Feature         | Cost                |
| --------------- | ------------------- |
| Storage         | $0.01 / GB / month |
| Egress (US/EU)  | ~$0.01 / GB       |
| Image Optimizer | $9/mo flat         |

---

## Recommended Use

- Store pipeline output `/mnt/e/SortedImages` in Bunny
- Serve public images from Bunny CDN
- Optimize delivery (WebP/AVIF) using Image Optimizer

---

## Next Steps

- Add `upload_to_bunny.py`
- Add to `pipeline.sh`
- Example command:

```bash
# Dry-run:
python upload_to_bunny.py /mnt/e/SortedImages --output uploaded_urls.txt --dry-run

# Real upload:
python upload_to_bunny.py /mnt/e/SortedImages --output uploaded_urls.txt
```

---

## Summary

- 🔄 Bunny CDN is **perfect** for current pipeline
- 🌟 Easy integration with Python
- 🌟 Cheapest, simplest solution
- 🔄 `upload_to_bunny.py` supports `--dry-run`

---

**Generated: 2025-06-19**