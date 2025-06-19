
import argparse
import os
from pathlib import Path
import shutil
from concurrent.futures import ThreadPoolExecutor

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff'}

def is_image_file(file_path):
    return file_path.suffix.lower() in IMAGE_EXTENSIONS

def copy_one(src_file, dest_file, dry_run, verbose):
    if dest_file.exists() and dest_file.stat().st_size == src_file.stat().st_size:
        if verbose >= 2:
            return f"[SKIP] {dest_file}"
        return None

    if not dry_run:
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_file, dest_file)
        return f"[COPY] {dest_file}"
    else:
        return f"[DRYRUN] Would copy: {dest_file}"

def copy_images(source_dir, target_dir, dry_run=False, verbose=1, log_file=None, workers=8):
    source_dir = Path(source_dir).resolve()
    target_dir = Path(target_dir).resolve()

    if not source_dir.is_dir():
        print(f"ERROR: Source directory does not exist: {source_dir}")
        return

    log_lines = []
    def log(msg):
        if verbose > 0 and msg:
            print(msg)
        if log_file and msg:
            log_lines.append(msg)

    print(f"Scanning source: {source_dir}")
    print(f"Target directory: {target_dir}")
    print(f"{'Dry run' if dry_run else 'Copying files'}")
    print(f"Using {workers} worker threads")
    print("=" * 60)

    all_tasks = []

    for root, _, files in os.walk(source_dir):
        rel_root = Path(root).relative_to(source_dir)
        dest_root = target_dir / rel_root

        for file in files:
            src_file = Path(root) / file

            if is_image_file(src_file):
                dest_file = dest_root / file
                all_tasks.append((src_file, dest_file))

    copied_count = 0
    skipped_count = 0

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(copy_one, src, dest, dry_run, verbose)
            for src, dest in all_tasks
        ]

        for future in futures:
            result = future.result()
            if result:
                log(result)
                if result.startswith("[COPY]") or result.startswith("[DRYRUN]"):
                    copied_count += 1
                elif result.startswith("[SKIP]"):
                    skipped_count += 1

    print("=" * 60)
    print(f"Done. {copied_count} files copied. {skipped_count} skipped.")

    if log_file:
        with open(log_file, 'w') as f:
            f.write("\n".join(log_lines))
        print(f"Log written to {log_file}")

def main():
    parser = argparse.ArgumentParser(description="Copy images and preserve directory structure (multi-threaded).")
    parser.add_argument("--source", required=True, help="Source directory (Google Drive mount)")
    parser.add_argument("--target", required=True, help="Target reference directory")
    parser.add_argument("--dry-run", action="store_true", help="Perform dry run (no files copied)")
    parser.add_argument("--verbose", type=int, default=1, help="Verbosity level: 0=quiet, 1=normal, 2=debug")
    parser.add_argument("--log-file", type=str, help="Path to log file")
    parser.add_argument("--workers", type=int, default=8, help="Number of worker threads (default: 8)")

    args = parser.parse_args()

    copy_images(args.source, args.target, args.dry_run, args.verbose, args.log_file, args.workers)

if __name__ == "__main__":
    main()
