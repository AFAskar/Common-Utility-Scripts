import fitz  # PyMuPDF
import argparse

def extract_links_from_pdf(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    links = []

    # Iterate through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        link_dicts = page.get_links()
        
        # Extract the URI from each link
        for link in link_dicts:
            if 'uri' in link:
                links.append(link['uri'])

    return links
def main():
    parser = argparse.ArgumentParser(description="Extract links from a PDF file.")
    parser.add_argument('-i', '--input', required=True, help="Input PDF file path")
    parser.add_argument('-o', '--output', required=True, help="Output text file path")
    
    args = parser.parse_args()
    
    pdf_path = args.input
    output_path = args.output
    
    links = extract_links_from_pdf(pdf_path)
    
    # Write the extracted links to the output file
    with open(output_path, 'w') as f:
        for link in links:
            f.write(link + '\n')

if __name__ == "__main__":
    main()