import os
import glob
import re
import argparse

def concatenate_markdown_files(directory, ignore_tags=False, include_filenames=True, use_relative_path=False, char_limit=None):
    """
    Concatenates all markdown files in the specified directory into one or more files based on character limit.

    Parameters:
    directory (str): The directory to search for markdown files.
    ignore_tags (bool): Whether to ignore lines with tags.
    include_filenames (bool): Whether to include filenames as headers.
    use_relative_path (bool): Whether to use relative paths for filenames.
    char_limit (int): The character limit for each output file.
    """
    try:
        # Find all markdown files in the directory and subdirectories
        markdown_files = glob.glob(os.path.join(directory, '**', '*.md'), recursive=True)
        
        current_char_count = 0
        file_index = 1
        outfile = open(f'concatenated_{file_index}.md', 'w', encoding='utf-8')
        
        for md_file in markdown_files:
            with open(md_file, 'r', encoding='utf-8') as infile:
                file_content = infile.read()
                if ignore_tags:
                    # Remove the entire block of lines between `---` markers
                    file_content = re.sub(r'---\n.*?\n---\n', '', file_content, flags=re.DOTALL)                
                if not file_content.strip():
                    # Skip empty files
                    continue
                file_length = len(file_content)
                
                if char_limit and current_char_count + file_length > char_limit:
                    outfile.close()
                    file_index += 1
                    current_char_count = 0
                    outfile = open(f'concatenated_{file_index}.md', 'w', encoding='utf-8')
                
                if include_filenames:
                    if use_relative_path:
                        filename = os.path.relpath(md_file, directory).replace(os.sep, '\\\\')
                    else:
                        filename = os.path.basename(md_file)
                    header = f'# Filename = {filename}\n\n'
                    outfile.write(header)
                    current_char_count += len(header)
                
                outfile.write(file_content)
                outfile.write('\n\n')  # Add a newline between files for separation
                current_char_count += file_length + 2  # +2 for the newlines

        outfile.close()
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Concatenate all markdown files in a directory.')
    parser.add_argument('directory', type=str, help='The directory to search for markdown files.')
    parser.add_argument('--ignore-tags', action='store_true', help='Ignore lines with tags.')
    parser.add_argument('--include-filenames', action='store_true', help='Include filenames as headers.')
    parser.add_argument('--use-relative-path', action='store_true', help='Use relative paths for filenames.')
    parser.add_argument('--char-limit', type=int, help='Character limit for each output file.')
    
    args = parser.parse_args()
    
    concatenate_markdown_files(args.directory, args.ignore_tags, args.include_filenames, args.use_relative_path, args.char_limit)

if __name__ == '__main__':
    main()