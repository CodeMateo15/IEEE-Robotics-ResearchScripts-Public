import os
import re
import PyPDF2
from tqdm import tqdm

def extract_funding_sources_from_pdf(pdf_path):
    funding_sources = []
    funding_patterns = [
        r'\bNational Science Foundation\b',
        r'\bNSF\b',
        r'\bEuropean Research Council\b',
        r'\bERC\b',
        r'\bHorizon 2020\b',
        r'\bDARPA\b',
        r'\bDefense Advanced Research Projects Agency\b',
        r'\bNIH\b',
        r'\bNational Institutes of Health\b',
        r'\bONR\b',
        r'\bOffice of Naval Research\b',
        r'\bNASA\b',
        r'\bNational Aeronautics and Space Administration\b',
        r'\bDOE\b',
        r'\bDepartment of Energy\b',
        r'\bAFOSR\b',
        r'\bAir Force Office of Scientific Research\b',
        r'\bsupported by\b',
        r'\bfunded by\b',
        r'\bgrant from\b',
        r'\bcontract\b'
    ]
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = "".join([page.extract_text() or "" for page in reader.pages])
            
            # Extract matches for hardcoded patterns
            for pattern in funding_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                funding_sources.extend(matches)
            
            # Extract sentences with funding-related keywords
            funding_sentences = re.findall(
                r'([^.]*\b(supported by|funded by|grant from|contract)\b[^.]*\.)',
                text,
                re.IGNORECASE
            )
            funding_sources.extend([sentence[0].strip() for sentence in funding_sentences])
        
        return list(set(funding_sources)), None
    except Exception as e:
        return None, str(e)

def process_pdfs_for_funding_sources(root_folder):
    funding_data = []
    error_log = []
    pdf_files = []

    # Gather PDF files for progress bar
    for foldername, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith('.pdf'):
                pdf_files.append((foldername, filename))

    # Process files with progress bar
    for foldername, filename in tqdm(pdf_files, desc="Processing PDFs", unit="file"):
        pdf_path = os.path.join(foldername, filename)
        funding_sources, error = extract_funding_sources_from_pdf(pdf_path)
        
        if funding_sources:
            funding_data.append({
                "PDF Name": filename,
                "Folder": os.path.relpath(foldername, root_folder),
                "Funding Sources": funding_sources
            })
        elif error:
            error_log.append(f"{pdf_path} | Error: {error}")
    
    return funding_data, error_log

if __name__ == "__main__":
    PDF_FOLDER = r"C:\Users\mateo\..."  # Update as needed
    funding_results, errors = process_pdfs_for_funding_sources(PDF_FOLDER)
    
    for result in funding_results:
        print(f"PDF: {result['PDF Name']}")
        print(f"Folder: {result['Folder']}")
        print(f"Funding Sources: {', '.join(result['Funding Sources'])}")
        print("-" * 40)
    
    if errors:
        with open("funding_extraction_errors.log", "w") as f:
            f.write("\n".join(errors))
        print(f"Encountered {len(errors)} errors (see funding_extraction_errors.log)")
