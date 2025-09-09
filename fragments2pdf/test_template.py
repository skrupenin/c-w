import os
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
from markdown_converter import MarkdownConverter
from pdf_generator import PDFGenerator


def generate_test_output():
    """
    Generate test HTML and PDF output using sample data.
    """
    # Initialize components
    markdown_converter = MarkdownConverter()
    pdf_generator = PDFGenerator()
    
    # Sample test data
    test_records = [
        {
            'title': 'Test Fragment 1',
            'sequence': '001',
            'attribute1': ['Определение "креативность сотрудников на работе”', 'Полезная креативность на работе, примеры'],
            'content': """
Было предложение от наших Администраторов вместе с официантами они придумали вечер «Титаник», предложили сами. \\n\\nВообще никто не предлагал. Такого в Минске еще не было. Они предложили восстановить картину банкета на Титанике в момент его крушения. Нашли меню с Титаника, нашли музыку, которая играла. И провели здесь вот такой вот шоу вечер. Меню с Титаника что подавалось, под какую музыку было видео, которое сопровождало? Ну, понятно, что видео это было не историческое, а скорее больше из фильма Титаник. Но, тем не менее, люди просто визжали от удовольствия, аплодировали. Зал был продан за несколько часов полностью. Прекрасно сделано это было этим летом. Вообще никаких не было ни пожеланий, ни просьб. Что то это просто вот они это предложили сами сделали мы. Лично я об этом узнал на моменте рекламы в Instagram. Это то, что касается креативности со знаком плюс. То, что вышло в компании в плюс и принесло и прибыль, и имидж, и хорошие отзывы.            
Было предложение от наших Администраторов вместе с официантами они придумали вечер «Титаник», предложили сами. \\n\\nВообще никто не предлагал. Такого в Минске еще не было. Они предложили восстановить картину банкета на Титанике в момент его крушения. Нашли меню с Титаника, нашли музыку, которая играла. И провели здесь вот такой вот шоу вечер. Меню с Титаника что подавалось, под какую музыку было видео, которое сопровождало? Ну, понятно, что видео это было не историческое, а скорее больше из фильма Титаник. Но, тем не менее, люди просто визжали от удовольствия, аплодировали. Зал был продан за несколько часов полностью. Прекрасно сделано это было этим летом. Вообще никаких не было ни пожеланий, ни просьб. Что то это просто вот они это предложили сами сделали мы. Лично я об этом узнал на моменте рекламы в Instagram. Это то, что касается креативности со знаком плюс. То, что вышло в компании в плюс и принесло и прибыль, и имидж, и хорошие отзывы.            
""",
            'Comments': ['Comment 1', 'Comment 2']
        },
        {
            'title': 'Test Fragment 2',
            'sequence': '002',
            'attribute1': ['Tag3'],
            'content': """
# Another Fragment

This fragment contains a table:

| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
| Cell 3   | Cell 4   |

And some *formatted* text with **emphasis**.
            """,
            'Comments': []
        }
    ]
    
    # Process records with markdown conversion
    processed_records = []
    for record in test_records:
        processed_record = markdown_converter.convert_record(record)
        processed_records.append(processed_record)
    
    try:
        # Generate PDF
        output_path = os.path.join(os.getcwd(), "output/test_fragments.pdf")
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

if __name__ == '__main__':
    result = generate_test_output()
    
    if result['success']:
        print("✅ Test output generated successfully!")

    else:
        print("❌ Error generating test output") 