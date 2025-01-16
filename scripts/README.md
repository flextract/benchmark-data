# SEC Filing Downloader

Scripts to download and process SEC EDGAR filings (10-K reports) for S&P 500 companies.

## Requirements

- Python 3.7+
- Required Python packages (listed in requirements.txt)
- WeasyPrint (optional, for PDF conversion - installed via requirements.txt)

## Setup Instructions

1. Create and activate a virtual environment:
```bash
# On Unix/macOS
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# On Unix/macOS
export SEC_USER_AGENT="YourCompany YourApp (your.email@example.com)"

# On Windows (Command Prompt)
set SEC_USER_AGENT="YourCompany YourApp (your.email@example.com)"

# On Windows (PowerShell)
$env:SEC_USER_AGENT="YourCompany YourApp (your.email@example.com)"
```

4. (Optional) System dependencies for WeasyPrint:
- Ubuntu/Debian: `sudo apt-get install python3-cffi python3-brotli libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0`
- macOS: `brew install pango`
- Windows: No additional dependencies required

## Running the Scripts

1. Download SEC filings:
```bash
# This will download HTML and XBRL data for all S&P 500 companies
python download_sp500_10k.py
```

2. (Optional) Convert HTML filings to PDF:
```bash
# This will convert all downloaded HTML files to PDF format
python convert_to_pdf.py
```

## Directory Structure

After running the scripts, you'll have:
```
data/
  sec_filings/
    AAPL/
      10K_2024-01-01/
        filing.html      # Original SEC filing
        filing.pdf       # (Optional) Converted PDF
        xbrl_data.json   # Structured financial data
    MSFT/
      ...
```

## Notes

- The SEC requires a User-Agent header identifying your application
- The scripts respect SEC EDGAR's rate limits (max 10 requests per second)
- XBRL data contains structured financial information
- PDF conversion is optional and can be run separately
- Files are organized by company ticker and filing date

## Troubleshooting

1. Rate Limiting:
   - If you see HTTP 429 errors, the script will automatically retry
   - You can increase the sleep time between requests if needed

2. PDF Conversion:
   - If PDF conversion fails, verify wkhtmltopdf is installed correctly
   - Try running `wkhtmltopdf --version` to check installation

3. Missing Data:
   - Some companies might not have recent 10-K filings
   - The script will log any missing or failed downloads

## Usage

1. Download SEC filings:
```bash
python download_sp500_10k.py
```

2. Convert HTML filings to PDF:
```bash
python convert_to_pdf.py
```

The scripts will create a `data/sec_filings` directory with the following structure:
```
data/
  sec_filings/
    AAPL/
      10K_2024-01-01/
        filing.html
        filing.pdf
        xbrl_data.json
    MSFT/
      ...
```

## Notes

- The scripts respect SEC EDGAR's rate limits (max 10 requests per second)
- XBRL data contains structured financial information
- PDF conversion is optional and can be run separately
- Files are organized by company ticker and filing date