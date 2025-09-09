import os
import sys
import argparse
import json
from dotenv import load_dotenv
from airtable_client import AirtableClient
from pdf_generator import PDFGenerator
from markdown_converter import MarkdownConverter
from datetime import datetime
from tqdm import tqdm

def parse_fragment_ids(arg):
    try:
        return set(int(x) for x in arg.split(','))
    except ValueError:
        raise argparse.ArgumentTypeError("must be integers separated by commas.")

def parse_modified_since(arg):
    try:
        return datetime.fromisoformat(arg)
    except ValueError:
        raise argparse.ArgumentTypeError(f"must be in ISO format (YYYY-MM-DD): {arg}")


def process_airtable_to_pdf(fragment_ids=None, modified_since=None):
    """
    Main function to process Airtable records and generate a PDF.
    
    Args:
        fragment_ids (set, optional): Set of fragment IDs to process. If None, process all fragments.
        modified_since (datetime, optional): If provided, only process records modified on or after this date.
    
    Returns:
        dict: Processing results including success status and output path
    """
    try:
        # Load environment variables
        load_dotenv()
        
        # Initialize components
        airtable_client = AirtableClient()
        pdf_generator = PDFGenerator()
        markdown_converter = MarkdownConverter()
        
        # Fetch records from Airtable
        records = airtable_client.get_records(modified_since=modified_since, fragment_ids=fragment_ids)
        if not records:
            return {
                "success": False,
                "error": "No records found in Airtable" + 
                        (" for the specified date range" if modified_since else "") +
                        (" for the specified fragment IDs" if fragment_ids else "")
            }

        # Save records as pretty JSON
        output_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(output_dir, exist_ok=True)
        json_path = os.path.join(output_dir, "records_clean.json")
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False, default=str)

        # Process each record
        processed_records = []
        for record in tqdm(records, desc="Converting Markdown to HTML"):
            # Convert markdown content to HTML
            record = markdown_converter.convert_record(record)
            processed_records.append(record)
        
        # Save processed records as pretty JSON
        processed_json_path = os.path.join(output_dir, "records_processed.json")
        with open(processed_json_path, 'w', encoding='utf-8') as f:
            json.dump(processed_records, f, indent=2, ensure_ascii=False, default=str)

        # Generate PDF
        output_path = os.path.join(os.getcwd(), "output/fragments.pdf")
        pdf_generator.generate_pdf(processed_records, output_path)
        
        return {
            "success": True,
            "output_path": output_path,
            "record_count": len(processed_records)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate PDF from Airtable records',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process all records
  python main.py

  # Process records modified after a specific date
  python main.py --modified-since 2024-03-01

  # Process specific fragments
  python main.py --fragment-ids 123 456 789

  # Process specific fragments modified after a date
  python main.py --fragment-ids 123 456 789 --modified-since 2024-03-01
        """
    )
    
    parser.add_argument(
        '--fragment-ids',
        type=parse_fragment_ids,
        help='List of fragment IDs to process (space-separated numbers)'
    )
    
    parser.add_argument(
        '--modified-since',
        type=parse_modified_since,
        help='Process only records modified on or after this date (YYYY-MM-DD format)'
    )
    
    args = parser.parse_args()
    
    result = process_airtable_to_pdf(args.fragment_ids, args.modified_since)
    
    if result["success"]:
        print(f"Successfully generated PDF with {result['record_count']} records")
        print(f"Output saved to: {result['output_path']}")
    else:
        print(f"Error: {result['error']}")
