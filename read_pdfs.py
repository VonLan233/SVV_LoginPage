import os
from pypdf import PdfReader

def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading {file_path}: {str(e)}"

pdf_files = [
    "Automated Defect Log.pdf",
    "Defect Log_Manual_Testing.pdf",
    "Automated Testing Report(3).pdf",
    "Manual Testing Report.pdf",
    "Testing Report.pdf"
]

for pdf_file in pdf_files:
    if os.path.exists(pdf_file):
        print(f"--- Start of {pdf_file} ---")
        print(extract_text_from_pdf(pdf_file))
        print(f"--- End of {pdf_file} ---\n")
    else:
        print(f"File not found: {pdf_file}")
