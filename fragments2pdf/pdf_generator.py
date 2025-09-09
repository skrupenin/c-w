import os
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
from config import Config

class PDFGenerator:
    def __init__(self):
        """Initialize the PDF generator with template environment."""
        self.env = Environment(loader=FileSystemLoader('.'))
        self.template = self.env.get_template('fragment.html.j2')

    def generate_pdf(self, records, output_path):
        """
        Generate PDF from records using the template.
        
        Args:
            records (list): List of records to include in the PDF
            output_path (str): Path where to save the PDF
            
        Returns:
            bool: True if PDF was generated successfully
        """
        try:
            # Render template with records
            html = self.template.render(records=records)
            # Save HTML to file for debugging
            html_debug_path = os.path.join(os.path.dirname(output_path), 'preview.html')
            with open(html_debug_path, 'w', encoding='utf-8') as f:
                f.write(html)

            # Open the HTML file in the default browser for preview on macOS
            os.system(f'open {html_debug_path}')
        
            return None

            # Convert HTML to PDF
            with open(output_path, 'wb') as output_file:
                pisa_status = pisa.CreatePDF(
                    html,
                    dest=output_file,
                    encoding='utf-8'
                )
            
            return pisa_status.err == 0
            
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return False
