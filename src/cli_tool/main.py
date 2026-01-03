import typer
from concatenate import Concatenate_all_Markdown, Concatenate_all_mkv
from convert import pdf_converter, wav_to_flac
from deleter import emptyfolder_deleter, macosx_folder_deleter
from duplicate import duplicate_deleter, extenstion_sorter, prefix_matcher
from extract import pdf_link_extractor, href_parser
from pathlib import Path
import os
from rich import print

app = typer.Typer()


@app.command()
def sort_by_extension(
    extension: str = typer.Argument(
        ..., help="File extension to search for (e.g., txt, jpg, .txt, .jpg)"
    ),
    source: Path = typer.Option(
        os.getcwd(),
        help="Source directory to search for files (default: current working directory)",
    ),
    destination: Path = typer.Option(
        os.path.join(os.getcwd(), "Sorted-Files"),
        help="Destination directory to move files to (default: ./Sorted-Files)",
    ),
):
    """Move files with a specific extension to a destination directory."""
    if not extension.startswith("."):
        extension = "." + extension

    print(f"Searching for files with extension '{extension}'")
    print(f"Source directory: {source}")
    print(f"Destination directory: {destination}")

    extenstion_sorter.move_files(source, destination, extension)


@app.command()
def organize_by_prefix(
    directory: Path = typer.Argument(
        ..., help="Directory containing files to organize by prefix."
    ),
    exclude_dirs: list[str] = typer.Option(
        None, help="List of directories to exclude from processing."
    ),
):
    """Organize files in a directory based on their prefixes."""

    exclude_dirs = [os.path.abspath(d) for d in exclude_dirs] if exclude_dirs else []
    prefix_matcher.organize_files_by_prefix(directory, exclude_dirs)


@app.command()
def concat_md(
    directory: Path = typer.Argument(
        ..., help="Directory containing markdown files to concatenate."
    ),
    ignore_tags: bool = typer.Option(False, help="Ignore lines with tags."),
    include_filenames: bool = typer.Option(True, help="Include filenames as headers."),
    use_relative_path: bool = typer.Option(
        False, help="Use relative paths for filenames."
    ),
    char_limit: int = typer.Option(None, help="Character limit for each output file."),
):
    """Concatenate all markdown files in a directory."""
    Concatenate_all_Markdown.concatenate_markdown_files(
        directory, ignore_tags, include_filenames, use_relative_path, char_limit
    )
    print("Done concatenating markdown files.")


@app.command()
def concat_mkv(
    directory: Path = typer.Argument(
        ..., help="Directory containing MKV files to concatenate."
    ),
    output_filename: str = typer.Option(
        None, help="Optional name of the output concatenated MKV file."
    ),
):
    """Concatenate all MKV files in a directory."""
    Concatenate_all_mkv.main(directory, output_filename)
    print("Done concatenating MKV files.")


@app.command()
def convert_pdfs(
    directory: Path = typer.Argument(
        ..., help="Directory containing PPT/DOC files to convert."
    ),
    doc_dir: Path = typer.Option(
        None, help="Directory to move DOC files after conversion."
    ),
    ppt_dir: Path = typer.Option(
        None, help="Directory to move PPT files after conversion."
    ),
):
    """Convert PPT and DOC files to PDF in the specified directory."""
    current_directory = directory
    if not ppt_dir:
        ppt_dir = os.path.join(current_directory, "PPT")
    if not doc_dir:
        doc_dir = os.path.join(current_directory, "DOC")
    file_list = []

    for root, dirs, files in os.walk(current_directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)

    pdf_converter.process_files(file_list, ppt_dir, doc_dir)
    print("Done converting files to PDF.")


@app.command()
def empty_folder(
    directory: Path = typer.Argument(
        ..., help="Directory to search for empty folders."
    ),
):
    """Move empty folders in the specified directory to an 'empty' subdirectory."""
    emptyfolder_deleter.move_empty_directories(directory)
    print("Done moving empty folders.")


@app.command()
def convert_wav_to_flac(
    directory: Path = typer.Argument(
        ..., help="Directory containing WAV files to convert."
    ),
    overwrite: bool = typer.Option(
        False, help="Overwrite existing FLAC files if they exist."
    ),
):
    """Convert all WAV files in the specified directory to FLAC format."""
    wav_to_flac.convert_all_wav_in_directory(directory, overwrite)
    print("Done converting WAV to FLAC.")


@app.command()
def delete_macosx_folders(
    directory: Path = typer.Argument(
        ..., help="Directory to search for __MACOSX folders."
    ),
):
    """Delete all __MACOSX folders in the specified directory and its subdirectories"""
    macosx_folder_deleter.delete_macosx_folders(directory)
    print("Done deleting __MACOSX folders.")


@app.command()
def delete_duplicate_files(
    directory: Path = typer.Argument(
        ..., help="Directory to search for duplicate files."
    ),
):
    """Delete duplicate files in the specified directory based on the chosen method."""
    duplicates = duplicate_deleter.find_duplicates(directory)
    duplicate_deleter.move_duplicates_to_delete(duplicates)
    print("Done processing duplicates.")


@app.command()
def extract_pdf_links(
    pdf_path: Path = typer.Argument(..., help="Input PDF file path"),
    output_path: Path = typer.Argument(None, help="Optional Output text file path"),
):
    links = pdf_link_extractor.extract_links_from_pdf(pdf_path)
    if output_path:
        with open(output_path, "w") as f:
            for link in links:
                f.write(link + "\n")
    else:
        for link in links:
            print(link)
    print(f"Successfully extracted {len(links)} links to {output_path}")


@app.command()
def parse_href(
    html_file: Path = typer.Argument(..., help="Input HTML file path"),
    output_path: Path = typer.Argument(None, help="Optional Output text file path"),
    prefix: str = typer.Option(
        "https://", help="URL prefix to filter hrefs (default: https://)"
    ),
):
    """Extract href links from an HTML file."""

    try:
        hrefs = href_parser.extract_hrefs(html_file, prefix)
        href_parser.save_hrefs_to_file(hrefs, output_path)
        print(f"Successfully extracted {len(hrefs)} hrefs to {output_path}")
        print(f"Filtered for hrefs starting with: {prefix}")
    except FileNotFoundError:
        print(f"Error: Input file '{html_file}' not found.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    app()
