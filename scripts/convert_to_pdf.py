import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from weasyprint import HTML, CSS

# Base directory where SEC filings are stored
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'sec_filings')

def convert_html_to_pdf(html_path):
    """Convert a single HTML file to PDF using WeasyPrint"""
    try:
        pdf_path = html_path.replace('.html', '.pdf')
        if os.path.exists(pdf_path):
            return False  # Skip if PDF already exists

        # Read the HTML file
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Define custom CSS for better PDF formatting
        css = CSS(string='''
            @page {
                margin: 1cm;
                @bottom-right {
                    content: "Page " counter(page) " of " counter(pages);
                    font-size: 8pt;
                }
            }
            body {
                font-family: Arial, sans-serif;
                font-size: 10pt;
                line-height: 1.3;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 10px 0;
            }
            td, th {
                border: 1px solid #ddd;
                padding: 8px;
            }
            th {
                background-color: #f8f8f8;
            }
            pre {
                white-space: pre-wrap;
                font-size: 9pt;
            }
        ''')

        # Convert to PDF
        HTML(string=html_content).write_pdf(
            pdf_path,
            stylesheets=[css],
            presentational_hints=True
        )
        
        print(f"Successfully converted {os.path.basename(html_path)}")
        return True
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

def main():
    
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