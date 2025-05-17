import re
from typing import List, Dict, Any

class FormattedText:
    def __init__(self, elements: List[Dict[str, Any]]):
        self.elements = elements

    def get_bold_elements(self):
        return [el['text'] for el in self.elements if el.get('bold')]

    def get_italic_elements(self):
        return [el['text'] for el in self.elements if el.get('italic')]

    def get_underline_elements(self):
        return [el['text'] for el in self.elements if el.get('underline')]

    def get_colored_elements(self):
        return [el for el in self.elements if el.get('color')]

class TextFormatter:
    BOLD_PATTERN = re.compile(r'\*\*(.+?)\*\*')
    ITALIC_PATTERN = re.compile(r'_(.+?)_')
    UNDERLINE_PATTERN = re.compile(r'__(.+?)__')
    COLOR_PATTERN = re.compile(r'<color:(#[0-9A-Fa-f]{6}|[a-zA-Z]+)>(.+?)</color>')

    def process(self, text: str) -> FormattedText:
        elements = []
        idx = 0
        while idx < len(text):
            # Color
            color_match = self.COLOR_PATTERN.search(text, idx)
            if color_match and color_match.start() == idx:
                elements.append({
                    'text': color_match.group(2),
                    'color': color_match.group(1)
                })
                idx = color_match.end()
                continue
            # Bold
            bold_match = self.BOLD_PATTERN.search(text, idx)
            if bold_match and bold_match.start() == idx:
                elements.append({'text': bold_match.group(1), 'bold': True})
                idx = bold_match.end()
                continue
            # Underline
            underline_match = self.UNDERLINE_PATTERN.search(text, idx)
            if underline_match and underline_match.start() == idx:
                elements.append({'text': underline_match.group(1), 'underline': True})
                idx = underline_match.end()
                continue
            # Italic
            italic_match = self.ITALIC_PATTERN.search(text, idx)
            if italic_match and italic_match.start() == idx:
                elements.append({'text': italic_match.group(1), 'italic': True})
                idx = italic_match.end()
                continue
            # Line break
            if text[idx] == '\n':
                elements.append({'text': '\n', 'linebreak': True})
                idx += 1
                continue
            # Plain text
            next_special = min([
                m.start() for m in [
                    self.COLOR_PATTERN.search(text, idx),
                    self.BOLD_PATTERN.search(text, idx),
                    self.UNDERLINE_PATTERN.search(text, idx),
                    self.ITALIC_PATTERN.search(text, idx)
                ] if m] + [len(text)])
            if next_special > idx:
                elements.append({'text': text[idx:next_special]})
                idx = next_special
            else:
                # Fallback: add one char
                elements.append({'text': text[idx]})
                idx += 1
        return FormattedText(elements)

    def truncate(self, text: str, max_length: int) -> str:
        if len(text) <= max_length:
            return text
        truncated = text[:max_length].rstrip()
        return truncated + '...'
