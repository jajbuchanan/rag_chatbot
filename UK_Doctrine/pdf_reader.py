import sys
# import required modules
from pypdf import PdfReader

# Check if the filename argument is provided
if len(sys.argv) < 2: 
    print("Usage: pdf_reader.py <filename.pdf> [output.txt]")
    sys.exit(1)

# Get input and (optional) output filenames
input_pdf = sys.argv[1]
output_txt = sys.argv[2] if len(sys.argv) > 2 else input_pdf.rsplit(".", 1)[0] + ".txt"

# Read the PDF
reader = PdfReader(input_pdf)

with open(output_txt, "w", encoding="utf-8") as f_out: 
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text: 
            f_out.write(text)
            f_out.write("\n\n") # Add spacing between pages
        else: 
            f_out.write(f"[Page {i+1}: No extractable text]\n\n")

print(f"Extracted text written to: {output_txt}")
