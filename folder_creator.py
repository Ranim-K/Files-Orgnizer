import os

def make_folder(path):
    """Create folder if not exists."""
    try:
        os.makedirs(path, exist_ok=True)
        print(f"✅ Folder created: {path}")
    except Exception as e:
        print(f"❌ Failed to create folder {path}: {e}")

if __name__ == "__main__":
    print("📁 Folder Creator")
    print("Type folder names one by one. Press Enter on empty input to exit.\n")

    base_path = input("Enter base folder path where folders will be created: ").strip()
    if not os.path.exists(base_path):
        print("❌ Base folder does not exist! Exiting...")
        exit()

    while True:
        folder_name = input("Enter folder name (or just Enter to finish): ").strip()
        if folder_name == "":
            print("🏁 Finished creating folders!")
            break
        folder_path = os.path.join(base_path, folder_name)
        make_folder(folder_path)
