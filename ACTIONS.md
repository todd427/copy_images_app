# ACTIONS.md

## 📂 **Image Pipeline Workflow**

This document explains the step-by-step process for managing and organizing images from Google Drive into Photoshop-ready folders.

---

## 1️⃣ **Mount Google Drive (via rclone)**

```bash
~/mount_gdrive.sh
```

- Mounts Google Drive at: `~/google`
- Uses `--vfs-cache-mode full` for full access

To unmount:

```bash
~/unmount_gdrive.sh
```

---

## 2️⃣ **Copy images from Google Drive to local target**

Run the image copy script:

```bash
python copy_images.py --source ~/google --target /mnt/e/Images --dry-run --log-file=logfile
```

Once confirmed:

```bash
python copy_images.py --source ~/google --target /mnt/e/Images --log-file=logfile
```

- Uses multi-threaded copy
- Skips duplicates
- Optionally ZIP after (if enabled)

---

## 3️⃣ **Sort images by date (scanner step)**

Run the date sorter:

```bash
python file_date_sorter.py /mnt/e/Images --output sorter.log
```

- Recursively scans `/mnt/e/Images`
- Extracts date from filenames
- Outputs `sorter.log` with full paths, sorted by date

---

## 4️⃣ **Organize images by date**

Run the organizer:

```bash
python file_date_organizer.py sorter.log --dest /mnt/e/SortedImages --dry-run
```

To actually move:

```bash
python file_date_organizer.py sorter.log --dest /mnt/e/SortedImages
```

Or to copy (instead of move):

```bash
python file_date_organizer.py sorter.log --dest /mnt/e/SortedImages --copy
```

- Creates `YYYY/MM/DD/` folder structure
- Moves or copies files
- Skips already-existing files
- Safe to re-run

---

## 5️⃣ **Check image rotation (optional step)**

Run the rotation checker:

```bash
python rotation_checker.py /mnt/e/Images --output rotations.csv
```

- Recursively scans `/mnt/e/Images`
- Reads EXIF orientation (JPG/TIF)
- Heuristically checks PNG, BMP based on aspect ratio
- Outputs `rotations.csv`: `filename, rotation_angle`
- Ready for Photoshop or ExifTool batch rotation

---

## 6️⃣ **Batch process in Photoshop (Auto Color / White Balance)**

Use the provided script:

```text
batch_auto_color.jsx
```

**Run in Windows Photoshop:**

1. Open Photoshop (Windows app)
2. Menu: `File → Scripts → Browse...`
3. Select `batch_auto_color.jsx`
4. Select Input Folder (example: `E:\SortedImages` or `\\wsl.localhost\Ubuntu\home\todd\google`)
5. Select Output Folder (example: `E:\WhiteBalancedImages`)

The script will:

- Recursively process images
- Apply Auto Color (White Balance)
- Save results in Output folder
- Preserve original folder structure

---

## 7️⃣ **Upload to Bunny CDN**

Run the uploader:

```bash
# Dry-run:
python upload_to_bunny.py /mnt/e/SortedImages --output uploaded_urls.txt --dry-run

# Real upload:
python upload_to_bunny.py /mnt/e/SortedImages --output uploaded_urls.txt
```

- Recursively scans `/mnt/e/SortedImages`
- Uploads all image files
- Generates `uploaded_urls.txt` with public URLs

---

## Notes:

🗼 The entire process is recursive  
📱 Dry-run supported at every step  
🔄 Designed to be safe and restartable  
📃 Log files are generated at each step  
🔗 Photoshop batch runs in Windows app, WSL folder access confirmed via `\\wsl.localhost\...`  
📁 Bunny CDN upload supports `--dry-run`

---