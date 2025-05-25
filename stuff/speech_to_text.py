import json
import sys
import os
from os.path import join, dirname, isfile, splitext, basename, abspath
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Initialize IBM Watson STT service
authenticator = IAMAuthenticator('0n8PpNRA-R_6iym8Fl0tL3Jf7kywktSY7g2aZxTyFPDY')
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url('https://api.eu-de.speech-to-text.watson.cloud.ibm.com')

# Supported audio formats by IBM Watson STT
SUPPORTED_FORMATS = {
    '.flac': 'flac',
    '.wav': 'wav',
    '.ogg': 'ogg',
    '.oga': 'ogg',
    '.mp3': 'mp3',
    '.mpeg': 'mp3',
    '.webm': 'webm',
    '.opus': 'opus'
}

class MyRecognizeCallback(RecognizeCallback):
    def __init__(self, output_path=None):
        RecognizeCallback.__init__(self)
        self.output_path = output_path

    def on_data(self, data):
        print("Transcription completed successfully!")
        if self.output_path:
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            with open(self.output_path, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Results saved to {self.output_path}")
        print(json.dumps(data, indent=2))

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

def get_audio_format(file_path):
    """Extract and validate audio file format from filename"""
    _, ext = splitext(file_path)
    ext = ext.lower()
    
    if ext not in SUPPORTED_FORMATS:
        supported = ', '.join(SUPPORTED_FORMATS.keys())
        print(f"Error: Unsupported file format '{ext}'. Supported formats: {supported}")
        return None
    
    return SUPPORTED_FORMATS[ext]

def get_output_path(audio_path):
    """Generate output path for JSON file"""
    # Get the directory where the script is running
    script_dir = os.getcwd()
    output_dir = join(script_dir, 'output')
    
    # Create output filename based on audio file
    base_name = basename(audio_path)
    file_name, _ = splitext(base_name)
    
    return join(output_dir, f"{file_name}.json")

def transcribe_audio(audio_path):
    if not isfile(audio_path):
        print(f"Error: Audio file not found at {audio_path}")
        return

    content_type = get_audio_format(audio_path)
    if not content_type:
        return

    output_path = get_output_path(audio_path)
    
    try:
        with open(audio_path, 'rb') as audio_file:
            audio_source = AudioSource(audio_file)
            myRecognizeCallback = MyRecognizeCallback(output_path=output_path)
            
            print(f"Starting transcription for {audio_path} (format: {content_type})...")
            print(f"Results will be saved to: {output_path}")
            
            speech_to_text.recognize_using_websocket(
                audio=audio_source,
                content_type=f'audio/{content_type}',
                recognize_callback=myRecognizeCallback,
                model='en-US_BroadbandModel',
                keywords=['colorado', 'tornado', 'tornadoes'],
                keywords_threshold=0.5,
                max_alternatives=3)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <audio_file_path>")
        print("Example: python script.py audio.flac")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    transcribe_audio(audio_file)