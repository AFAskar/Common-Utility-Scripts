import argparse
from bs4 import BeautifulSoup

def extract_hrefs(file_path, prefix='https://'):
    """Extract hrefs from HTML file that start with the specified prefix."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    hrefs = {a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith(prefix)}
    
    return hrefs

def save_hrefs_to_file(hrefs, output_file):
    """Save hrefs to a text file, one per line."""
    with open(output_file, 'w', encoding='utf-8') as file:
        for href in hrefs:
            file.write(f"{href}\n")

def main():
    parser = argparse.ArgumentParser(description='Extract href links from HTML files')
    parser.add_argument('input_file', help='Path to the input HTML file')
    parser.add_argument('-o', '--output', default='hrefs.txt', 
                       help='Output file for extracted hrefs (default: hrefs.txt)')
    parser.add_argument('-p', '--prefix', default='https://', 
                       help='URL prefix to filter hrefs (default: https://)')
    
    args = parser.parse_args()
    
    try:
        hrefs = extract_hrefs(args.input_file, args.prefix)
        save_hrefs_to_file(hrefs, args.output)
        print(f"Successfully extracted {len(hrefs)} hrefs to {args.output}")
        print(f"Filtered for hrefs starting with: {args.prefix}")
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()