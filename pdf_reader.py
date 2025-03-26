import sys
import os

# import required modules
from pathlib import Path
from pypdf import PdfReader

# Check if the filename argument is provided
if len(sys.argv) < 2:
    print("Usage: ./batch_pdf_extract.py <directory_with_pdfs>")
    sys.exit(1)

input_dir = Path(sys.argv[1])

if not input_dir.exists() or not input_dir.is_dir():
    print(f"Error: {input_dir} is not a valid directory.")
    sys.exit(1)

for pdf_file in input_dir.glob("*.pdf"):
    try:
        print(f"Processing: {pdf_file.name}")
        reader = PdfReader(pdf_file)
        output_text = ""

        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                output_text += text + "\n\n"
            else:
                output_text += f"[Page {i+1}: No extractable text]\n\n"

        txt_filename = pdf_file.with_suffix(".txt")
        with open(txt_filename, "w", encoding="utf-8") as f_out:
            f_out.write(output_text)

        print(f"Saved to: {txt_filename.name}")

    except Exception as e:
        print(f"Error processing {pdf_file.name}: {e}")
