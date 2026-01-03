import argparse
import os
import shutil
import re
from collections import defaultdict

def organize_files_by_prefix(exclude_dirs=None):
    if exclude_dirs is None:
        exclude_dirs = []
    
    # Get the current working directory
    current_dir = os.getcwd()
    
    # Dictionary to keep track of files by prefix
    prefix_files = defaultdict(list)
    
    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(current_dir):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in exclude_dirs]
        
        for file in files:
            # Extract the prefix (assuming prefix ends at the first '-' or '_')
            match = re.split('[-_]', file, 1)
            prefix = match[0] if match else file
            
            # Add file to the prefix_files dictionary
            prefix_files[prefix].append(os.path.join(root, file))
    
    # Create the "Stand-Alone" directory if it doesn't exist
    stand_alone_dir = os.path.join(current_dir, "Stand-Alone")
    if not os.path.exists(stand_alone_dir):
        os.makedirs(stand_alone_dir)
    
    # Move files to their respective directories
    for prefix, files in prefix_files.items():
        if len(files) == 1:
            # Move to "Stand-Alone" directory
            dest_dir = stand_alone_dir
        else:
            # Create a directory named after the prefix if it doesn't exist
            dest_dir = os.path.join(current_dir, prefix)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
        
        for file in files:
            dest_path = os.path.join(dest_dir, os.path.basename(file))
            shutil.move(file, dest_path)
def main():
    parser = argparse.ArgumentParser(description='Organize files by prefix.')
    parser.add_argument('-e', '--exclude', nargs='*', default=[], 
                        help='Directories to exclude from processing')
    args = parser.parse_args()
    
    exclude_dirs = [os.path.abspath(d) for d in args.exclude]
    organize_files_by_prefix(exclude_dirs)
if __name__ == "__main__":
    main()