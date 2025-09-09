# Airtable to PDF Converter

A Python application that extracts data from an Airtable database and generates a single PDF document with all records. Each record is presented on its own A5 page with specific formatting and layout requirements. The application uses Jinja2 templates and xhtml2pdf for PDF generation.

## Setup

1. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Unix/macOS
   # or
   .\venv\Scripts\activate  # On Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   Create a `.env` file in the project root with the following variables:
   ```
   AIRTABLE_API_KEY=your_api_key
   AIRTABLE_BASE_ID=your_base_id
   AIRTABLE_TABLE_ID=your_table_id
   ```

## Usage

Run the application:
```bash
python main.py
```

This will:
- Connect to Airtable and fetch records
- Generate a PDF file named `fragments.pdf` in the `output` directory
- Display progress and any errors

## Project Structure

- `fragment.html.j2` - Jinja2 template with embedded CSS for PDF layout
- `config.py` - Configuration settings
- `main.py` - Entry point
- `airtable_client.py` - Airtable API interactions
- `pdf_generator.py` - PDF generation using xhtml2pdf
- `requirements.txt` - Project dependencies

## Features

- A5 page size (148mm × 210mm)
- Proper positioning of elements:
  - Title (top-left)
  - Sequence number (top-right)
  - Content (main area)
  - Attributes (right margin)
  - Comments count (bottom-right)
- Support for Cyrillic characters
- Automatic page breaks
- Print-optimized layout

## Requirements

- Python 3.7+
- Airtable API key
- Required Python packages:
  - pyairtable
  - python-dotenv
  - jinja2
  - xhtml2pdf
  - pdfminer.six

## Troubleshooting

- **Missing API Key**: Ensure your `.env` file contains the correct Airtable API key
- **Network Issues**: Check your internet connection and Airtable API status
- **PDF Generation Errors**: Verify that the required fonts are available on your system
- **Template Issues**: Check that `fragment.html.j2` is in the correct location
