import os
import ffmpeg


def main():
    """
    Concatenates all MKV files in the current directory into a single MKV file.
    The output file is named based on the first MKV file's name, removing any numeric suffix.
    """
    # Get all mkv files in the current directory
    mkv_files = [f for f in os.listdir() if f.endswith(".mkv")]

    # Get the base name for output from the first file (remove numeric suffix)
    output_name = mkv_files[0].rsplit("-", 1)[0] + ".mkv"

    # Use ffmpeg-python to concatenate files
    input_files = [ffmpeg.input(mkv) for mkv in mkv_files]

    # Concatenate all mkv files and save the output
    ffmpeg.concat(*input_files, v=1, a=1).output(output_name).run()

    print(f"Concatenation complete: {output_name}")


if __name__ == "__main__":
    main()
