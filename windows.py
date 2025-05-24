import os
from moviepy import VideoFileClip


def convert_to_mp3(input_path):
    # Define your custom output directory
    output_dir = r"C:\Users\smart\Downloads\Final Project P20119\makeathon-2025\mp3-output"
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
    input_path = input("Enter the full path to the MP4 file: ").strip()
    if not os.path.isfile(input_path):
        print("Error: The file does not exist. Please check the path and try again.")
    else:
        convert_to_mp3(input_path)
