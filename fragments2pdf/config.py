import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Airtable Configuration
    AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
    AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
    AIRTABLE_TABLE_ID = os.getenv('AIRTABLE_TABLE_ID')

    # PDF Configuration
    PAGE_SIZE = (148, 210)  # A5 size in mm
    MARGIN = 10  # mm
    
    # Font Configuration
    TITLE_FONT_SIZE = 14
    SEQUENCE_FONT_SIZE = 14
    CONTENT_FONT_SIZE = 12
    ATTRIBUTE_FONT_SIZE = 10
    COMMENT_FONT_SIZE = 10

    # Layout Configuration
    TITLE_POSITION = (MARGIN, PAGE_SIZE[1] - MARGIN)  # Top-left
    SEQUENCE_POSITION = (PAGE_SIZE[0] - MARGIN, PAGE_SIZE[1] - MARGIN)  # Top-right
    CONTENT_AREA = (
        MARGIN,  # Left
        MARGIN,  # Bottom
        PAGE_SIZE[0] - 2 * MARGIN,  # Width
        PAGE_SIZE[1] - 4 * MARGIN  # Height
    )
    ATTRIBUTE_AREA = (
        PAGE_SIZE[0] - 2 * MARGIN,  # Right margin
        PAGE_SIZE[1] - 4 * MARGIN,  # Below sequence
        MARGIN,  # Width
        PAGE_SIZE[1] - 6 * MARGIN  # Height
    )
    COMMENT_POSITION = (PAGE_SIZE[0] - MARGIN, MARGIN)  # Bottom-right

    # Field Names (Airtable column names)
    FIELD_TITLE = 'Название'
    FIELD_SEQUENCE = 'Порядковый номер'
    FIELD_ATTRIBUTE1 = 'Атрибут 1'
    FIELD_CONTENT = 'Фрагмент'
    FIELD_COMMENTS = 'Comments'

    @classmethod
    def validate(cls):
        """Validate that all required configuration is present."""
        required_vars = [
            'AIRTABLE_API_KEY',
            'AIRTABLE_BASE_ID',
            'AIRTABLE_TABLE_ID'
        ]
        
        missing = [var for var in required_vars if not getattr(cls, var)]
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
