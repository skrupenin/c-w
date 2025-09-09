import unittest
from markdown_converter import MarkdownConverter

class TestMarkdownConverter(unittest.TestCase):
    def setUp(self):
        self.converter = MarkdownConverter()

    def test_convert_empty_text(self):
        """Test converting empty text."""
        result = self.converter.convert("")
        self.assertEqual(result, "")

    def test_convert_basic_markdown(self):
        """Test converting basic markdown elements."""
        text = """
# Heading 1
## Heading 2

This is a paragraph with **bold** and *italic* text.

- List item 1
- List item 2

1. Numbered item 1
2. Numbered item 2

[Link text](http://example.com)
        """
        result = self.converter.convert(text)
        
        # Check for basic HTML elements
        self.assertIn("<h1>Heading 1</h1>", result)
        self.assertIn("<h2>Heading 2</h2>", result)
        self.assertIn("<strong>bold</strong>", result)
        self.assertIn("<em>italic</em>", result)
        self.assertIn("<ul>", result)
        self.assertIn("<ol>", result)
        self.assertIn('<a href="http://example.com">', result)

    def test_convert_code_blocks(self):
        """Test converting code blocks."""
        text = """
```python
def hello():
    print("Hello, world!")
```
        """
        result = self.converter.convert(text)
        self.assertIn("<pre><code class=\"language-python\">", result)
        self.assertIn("def hello():", result)

    def test_convert_tables(self):
        """Test converting markdown tables."""
        text = """
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
        """
        result = self.converter.convert(text)
        self.assertIn("<table>", result)
        self.assertIn("<th>Header 1</th>", result)
        self.assertIn("<td>Cell 1</td>", result)

    def test_convert_record(self):
        """Test converting markdown content in a record."""
        record = {
            "id": "1",
            "content": "# Title\nSome content"
        }
        result = self.converter.convert_record(record)
        
        self.assertEqual(result["id"], "1")
        self.assertIn("<h1>Title</h1>", result["content_html"])
        self.assertIn("Some content", result["content_html"])

    def test_convert_record_no_content(self):
        """Test converting a record without content field."""
        record = {"id": "1"}
        result = self.converter.convert_record(record)
        self.assertEqual(result, record)

if __name__ == '__main__':
    unittest.main() 