import os
import ffmpeg

# Get all mkv files in the current directory
mkv_files = [f for f in os.listdir() if f.endswith(".mkv")]

# Get the base name for output from the first file (remove numeric suffix)
output_name = mkv_files[0].rsplit("-", 1)[0] + ".mkv"

# Use ffmpeg-python to concatenate files
input_files = [ffmpeg.input(mkv) for mkv in mkv_files]

# Concatenate all mkv files and save the output
ffmpeg.concat(*input_files, v=1, a=1).output(output_name).run()

print(f"Concatenation complete: {output_name}")
