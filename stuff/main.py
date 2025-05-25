import os
import sys
from moviepy import VideoFileClip

def convert_to_mp3(input_path):
    # Ensure output directory exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Extract filename without extension
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f"{base_name}.mp3")

    try:
        print(f"Converting: {input_path} -> {output_path}")
        video = VideoFileClip(input_path)
        video.audio.write_audiofile(output_path)
        print("Conversion successful!")
    except Exception as e:
        print(f"Error during conversion: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <path-to-mp4>")
    else:
        convert_to_mp3(sys.argv[1])

