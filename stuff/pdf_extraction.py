import sys
from pypdf import PdfReader

if len(sys.argv) != 2:
    print("Usage: python pdf_extraction.py <pdf_file>")
    sys.exit(1)

pdf_path = sys.argv[1]

try:
    reader = PdfReader(pdf_path)
    full_text = ""
    
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"
    
    print(full_text)
except Exception as e:
    print(f"Error processing PDF: {str(e)}", file=sys.stderr)
    sys.exit(1)
