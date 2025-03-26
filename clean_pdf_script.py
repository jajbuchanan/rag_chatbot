#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter


def clean_pdf(input_path: Path, output_path: Path):
    try:
        reader = PdfReader(str(input_path))
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        with open(output_path, "wb") as f_out:
            writer.write(f_out)

        print(f"Cleaned: {input_path.name} -> {output_path.name}")

    except Exception as e:
        print(f"Failed to clean {input_path.name}: {e}")


if len(sys.argv) < 2:
    print("Usage: ./clean_pdfs.py <directory_with_pdfs>")
    sys.exit(1)

input_dir = Path(sys.argv[1])
output_dir = input_dir / "cleaned"
output_dir.mkdir(exist_ok=True)

for pdf_file in input_dir.glob("*.pdf"):
    output_file = output_dir / pdf_file.name
    clean_pdf(pdf_file, output_file)
