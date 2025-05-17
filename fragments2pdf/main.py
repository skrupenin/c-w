from airtable_client import AirtableClient
from pdf_generator import PDFGenerator
from text_formatter import TextFormatter
import os

class ProcessResult:
    def __init__(self, success, pdf_path=None, record_count=0, error=None):
        self.success = success
        self.pdf_path = pdf_path
        self.record_count = record_count
        self.error = error

def process_airtable_to_pdf(output_path="output.pdf"):
    try:
        print("Connecting to Airtable...")
        client = AirtableClient()
        records = client.get_records()
        print(f"Fetched {len(records)} records.")

        print("Initializing PDF generator...")
        generator = PDFGenerator(output_path)
        generator.create_pdf()
        formatter = TextFormatter()

        for idx, record in enumerate(records, 1):
            print(f"Processing record {idx}/{len(records)}: {record['title']}")
            # Format content
            truncated_content = formatter.truncate(record['content'], max_length=2000)
            formatted_content = formatter.process(truncated_content)
            generator.create_page(
                title=record['title'],
                sequence=record['sequence'],
                attributes=record['attribute1'] if isinstance(record['attribute1'], list) else [record['attribute1']],
                content=truncated_content,
                formatted_content=formatted_content,
                comment_count=None  # Add comment count if available
            )
        generator.save()
        print(f"PDF generated: {output_path}")
        return ProcessResult(True, pdf_path=os.path.abspath(output_path), record_count=len(records))
    except Exception as e:
        print(f"Error: {e}")
        return ProcessResult(False, error=str(e))

if __name__ == "__main__":
    result = process_airtable_to_pdf()
    if result.success:
        print(f"Success! PDF saved at {result.pdf_path} ({result.record_count} records)")
    else:
        print(f"Failed: {result.error}")
