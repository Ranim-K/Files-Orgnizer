import os
import re
import shutil
from pathlib import Path
import calendar
from datetime import datetime

def get_media_creation_date(file_path: Path) -> datetime:
    """
    Try to get the file's creation date (fallback if no date in filename).
    """
    try:
        created_time = file_path.stat().st_ctime  # Windows creation time
    except AttributeError:
        created_time = file_path.stat().st_mtime  # Unix fallback
    return datetime.fromtimestamp(created_time)

def organize_videos_by_date(main_folder):
    main_path = Path(main_folder)

    # Step 1: Move all files from subfolders to main folder
    for root, _, files in os.walk(main_path):
        for file in files:
            file_path = Path(root) / file
            if file_path.parent != main_path:
                dest_path = main_path / file
                if not dest_path.exists():
                    shutil.move(str(file_path), str(dest_path))

    # Step 2: Sort files by date
    date_pattern = re.compile(r'(19|20)\d{2}[-_/.]\d{2}[-_/.]\d{2}')  # handles -, _, /, . separators

    for file in main_path.iterdir():
        if file.is_file():
            # Clean name of any weird unicode
            clean_name = file.name.strip().replace('\u202a', '').replace('\u202c', '')

            match = date_pattern.search(clean_name)
            if match:
                # Normalize date to YYYY-MM-DD
                date_str = match.group().replace('_', '-').replace('/', '-').replace('.', '-')
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    print(f"⚠️ Skipping invalid date format in: {file.name}")
                    continue
            else:
                # Use file creation date if no date in filename
                date_obj = get_media_creation_date(file)
                print(f"ℹ️ Used media creation date for: {file.name}")

            year = str(date_obj.year)
            month_name = calendar.month_name[date_obj.month]
            day = f"{date_obj.day:02d}"

            dest_folder = main_path / year / month_name / day
            dest_folder.mkdir(parents=True, exist_ok=True)

            shutil.move(str(file), str(dest_folder / file.name))

    print("✅ All videos organized by Year → Month → Day (filename or media creation date)")

if __name__ == "__main__":
    folder_path = input("Enter the path to your main folder: ").strip('"')
    organize_videos_by_date(folder_path)
