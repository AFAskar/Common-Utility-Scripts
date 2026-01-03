import os
import hashlib
import shutil
import re
from collections import defaultdict

def calculate_file_hash(file_path):
    """Calculate the SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        # Read file in chunks to avoid high memory usage for large files
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicates(cwd):
    """Find duplicate files in the given directory and subdirectories."""
    file_hashes = defaultdict(list)

    # Walk through the directory
    for root, _, files in os.walk(cwd):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_hash = calculate_file_hash(file_path)
            file_hashes[file_hash].append(file_path)

    return file_hashes

def move_duplicates_to_delete(duplicates):
    """Move duplicates to the 'to-be-deleted' directory."""
    to_be_deleted_dir = os.path.join(os.getcwd(), 'to-be-deleted')
    
    # Create 'to-be-deleted' directory if it doesn't exist
    if not os.path.exists(to_be_deleted_dir):
        os.makedirs(to_be_deleted_dir)

    # Regex pattern to match 'duplicates_#'
    pattern = re.compile(r'duplicates_\d+')

    for file_hash, file_paths in duplicates.items():
        # Check for duplicates
        if len(file_paths) > 1:
            for path in file_paths:
                # Check if the file path contains 'duplicates_#'
                if pattern.search(path):
                    print(f"Moving {path} to {to_be_deleted_dir}")
                    shutil.move(path, to_be_deleted_dir)

def main():
    cwd = os.getcwd()  # Get the current working directory
    duplicates = find_duplicates(cwd)
    move_duplicates_to_delete(duplicates)
    print("Done processing duplicates.")

if __name__ == "__main__":
    main()
