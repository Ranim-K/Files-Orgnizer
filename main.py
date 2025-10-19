import os
import shutil
from art import *
from pathlib import Path

# --- Helper Functions ---

def list_items(folder):
    """Return all files + subfolders (sorted)."""
    items = [os.path.join(folder, i) for i in os.listdir(folder)]
    items.sort()
    return [i for i in items if i != os.path.abspath(__file__)]  # avoid moving script itself

def make_folder(path):
    """Create folder if not exists."""
    os.makedirs(path, exist_ok=True)

# --- 1. Split Files ---
def split_files(folder, group_size=10):
    items = list_items(folder)
    group = 1
    index = 0

    while index < len(items):
        group_folder = os.path.join(folder, f"#{group:02}")
        make_folder(group_folder)

        for _ in range(group_size):
            if index >= len(items): break
            item = items[index]
            try:
                shutil.move(item, group_folder)
            except Exception as e:
                print(f"❌ Failed to move {item}: {e}")
            index += 1

        group += 1
    print(f"✅ Files split successfully into groups of {group_size}!")

# --- 2. Small Files Cleanup ---
def small_files_cleanup(folder):
    send_them_folder = os.path.join(folder, "send_them")
    make_folder(send_them_folder)

    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size_kb = os.path.getsize(file_path) / 1024
                if size_kb <= 500 and "send_them" not in root:
                    shutil.move(file_path, send_them_folder)
                    print(f"🧹 Moved small file: {file}")
            except Exception as e:
                print(f"❌ Error with {file_path}: {e}")

    print("✅ Small files moved to 'send_them' folder.")

# --- 3. Type Sorter ---
def type_sorter(folder):
    video_ext = [".mp4", ".mkv", ".avi", ".mov", ".flv"]
    photo_ext = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]

    video_folder = os.path.join(folder, "videos")
    photo_folder = os.path.join(folder, "photos")
    other_folder = os.path.join(folder, "other")

    for path in [video_folder, photo_folder, other_folder]:
        make_folder(path)

    for item in list_items(folder):
        if os.path.isdir(item): continue  # skip folders
        ext = os.path.splitext(item)[1].lower()

        if ext in video_ext:
            dest = video_folder
        elif ext in photo_ext:
            dest = photo_folder
        else:
            dest = other_folder

        try:
            shutil.move(item, dest)
        except Exception as e:
            print(f"❌ Failed to move {item}: {e}")

    print("✅ Files sorted by type!")

# --- 4. Re-order Files ---
def reorder_files(folder):
    all_files = []
    group_folders = []

    for i in os.listdir(folder):
        if i.startswith("#") and os.path.isdir(os.path.join(folder, i)):
            group_folders.append(os.path.join(folder, i))

    group_folders.sort()

    for g in group_folders:
        for i in os.listdir(g):
            all_files.append(os.path.join(g, i))

    # Clear all group folders
    for g in group_folders:
        for i in os.listdir(g):
            os.remove(os.path.join(g, i))

    # Refill them correctly (10 per group)
    index = 0
    group = 1
    while index < len(all_files):
        group_folder = os.path.join(folder, f"#{group:02}")
        make_folder(group_folder)
        for _ in range(10):
            if index >= len(all_files): break
            try:
                shutil.move(all_files[index], group_folder)
            except Exception as e:
                print(f"❌ Error moving file: {e}")
            index += 1
        group += 1

    print("✅ Reordered all group folders!")

# --- 5. Group Consecutive Videos ---
def group_consecutive_videos(folder):
    video_ext = [".mp4", ".mkv", ".avi", ".mov", ".flv"]
    files = [f for f in os.listdir(folder) if os.path.splitext(f)[1].lower() in video_ext]

    # Extract numeric filenames only
    nums = []
    for f in files:
        name, _ = os.path.splitext(f)
        if name.isdigit():
            nums.append(int(name))

    if not nums:
        print("⚠️ No numeric video files found.")
        return

    nums.sort()
    groups = []
    group = [nums[0]]

    for n in nums[1:]:
        if n == group[-1] + 1:
            group.append(n)
        else:
            groups.append(group)
            group = [n]
    groups.append(group)

    # Create folders for consecutive sequences
    for g in groups:
        if len(g) > 1:
            folder_name = f"Group_{g[0]}-{g[-1]}"
            full_path = os.path.join(folder, folder_name)
            make_folder(full_path)

            for num in g:
                for f in files:
                    if f.startswith(str(num)):
                        src = os.path.join(folder, f)
                        dst = os.path.join(full_path, f)
                        try:
                            shutil.move(src, dst)
                        except Exception as e:
                            print(f"❌ Failed to move {f}: {e}")
                        break

    print("✅ Consecutive video files grouped successfully!")

# --- Main Menu ---
tprint("Files Orgnizer")
print("1. Split Files. ")
print("2. Small files cleanup. ")
print("3. Type sorter. ")
print("4. Re-order files. ")
print("5. Group consecutive videos. ")

choice = input("Pick a choice (1-5): ").strip()
path = input("Enter folder path: ").strip()

if not os.path.exists(path):
    print("❌ Folder does not exist!")
else:
    if choice == "1":
        group_size_input = input("How many files per group? (default = 10): ").strip()
        group_size = int(group_size_input) if group_size_input.isdigit() else 10
        split_files(path, group_size)
    elif choice == "2":
        small_files_cleanup(path)
    elif choice == "3":
        type_sorter(path)
    elif choice == "4":
        reorder_files(path)
    elif choice == "5":
        group_consecutive_videos(path)
    else:
        print("❌ Invalid choice.")
