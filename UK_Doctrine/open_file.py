from pdfminer.high_level import extract_text as extract_pdf_text

pdf_path = "UK_Defence_Doctrine_Ed6.pdf"
def extract_text(pdf_path):
    try: 
        text = extract_pdf_text(pdf_path)
        return text
    except Exception as e: 
        print(f\"Error extracting {pdf_path}: {e}\")
        return \"\"



