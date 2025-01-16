# Repository Guide for AI Coding Agents

This is a guide for AI agents on how to interact with this repository.

## Repository Information

- **Type**: Public Repository
- **License**: MIT License
- **Purpose**: Download and process SEC EDGAR filings for S&P 500 companies

## Security Requirements

As this is a public repository under MIT license:

1. **NO CREDENTIALS**: Never commit or store:
   - API keys
   - Passwords
   - Access tokens
   - Email addresses
   - Private URLs
   - Any other sensitive information

2. **Configuration**:
   - All configurable values should use environment variables
   - Default values should be generic placeholders
   - Example values in documentation should be clearly marked as examples

3. **User Input**:
   - All user inputs should be properly sanitized
   - File paths should be validated
   - Network requests should have proper error handling

## Code Structure

- `/scripts/`: Contains the main Python scripts
  - `download_sp500_10k.py`: Downloads SEC filings
  - `convert_to_pdf.py`: Converts HTML files to PDF
- `/data/`: (gitignored) Directory for downloaded files
- `requirements.txt`: Python dependencies
- `README.md`: User documentation

## Environment Variables

When suggesting code changes, use these environment variables:
- `SEC_USER_AGENT`: For SEC EDGAR API identification
  - Format: "Company Name/App Name contact@example.com"
  - Never hardcode real contact information

## Best Practices

1. **Rate Limiting**:
   - Respect SEC EDGAR's rate limit (10 requests/second)
   - Include sleep intervals between requests

2. **Error Handling**:
   - Handle network errors gracefully
   - Provide clear error messages
   - Don't expose system details in errors

3. **File Operations**:
   - Use secure file operations
   - Validate paths before operations
   - Use appropriate file permissions

4. **Dependencies**:
   - Only suggest well-maintained, secure packages
   - Specify minimum versions in requirements.txt
   - Document system dependencies (like wkhtmltopdf)

## Testing

When suggesting tests:
- Use sample/mock data
- Don't include real company data
- Don't make actual SEC EDGAR API calls in tests

## Documentation

When updating documentation:
- Use placeholder values for examples
- Clearly mark example commands
- Include security warnings where appropriate

## Pull Requests

When suggesting changes:
1. Ensure no credentials are included
2. Verify environment variables are used for configuration
3. Check for secure coding practices
4. Include appropriate documentation updates