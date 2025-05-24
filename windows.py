import os
from moviepy import VideoFileClip
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

#api_key = "0n8PpNRA-R_6iym8Fl0tL3Jf7kywktSY7g2aZxTyFPDY"
#service_url = "https://api.eu-de.speech-to-text.watson.cloud.ibm.com/instances/22f45bc5-f1f0-4d61-affe-5fbc5d800547"

def convert_to_mp3(input_path):
    output_dir = r"C:\Users\smart\Downloads\Final Project P20119\makeathon-2025\mp3-output"
    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f"{base_name}.mp3")

    try:
        print(f"Converting: {input_path} -> {output_path}")
        video = VideoFileClip(input_path)
        video.audio.write_audiofile(output_path)
        print("Conversion successful!")
        return output_path
    except Exception as e:
        print(f"Error during conversion: {e}")
        return None

def transcribe_with_watson(mp3_path, api_key, service_url):
    if not os.path.isfile(mp3_path):
        print("MP3 file not found.")
        return None

    authenticator = IAMAuthenticator(api_key)
    speech_to_text = SpeechToTextV1(authenticator=authenticator)
    speech_to_text.set_service_url(service_url)

    with open(mp3_path, 'rb') as audio_file:
        print(f"Transcribing {mp3_path} with IBM Watson...")
        result = speech_to_text.recognize(
            audio=audio_file,
            content_type='audio/mp3',
            model='en-US_BroadbandModel'
        ).get_result()

    transcripts = []
    results = result.get('results', [])
    for res in results:
        for alt in res.get('alternatives', []):
            transcripts.append(alt.get('transcript', ''))

    full_transcript = ' '.join(transcripts)

    print("\nTranscription result:\n")
    print(full_transcript)

    # Save transcription to a text file next to the mp3
    txt_path = os.path.splitext(mp3_path)[0] + ".txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(full_transcript)
    print(f"\nTranscription saved to: {txt_path}")

    return full_transcript

if __name__ == "__main__":
    mp4_path = input("Enter the full path to the MP4 file: ").strip()
    if not os.path.isfile(mp4_path):
        print("MP4 file does not exist. Please check the path.")
        exit(1)

    api_key = input("Enter your IBM Watson API Key: ").strip()
    service_url = input("Enter your IBM Watson Service URL: ").strip()

    mp3_path = convert_to_mp3(mp4_path)
    if mp3_path:
        transcribe_with_watson(mp3_path, api_key, service_url)
