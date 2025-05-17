from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5, landscape
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
import os

class PDFGenerator:
    def __init__(self, output_path="output.pdf"):
        self.output_path = output_path
        self.page_width, self.page_height = landscape(A5)
        self.margin = 10 * mm
        self._register_fonts()

    def _register_fonts(self):
        """Register fonts for both Latin and Cyrillic characters."""
        # Using DejaVuSans as it supports both Latin and Cyrillic
        font_path = os.path.join(os.path.dirname(__file__), "fonts", "DejaVuSans.ttf")
        if not os.path.exists(font_path):
            # Fallback to system font if custom font not found
            font_path = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
        pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))

    def create_pdf(self):
        """Create a new PDF document in landscape orientation."""
        self.canvas = canvas.Canvas(self.output_path, pagesize=landscape(A5))
        self.canvas.setTitle("Airtable Records")
        return self.canvas

    def create_page(self, title, sequence, attributes, content, comment_count=None, formatted_content=None):
        """Create a single page with all required elements."""
        # Set up the page
        self.canvas.setFont('DejaVuSans', 14)
        
        # Title (top-left)
        self.canvas.drawString(self.margin, self.page_height - self.margin, title)
        
        # Sequence number (top-right)
        sequence_text = str(sequence)
        sequence_width = self.canvas.stringWidth(sequence_text, 'DejaVuSans', 14)
        self.canvas.drawString(
            self.page_width - self.margin - sequence_width,
            self.page_height - self.margin,
            sequence_text
        )
        
        # Attributes (right margin, below sequence number)
        attr_y = self.page_height - 2 * self.margin
        for attr in attributes:
            self.canvas.drawString(
                self.page_width - self.margin - 30 * mm,
                attr_y,
                str(attr)
            )
            attr_y -= 5 * mm
        
        # Content area (wider due to landscape)
        content_y = self.page_height - 3 * self.margin
        if formatted_content is not None:
            self._draw_formatted_text(formatted_content, self.margin, content_y, self.page_width - 2 * self.margin)
        else:
            self.canvas.setFont('DejaVuSans', 12)
            self._draw_wrapped_text(content, self.margin, content_y, self.page_width - 2 * self.margin)
        
        # Comment count (bottom-right, if exists)
        if comment_count is not None:
            self.canvas.setFont('DejaVuSans', 10)
            comment_text = f"Comments: {comment_count}"
            comment_width = self.canvas.stringWidth(comment_text, 'DejaVuSans', 10)
            self.canvas.drawString(
                self.page_width - self.margin - comment_width,
                self.margin,
                comment_text
            )
        
        self.canvas.showPage()

    def _draw_wrapped_text(self, text, x, y, max_width):
        """Draw text with word wrapping."""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if self.canvas.stringWidth(test_line, 'DejaVuSans', 12) <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        for line in lines:
            if y < self.margin:
                # If we run out of space, add ellipsis and stop
                self.canvas.drawString(x, y, "...")
                break
            self.canvas.drawString(x, y, line)
            y -= 5 * mm

    def _draw_formatted_text(self, formatted_text, x, y, max_width):
        """Draw FormattedText (from TextFormatter) with support for bold, italic, underline, color, and line breaks."""
        font_name = 'DejaVuSans'
        font_size = 12
        line_height = 5 * mm
        cur_x = x
        cur_y = y
        for el in formatted_text.elements:
            if el.get('linebreak'):
                cur_x = x
                cur_y -= line_height
                continue
            style = {}
            if el.get('bold'):
                style['font'] = font_name
                style['size'] = font_size
                self.canvas.setFont(font_name, font_size)
            else:
                self.canvas.setFont(font_name, font_size)
            if el.get('color'):
                try:
                    self.canvas.setFillColor(colors.HexColor(el['color']))
                except Exception:
                    self.canvas.setFillColor(colors.black)
            else:
                self.canvas.setFillColor(colors.black)
            text = el['text']
            text_width = self.canvas.stringWidth(text, font_name, font_size)
            if cur_x + text_width > x + max_width:
                cur_x = x
                cur_y -= line_height
            self.canvas.drawString(cur_x, cur_y, text)
            # Underline
            if el.get('underline'):
                underline_y = cur_y - 1
                self.canvas.line(cur_x, underline_y, cur_x + text_width, underline_y)
            cur_x += text_width
        # If we run out of space, add ellipsis
        if cur_y < self.margin:
            self.canvas.drawString(x, self.margin, "...")

    def save(self):
        """Save the PDF document."""
        self.canvas.save()
