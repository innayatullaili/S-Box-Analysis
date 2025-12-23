"""
PDF Text Extractor
Extracts text content from PDF file for analysis
"""

import sys
import os

def extract_with_pypdf2(pdf_path, output_path):
    """Extract text using PyPDF2"""
    try:
        import PyPDF2
        
        print(f"Reading PDF: {pdf_path}")
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            print(f"Total pages: {num_pages}")
            
            text_content = []
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                text_content.append(f"\n{'='*80}\n")
                text_content.append(f"PAGE {page_num + 1}\n")
                text_content.append(f"{'='*80}\n\n")
                text_content.append(text)
            
            # Save to file
            with open(output_path, 'w', encoding='utf-8') as out_file:
                out_file.write(''.join(text_content))
            
            print(f"✓ Text extracted successfully to: {output_path}")
            print(f"  Total characters: {len(''.join(text_content))}")
            return True
            
    except ImportError:
        print("PyPDF2 not installed. Install with: pip install PyPDF2")
        return False
    except Exception as e:
        print(f"Error with PyPDF2: {e}")
        return False

def extract_with_pdfplumber(pdf_path, output_path):
    """Extract text using pdfplumber (better quality)"""
    try:
        import pdfplumber
        
        print(f"Reading PDF with pdfplumber: {pdf_path}")
        text_content = []
        
        with pdfplumber.open(pdf_path) as pdf:
            num_pages = len(pdf.pages)
            print(f"Total pages: {num_pages}")
            
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    text_content.append(f"\n{'='*80}\n")
                    text_content.append(f"PAGE {page_num + 1}\n")
                    text_content.append(f"{'='*80}\n\n")
                    text_content.append(text)
        
        # Save to file
        with open(output_path, 'w', encoding='utf-8') as out_file:
            out_file.write(''.join(text_content))
        
        print(f"✓ Text extracted successfully to: {output_path}")
        print(f"  Total characters: {len(''.join(text_content))}")
        return True
        
    except ImportError:
        print("pdfplumber not installed. Install with: pip install pdfplumber")
        return False
    except Exception as e:
        print(f"Error with pdfplumber: {e}")
        return False

def main():
    # Path to PDF file
    pdf_file = "paper referensi sbox.pdf"
    output_file = "paper_extracted.txt"
    
    # Check if file exists
    if not os.path.exists(pdf_file):
        print(f"Error: File not found: {pdf_file}")
        return
    
    print("PDF Text Extractor")
    print("=" * 80)
    
    # Try pdfplumber first (better quality)
    print("\nAttempt 1: Using pdfplumber...")
    if extract_with_pdfplumber(pdf_file, output_file):
        return
    
    # Fallback to PyPDF2
    print("\nAttempt 2: Using PyPDF2...")
    if extract_with_pypdf2(pdf_file, output_file):
        return
    
    print("\n❌ Could not extract PDF. Please install one of these libraries:")
    print("   pip install pdfplumber")
    print("   pip install PyPDF2")

if __name__ == "__main__":
    main()
