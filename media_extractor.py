import os
import shutil

def extract_media(src_folder, dest_folder):
    # Define supported extensions
    IMAGE_EXT = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    VIDEO_EXT = {'.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.webm'}
    AUDIO_EXT = {'.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a'}

    # Create destination subfolders
    images_dir = os.path.join(dest_folder, 'Images')
    videos_dir = os.path.join(dest_folder, 'Videos')
    audios_dir = os.path.join(dest_folder, 'Audios')

    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(videos_dir, exist_ok=True)
    os.makedirs(audios_dir, exist_ok=True)

    # Walk through all subdirectories
    for root, _, files in os.walk(src_folder):
        for file in files:
            file_path = os.path.join(root, file)
            _, ext = os.path.splitext(file)
            ext = ext.lower()

            # Check file type and copy to appropriate folder
            if ext in IMAGE_EXT:
                shutil.copy2(file_path, images_dir)
                print(f"📸 Copied image: {file}")
            elif ext in VIDEO_EXT:
                shutil.copy2(file_path, videos_dir)
                print(f"🎬 Copied video: {file}")
            elif ext in AUDIO_EXT:
                shutil.copy2(file_path, audios_dir)
                print(f"🎵 Copied audio: {file}")

    print("\n✅ Media extraction complete!")
    print(f"Images saved in: {images_dir}")
    print(f"Videos saved in: {videos_dir}")
    print(f"Audios saved in: {audios_dir}")

if __name__ == "__main__":
    print("📂 Media Extractor Script\n")

    src_folder = input("Enter the path to the SOURCE folder: ").strip('" ')
    dest_folder = input("Enter the path to the DESTINATION folder: ").strip('" ')

    # Validate folders
    if not os.path.isdir(src_folder):
        print("❌ Error: Source folder does not exist.")
    else:
        os.makedirs(dest_folder, exist_ok=True)
        extract_media(src_folder, dest_folder)
