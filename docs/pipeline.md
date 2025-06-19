# Full Pipeline Guide

---

## Workflow:

1️⃣ Mount Google Drive  
2️⃣ Copy images  
3️⃣ Sort by date  
4️⃣ Organize folders  
5️⃣ Check rotations (optional)  
6️⃣ Process in Photoshop (UXP panel or `.jsx`)

---

## Example Commands:

```bash
~/mount_gdrive.sh
python copy_images.py --source ~/google --target /mnt/e/Images --log-file=logfile
python file_date_sorter.py /mnt/e/Images --output sorter.log
python file_date_organizer.py sorter.log --dest /mnt/e/SortedImages
python rotation_checker.py /mnt/e/Images --output rotations.csv
