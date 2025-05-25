import sys
from pypdf import PdfReader
from moviepy import VideoFileClip
import os
import json
from os.path import join, dirname, isfile, splitext, basename, abspath
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import sys
import base64

# Initialize IBM Watson STT service
authenticator = IAMAuthenticator('0n8PpNRA-R_6iym8Fl0tL3Jf7kywktSY7g2aZxTyFPDY')
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url('https://api.eu-de.speech-to-text.watson.cloud.ibm.com')

def pdf_extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    full_text = ""
    
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"
    
    return full_text

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

def transcribe_with_watson(mp3_path):
    if not os.path.isfile(mp3_path):
        print("MP3 file not found.")
        return None

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

    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create output filename based on MP3 name
    base_name = os.path.splitext(os.path.basename(mp3_path))[0]
    txt_path = os.path.join(output_dir, f"{base_name}.txt")
    
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(full_transcript)

    print(f"\nTranscription saved to: {txt_path}")
    return full_transcript

def save_text_to_file(text, output_dir="output", filename=None):
    """
    Save text to a .txt file in the specified output directory.
    
    Args:
        text (str): The text content to save
        output_dir (str): Directory where to save the file
        filename (str, optional): Name of the output file (without extension). 
            If None, uses the name of the calling script.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # If filename is not provided, use the name of the calling script
    if filename is None:
        base_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    else:
        base_name = filename
    
    output_path = os.path.join(output_dir, f"{base_name}.txt")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    return output_path

# PDF-specific helper function
def save_pdf_text_to_file(text, pdf_path, output_dir="output"):
    """
    Save text to a .txt file with the same name as the PDF file.
    
    Args:
        text (str): The text content to save
        pdf_path (str): Path to the PDF file
        output_dir (str): Directory where to save the file
    """
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    return save_text_to_file(text, output_dir=output_dir, filename=base_name)

client = genai.Client(api_key="AIzaSyDwFlz5ipw_QpHzTi1akcHrdy-HgM5wKfQ")

def get_summary(text):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Give me a summary about:" + text,
    )
    return extract_text_from_response(response)

def get_qna(text):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Give me 10 frequent questions and answers about:" + text,
    )
    return extract_text_from_response(response)

def get_quiz(text):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Give me a multiple choice quiz that has similar answers and traps about:" + text,
    )
    return extract_text_from_response(response)

def extract_text_from_response(response):
    """Extract text content from Gemini response"""
    if hasattr(response, 'candidates') and response.candidates:
        first_candidate = response.candidates[0]
        if hasattr(first_candidate, 'content') and hasattr(first_candidate.content, 'parts') and first_candidate.content.parts:
            first_part = first_candidate.content.parts[0]
            if hasattr(first_part, 'text'):
                return first_part.text
    return ""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/output/<path:filename>')
def serve_file(filename):
    try:
        return send_file(f'output/{filename}')
    except FileNotFoundError:
        return "File not found", 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)
    print("1. EXTRACT TEXT FROM PDF")
    print("2. TRANSCRIBE VIDEO")
    print("3. GENERATE OUTPUT")

    mode = input("Enter mode number (1-3): ")
    
    if mode == "1":
        pdf_path = input("Enter the full path to the PDF file: ").strip()
        text = pdf_extract_text(pdf_path)
        save_pdf_text_to_file(text, pdf_path)
    elif mode == "2":
        mp4_path = input("Enter the full path to the MP4 file: ").strip()
        mp3_path = convert_to_mp3(mp4_path)
        if mp3_path:
            transcribe_with_watson(mp3_path)
    elif mode == "3":
        txt_path = input("Enter the full path to the TXT file: ").strip()
        with open(txt_path, 'r') as file:
            text = file.read()
        print("\nSelect processing mode:")
        print("1 - Summary")
        print("2 - Q&A")
        print("3 - Quiz")
        mode = input("Enter mode number (1-3): ")
        
        mode = int(mode)
        response = None
        
        if mode == 1:
            response = get_summary(text)
        elif mode == 2:
            response = get_qna(text)
        elif mode == 3:
            response = get_quiz(text)
        
        if response:
            print("\nProcessing complete! Saving output...")
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            base_name = os.path.splitext(os.path.basename(txt_path))[0]
            output_path = os.path.join(output_dir, f"{base_name}_processed.txt")
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(str(response))
            print(f"\nOutput saved to: {output_path}")
    else:
        print("Invalid mode number.")