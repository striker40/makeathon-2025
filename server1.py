# server.py
from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from pdf_extraction import extract_text_from_pdf
from windows import convert_to_mp3, transcribe_with_watson
from text_output import get_summary, get_qna, get_quiz

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/process-text', methods=['POST'])
def process_text():
    file = request.files['file']
    mode = request.form.get('mode')
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    ext = os.path.splitext(filename)[1].lower()

    if ext == '.pdf':
        text = extract_text_from_pdf(path)
    elif ext in ['.mp4', '.avi', '.mov']:
        mp3_path = convert_to_mp3(path)
        text = transcribe_with_watson(mp3_path, os.getenv("WATSON_API_KEY"), os.getenv("WATSON_URL"))
    else:
        return jsonify({'error': 'Unsupported file type'}), 400

    if not text:
        return jsonify({'error': 'Failed to extract text'}), 500

    if mode == '1':
        result = get_summary(text)
    elif mode == '2':
        result = get_qna(text)
    elif mode == '3':
        result = get_quiz(text)
    else:
        return jsonify({'error': 'Invalid processing mode'}), 400

    return jsonify({'result': result.text if hasattr(result, 'text') else str(result)})

if __name__ == '__main__':
    app.run(debug=True)

#pip install flask werkzeug moviepy ibm-watson ibm-cloud-sdk-core google-generativeai pypdf
#Start the Flask backend: python server.py

#Start your React frontend: npm start

#Go to Home → upload files

#Go to Downloads → click "Get Summary", "Get QnA", or "Get Quizzes"

#You should see the result from Gemini via Flask!