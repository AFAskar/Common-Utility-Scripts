import os
import shutil
import argparse
def delete_macosx_folders(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if '__MACOSX' in dirnames:
            macosx_path = os.path.join(dirpath, '__MACOSX')
            shutil.rmtree(macosx_path)
            print(f"Deleted: {macosx_path}")
def main():
    parser = argparse.ArgumentParser(description='Delete all __MACOSX folders in the specified directory and its subdirectories.')
    parser.add_argument('directory',
                        help='Root directory to start searching')

    args = parser.parse_args()
    
    root_directory = args.directory
    print(f"Starting to delete __MACOSX folders in: {root_directory}")
    delete_macosx_folders(root_directory)
    print("Done deleting __MACOSX folders.")
if __name__ == "__main__":
    main()