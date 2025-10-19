import os
import shutil

def make_folder(path):
    """Create folder if not exists."""
    os.makedirs(path, exist_ok=True)

def extract_files(src_folder, dest_folder):
    """Extract all files from subfolders and move them into destination."""
    make_folder(dest_folder)
    moved_count = 0

    for root, dirs, files in os.walk(src_folder):
        for file in files:
            src_path = os.path.join(root, file)
            # Skip the script itself
            if os.path.abspath(src_path) == os.path.abspath(__file__):
                continue
            try:
                dest_path = os.path.join(dest_folder, file)
                # Avoid overwriting duplicate names
                if os.path.exists(dest_path):
                    base, ext = os.path.splitext(file)
                    i = 1
                    while os.path.exists(dest_path):
                        dest_path = os.path.join(dest_folder, f"{base}_{i}{ext}")
                        i += 1
                shutil.move(src_path, dest_path)
                print(f"📦 Moved: {file}")
                moved_count += 1
            except Exception as e:
                print(f"❌ Failed to move {file}: {e}")

    print(f"\n✅ Done! Extracted {moved_count} files to '{dest_folder}'.")

if __name__ == "__main__":
    print("📁 Extract Files from Subfolders")
    src = input("Enter source folder path: ").strip()
    dest = input("Enter destination folder path: ").strip()

    if not os.path.exists(src):
        print("❌ Source folder does not exist!")
    else:
        extract_files(src, dest)
