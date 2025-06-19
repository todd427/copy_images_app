#!/bin/bash

# Mount Google Drive
~/mount_gdrive.sh

# Copy images
python copy_images.py --source ~/google --target /mnt/e/Images --log-file=logfile

# Sort images
python file_date_sorter.py /mnt/e/Images --output sorter.log

# Organize images
python file_date_organizer.py sorter.log --dest /mnt/e/SortedImages

# Optional: Rotation check
python rotation_checker.py /mnt/e/Images --output rotations.csv

echo "Pipeline complete. Ready for Photoshop batch!"
