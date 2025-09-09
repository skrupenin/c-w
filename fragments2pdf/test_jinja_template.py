import json
import os
from pdf_generator import PDFGenerator

def main():
    # Initialize PDF generator
    pdf_generator = PDFGenerator()
    
    # Read the processed records
    input_file = 'output/records_processed.json'
    output_pdf = 'output/generated.pdf'
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            records = json.load(f)
            
        # Generate PDF
        success = pdf_generator.generate_pdf(records, output_pdf)
        
        if success:
            print(f"PDF generated successfully at: {output_pdf}")
        else:
            print("Failed to generate PDF")
            
    except FileNotFoundError:
        print(f"Error: Could not find input file {input_file}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {input_file}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 