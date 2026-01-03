import os
import shutil

def move_empty_directories(root_dir):
    empty_dir = os.path.join(root_dir, 'empty')
    if not os.path.exists(empty_dir):
        os.makedirs(empty_dir)

    for subdir in os.listdir(root_dir):
        subdir_path = os.path.join(root_dir, subdir)
        if os.path.isdir(subdir_path) and not os.listdir(subdir_path):
            shutil.move(subdir_path, empty_dir)
            print(f"Moved empty directory: {subdir_path}")
def main():
    root_directory = os.getcwd()
    move_empty_directories(root_directory)
    print("Done moving empty directories.")
if __name__ == "__main__":
    main()