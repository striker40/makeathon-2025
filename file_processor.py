from flask import Flask, request, jsonify
import subprocess
import os
import tempfile

app = Flask(__name__)

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'File must be PDF'}), 400
    
    try:
        # Save file to temporary location
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, file.filename)
        file.save(temp_path)
        
        # Process PDF
        current_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_dir, 'pdf_extraction.py')
        result = subprocess.run(['python3', script_path, temp_path], capture_output=True, text=True)
        
        # Clean up
        os.remove(temp_path)
        os.rmdir(temp_dir)
        
        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 500
            
        return jsonify({'result': result.stdout})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/process-text', methods=['POST'])
def process_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    mode = request.form.get('mode')
    if not mode or not mode.isdigit():
        return jsonify({'error': 'Invalid mode'}), 400
    
    try:
        # Save file to temporary location
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, file.filename)
        file.save(temp_path)
        
        # Process text
        current_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_dir, 'text_output.py')
        result = subprocess.run(['python3', script_path, temp_path, mode], capture_output=True, text=True)
        
        # Clean up
        os.remove(temp_path)
        os.rmdir(temp_dir)
        
        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 500
            
        return jsonify({'result': result.stdout})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
