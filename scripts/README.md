# SEC Filing Downloader

Scripts to download and process SEC EDGAR filings (10-K reports) for S&P 500 companies.

## Requirements

- Python 3.7+
- Required Python packages (install via `pip install -r requirements.txt`):
  - pandas
  - requests
  - tqdm
- wkhtmltopdf (for PDF conversion)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install wkhtmltopdf:
- Ubuntu/Debian: `sudo apt-get install wkhtmltopdf`
- macOS: `brew install wkhtmltopdf`
- Windows: Download from https://wkhtmltopdf.org/downloads.html

3. Set up environment variables:
```bash
# Required by SEC EDGAR - identify your application
export SEC_USER_AGENT="Company Name/App Name contact@example.com"
```

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