import os
from moviepy.editor import VideoFileClip
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import google.generativeai as genai

# Set your Gemini API Key here
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
genai.configure(api_key=GEMINI_API_KEY)

# === GEMINI FUNCTIONS ===
def ask_gemini(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text.strip()

def summarize_text(text):
    prompt = f"Summarize this text for a student:\n{text}"
    return ask_gemini(prompt)

def generate_quiz(text):
    prompt = f"""
    Based on this text, generate 3 multiple-choice questions.
    Each question should have 4 options and clearly indicate the correct answer.

    TEXT:
    {text}
    """
    return ask_gemini(prompt)

# === AUDIO FUNCTIONS ===
def convert_to_mp3(input_path):
    output_dir = "mp3-output"
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

    txt_path = os.path.splitext(mp3_path)[0] + ".txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(full_transcript)

    print(f"\nTranscription saved to: {txt_path}")
    return full_transcript

# === MAIN ===
if __name__ == "__main__":
    mp4_path = input("Enter the full path to the MP4 file: ").strip()
    if not os.path.isfile(mp4_path):
        print("MP4 file does not exist. Please check the path.")
        exit(1)

    watson_api_key = input("Enter your IBM Watson API Key: ").strip()
    watson_service_url = input("Enter your IBM Watson Service URL: ").strip()

    mp3_path = convert_to_mp3(mp4_path)
    if mp3_path:
        transcript = transcribe_with_watson(mp3_path, watson_api_key, watson_service_url)

        print("\n=== Gemini AI Summary ===")
        summary = summarize_text(transcript)
        print(summary)

        print("\n=== Gemini AI Quiz ===")
        quiz = generate_quiz(transcript)
        print(quiz)
