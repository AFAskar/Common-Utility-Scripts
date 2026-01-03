import os
import shutil
import argparse

def move_files(source_dir, dest_dir, file_extension):
    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(source_dir):
        for filename in files:
            if os.path.abspath(root).startswith(os.path.abspath(dest_dir)):
                continue
            # Check if the file ends with the specified extension
            if filename.endswith(file_extension):
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                    
                source_file = os.path.join(root, filename)
                dest_file = os.path.join(dest_dir, filename)
                if os.path.exists(dest_file):
                    name, ext = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(dest_file):
                        dest_file = os.path.join(dest_dir, f'{name}({counter}){ext}')
                        counter += 1
                
                # Move the file
                shutil.move(source_file, dest_file)
                print(f'Moved: {source_file} to {dest_file}')

def main():
    parser = argparse.ArgumentParser(description='Move files with a specific extension to a destination directory.')
    parser.add_argument('extension', 
                        help='File extension to search for (e.g., txt, jpg, .txt, .jpg)')
    parser.add_argument('-s', '--source', 
                        default=os.getcwd(), 
                        help='Source directory to search for files (default: current working directory)')
    parser.add_argument('-d', '--destination', 
                        default=os.path.join(os.getcwd(), 'Sorted-Files'),
                        help='Destination directory to move files to (default: ./Sorted-Files)')
    
    args = parser.parse_args()
    
    # Ensure the extension starts with a dot
    if not args.extension.startswith('.'):
        args.extension = '.' + args.extension
    
    print(f"Searching for files with extension '{args.extension}'")
    print(f"Source directory: {args.source}")
    print(f"Destination directory: {args.destination}")
    
    move_files(args.source, args.destination, args.extension)


if __name__ == '__main__':
    main()