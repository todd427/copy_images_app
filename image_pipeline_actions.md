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

## 5️⃣ **Process in Photoshop**

Open folder:

```
E:\SortedImages
```

- Batch process using Actions or `.jsx` scripts in Photoshop

---

## Notes:

🗼 The entire process is recursive\
📱 Dry-run supported at every step\
🔄 Designed to be safe and restartable\
📃 Log files are generated at each step

---

