import os
import re
import shutil

def make_folder(path):
    os.makedirs(path, exist_ok=True)

def group_consecutive_videos_smart(folder):
    video_ext = [".mp4", ".mkv", ".avi", ".mov", ".flv"]
    files = [f for f in os.listdir(folder) if os.path.splitext(f)[1].lower() in video_ext]

    num_map = {}

    # Extract numeric parts from filenames
    for f in files:
        nums = re.findall(r'\d+', f)  # find all numbers
        if nums:
            # choose the largest number (often the main ID)
            main_num = int(max(nums, key=int))
            num_map[f] = main_num

    if not num_map:
        print("⚠️ No numeric identifiers found in filenames.")
        return

    # Sort files by numeric ID
    sorted_items = sorted(num_map.items(), key=lambda x: x[1])

    # Group consecutive numbers
    groups = []
    current_group = [sorted_items[0]]

    for i in range(1, len(sorted_items)):
        prev_num = sorted_items[i-1][1]
        curr_num = sorted_items[i][1]

        if curr_num == prev_num + 1:
            current_group.append(sorted_items[i])
        else:
            groups.append(current_group)
            current_group = [sorted_items[i]]
    groups.append(current_group)

    # Create folders and move files
    for group in groups:
        if len(group) > 1:
            start = group[0][1]
            end = group[-1][1]
            folder_name = f"Group_{start}-{end}"
            full_path = os.path.join(folder, folder_name)
            make_folder(full_path)

            for filename, _ in group:
                src = os.path.join(folder, filename)
                dst = os.path.join(full_path, filename)
                try:
                    shutil.move(src, dst)
                except Exception as e:
                    print(f"❌ Failed to move {filename}: {e}")

    print("✅ Smart consecutive video grouping complete!")

# Example usage:
if __name__ == "__main__":
    path = input("Enter folder path: ").strip('"')
    if os.path.exists(path):
        group_consecutive_videos_smart(path)
    else:
        print("❌ Folder not found!")
