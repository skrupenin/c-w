# Airtable to PDF Converter

A Python application that extracts data from an Airtable database and generates a single PDF document with all records. Each record is presented on its own A5 page with specific formatting and layout requirements.

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
- Generate a PDF file named `output.pdf` in the project directory
- Display progress and any errors

## Troubleshooting

- **Missing API Key**: Ensure your `.env` file contains the correct Airtable API key.
- **Network Issues**: Check your internet connection and Airtable API status.
- **PDF Generation Errors**: Verify that the required fonts are available in the `fonts` directory or fallback to system fonts.

## Project Structure

- `config.py` - Configuration settings
- `main.py` - Entry point
- `airtable_client.py` - Airtable API interactions
- `pdf_generator.py` - PDF creation logic
- `text_formatter.py` - Text formatting handlers
- `requirements.txt` - Project dependencies

## Requirements

- Python 3.7+
- Airtable API key
- Required Python packages (see requirements.txt)
