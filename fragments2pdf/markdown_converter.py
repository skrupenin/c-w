import markdown
# from markdown.extensions import fenced_code, tables, nl2br, sane_lists
from markdown.extensions import nl2br

class MarkdownConverter:
    def __init__(self):
        """Initialize the markdown converter with custom extensions."""
        self.md = markdown.Markdown(extensions=['nl2br'])
        """
            extensions=[
                'fenced_code',  # For code blocks
                'tables',       # For tables
                'nl2br',       # Convert newlines to <br>
                'sane_lists',  # Better list handling
                'attr_list',   # For adding attributes to elements
                'def_list',    # For definition lists
                'abbr',        # For abbreviations
                'footnotes',   # For footnotes
                'toc',         # For table of contents
                'meta',        # For metadata
                'smarty',      # For smart quotes and dashes
                'wikilinks',   # For wiki-style links
                'admonition',  # For admonitions
                'codehilite',  # For syntax highlighting
                'extra'        # Includes many common extensions
            ],
            output_format='html4'
        )
        """

    def convert(self, text: str) -> str:
        """
        Convert markdown text to HTML.
        
        Args:
            text (str): Markdown text to convert
            
        Returns:
            str: Converted HTML
        """
        if not text:
            return ""
        
        text = text.replace('----', '---\n')
        # Convert markdown to HTML
        html = self.md.convert(text)
        
        # Reset the converter for next use
        self.md.reset()
        
        return html

    def convert_record(self, record: dict) -> dict:
        """
        Convert markdown content in a record to HTML.
        
        Args:
            record (dict): Record containing markdown content
            
        Returns:
            dict: Record with HTML content
        """
        if 'content' in record:
            record['content_html'] = self.convert(record['content'])
        return record 