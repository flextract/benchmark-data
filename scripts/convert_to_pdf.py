import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# Base directory where SEC filings are stored
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'sec_filings')

def convert_html_to_pdf(html_path):
    """Convert a single HTML file to PDF using wkhtmltopdf"""
    try:
        pdf_path = html_path.replace('.html', '.pdf')
        if os.path.exists(pdf_path):
            return False  # Skip if PDF already exists
            
        # Configure wkhtmltopdf options
        options = [
            'wkhtmltopdf',
            '--quiet',  # Reduce output
            '--enable-local-file-access',  # Allow loading local files
            '--encoding', 'UTF-8',  # Set encoding
            '--page-size', 'Letter',  # Use letter size
            '--margin-top', '20',  # Add margins
            '--margin-right', '20',
            '--margin-bottom', '20',
            '--margin-left', '20',
            '--footer-right', '[page]/[topage]',  # Add page numbers
            '--footer-font-size', '8',
            '--header-line',  # Add a line under the header
            '--header-spacing', '5',
            html_path,  # Input HTML file
            pdf_path   # Output PDF file
        ]
        
        # Run wkhtmltopdf
        result = subprocess.run(options, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Successfully converted {os.path.basename(html_path)}")
            return True
        else:
            print(f"Error converting {os.path.basename(html_path)}: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error processing {os.path.basename(html_path)}: {str(e)}")
        return False

def find_html_files():
    """Find all HTML files in the SEC filings directory"""
    html_files = []
    for root, _, files in os.walk(BASE_DIR):
        for file in files:
            if file == 'filing.html':
                html_files.append(os.path.join(root, file))
    return html_files

def check_wkhtmltopdf():
    """Check if wkhtmltopdf is installed"""
    try:
        subprocess.run(['wkhtmltopdf', '-V'], capture_output=True)
        return True
    except FileNotFoundError:
        print("Error: wkhtmltopdf is not installed.")
        print("Please install it using one of these methods:")
        print("  - Ubuntu/Debian: sudo apt-get install wkhtmltopdf")
        print("  - macOS: brew install wkhtmltopdf")
        print("  - Windows: Download from https://wkhtmltopdf.org/downloads.html")
        return False

def main():
    # First, make sure wkhtmltopdf is installed
    if not check_wkhtmltopdf():
        print("Exiting due to missing wkhtmltopdf.")
        return
    
    # Find all HTML files
    html_files = find_html_files()
    print(f"Found {len(html_files)} HTML files to convert")
    
    # Convert files using a thread pool
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(tqdm(
            executor.map(convert_html_to_pdf, html_files),
            total=len(html_files),
            desc="Converting to PDF"
        ))

if __name__ == "__main__":
    main()