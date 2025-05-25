from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import sys
import base64

# Initialize client
client = genai.Client(api_key="AIzaSyDwFlz5ipw_QpHzTi1akcHrdy-HgM5wKfQ")

def read_text_from_file(filepath):
    """Read text content from a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def get_summary(text):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Give me a summary about:" + text,
    )
    return response

def get_qna(text):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Give me a list of frequent questions and answers about:" + text,
    )
    return response

def get_quiz(text):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Give me a multiple choice quiz that has similar answers and traps about:" + text,
    )
    return response

def gen_image(text):

    contents = ("Generate an image of a mind map or a timeline or a key term graph, choose whatever suits the best on the following text:" + text)

    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=contents,
        config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
        )
    )

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))
            image.save('gemini-native-image.png')
            image.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filepath>")
        print("Example: python script.py output/myfile.txt")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    with open(file_path,'r') as file:
        text = file.read()

    print(f"\nProcessing file: {file_path}")
    print("\nSelect processing mode:")
    print("1 - Summary")
    print("2 - Q&A")
    print("3 - Quiz")
    print("4 - Image Generation")
    mode = input("Enter mode number (1-4): ")
    
    if mode == 1:
        response = get_summary(text)
    elif mode == 2:
        response = get_qna(text)
    elif mode == 3:
        response = get_quiz(text)
    elif mode == 4:
        gen_image(text)
    
    if int(mode) <= 3:
        print(response)

