import os
import shutil
from pathlib import Path

def split_folders_and_media(main_folder):
    main_path = Path(main_folder)

    # Create destination folders
    folders_dir = main_path / "folders"
    media_dir = main_path / "media"
    folders_dir.mkdir(exist_ok=True)
    media_dir.mkdir(exist_ok=True)

    for item in main_path.iterdir():
        # Skip the new destination folders
        if item.name in ["folders", "media"]:
            continue

        # Move subfolders
        if item.is_dir():
            dest = folders_dir / item.name
            if not dest.exists():
                shutil.move(str(item), str(dest))
                print(f"📁 Moved folder: {item.name}")

        # Move media files
        elif item.is_file():
            dest = media_dir / item.name
            if not dest.exists():
                shutil.move(str(item), str(dest))
                print(f"🎞️ Moved media: {item.name}")

    print("\n✅ Split complete! All folders → 'folders', all media → 'media'")

if __name__ == "__main__":
    folder_path = input("Enter the path to your main folder: ").strip('"')
    if os.path.exists(folder_path):
        split_folders_and_media(folder_path)
    else:
        print("❌ Folder does not exist!")
