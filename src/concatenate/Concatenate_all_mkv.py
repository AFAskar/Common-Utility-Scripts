import os
import ffmpeg
from pathlib import Path
from typing import Optional


def main(directory: str | Path, output_name: str | None = None) -> None:
    """
    Concatenates all MKV files in the given directory into a single MKV file.
    The output file is named based on the first MKV file's name, removing any numeric suffix.
    """
    mkv_files = [f for f in os.listdir(directory) if f.endswith(".mkv")]
    if not mkv_files:
        raise ValueError("No MKV files found in the specified directory.")

    if not output_name:
        # Get the base name for output from the first file (remove numeric suffix)
        output_name = Path(mkv_files[0]).stem.rsplit("-", 1)[0] + ".mkv"

    # Use ffmpeg-python to concatenate files
    input_files = [ffmpeg.input(os.path.join(directory, mkv)) for mkv in mkv_files]

    # Concatenate all mkv files and save the output
    ffmpeg.concat(*input_files, v=1, a=1).output(
        os.path.join(directory, output_name)
    ).run()

    print(f"Concatenation complete: {output_name}")


if __name__ == "__main__":
    main(".")
