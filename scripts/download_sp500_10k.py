import os
import json
import time
import requests
import pandas as pd
from datetime import datetime, timedelta

# Create directories for storing the data
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'sec_filings')
os.makedirs(BASE_DIR, exist_ok=True)

# SEC API configuration
# SEC requires a User-Agent header identifying your application
# Set SEC_USER_AGENT environment variable or use default
HEADERS = {
    "User-Agent": os.getenv('SEC_USER_AGENT', 'Company/App Name contact@example.com')
}

def get_sp500_companies():
    """Get list of S&P 500 companies using Wikipedia"""
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    df = tables[0]
    return df[['Symbol', 'Security', 'CIK']]

def get_company_filings(cik, ticker, company_name):
    """Get company filings from SEC EDGAR"""
    # Ensure CIK is 10 digits with leading zeros
    cik_padded = str(cik).zfill(10)
    
    # Create company directory
    company_dir = os.path.join(BASE_DIR, f"{ticker}")
    os.makedirs(company_dir, exist_ok=True)
    
    # Get company submissions
    url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        filings = response.json()
        
        # Get recent filings
        recent_filings = filings.get('filings', {}).get('recent', {})
        if not recent_filings:
            print(f"No recent filings found for {ticker}")
            return
        
        # Convert to DataFrame
        df = pd.DataFrame(recent_filings)
        
        # Filter for 10-K filings from the past year
        one_year_ago = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        mask = (df['form'] == '10-K') & (df['filingDate'] >= one_year_ago)
        recent_10k = df[mask]
        
        if recent_10k.empty:
            print(f"No 10-K filings in the past year for {ticker}")
            return
        
        # Download each 10-K filing
        for _, filing in recent_10k.iterrows():
            accession_number = filing['accessionNumber'].replace('-', '')
            primary_doc = filing['primaryDocument']
            
            # Create filing directory
            filing_dir = os.path.join(company_dir, f"10K_{filing['filingDate']}")
            os.makedirs(filing_dir, exist_ok=True)
            
            # Download HTML
            html_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number}/{primary_doc}"
            try:
                response = requests.get(html_url, headers=HEADERS)
                response.raise_for_status()
                html_path = os.path.join(filing_dir, 'filing.html')
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
            except Exception as e:
                print(f"Error downloading HTML for {ticker}: {e}")
            
            # Download XBRL data
            xbrl_url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_padded}.json"
            try:
                response = requests.get(xbrl_url, headers=HEADERS)
                response.raise_for_status()
                with open(os.path.join(filing_dir, 'xbrl_data.json'), 'w', encoding='utf-8') as f:
                    json.dump(response.json(), f, indent=2)
            except Exception as e:
                print(f"Error downloading XBRL for {ticker}: {e}")
            
            print(f"Downloaded 10-K filing for {ticker} dated {filing['filingDate']}")
            
            # Sleep to respect SEC rate limits (10 requests per second)
            time.sleep(0.1)
            
    except Exception as e:
        print(f"Error processing {ticker}: {e}")

def main():
    # Get all S&P 500 companies
    print("Getting S&P 500 companies list...")
    companies = get_sp500_companies()
    
    # Download filings for all companies
    total = len(companies)
    for idx, (_, company) in enumerate(companies.iterrows(), 1):
        print(f"\nProcessing {idx}/{total}: {company['Symbol']} - {company['Security']}")
        get_company_filings(company['CIK'], company['Symbol'], company['Security'])
        # Sleep between companies to respect SEC rate limits
        time.sleep(0.1)

if __name__ == "__main__":
    main()