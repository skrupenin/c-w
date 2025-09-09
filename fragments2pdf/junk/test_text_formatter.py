import unittest
from junk.text_formatter import TextFormatter

class TestTextFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = TextFormatter()

    def test_formatting_preservation(self):
        test_text = "**Bold** _Italic_ __Underline__ <color:#FF0000>Red</color>"
        formatted = self.formatter.process(test_text)
        self.assertIn("Bold", formatted.get_bold_elements())
        self.assertIn("Italic", formatted.get_italic_elements())
        self.assertIn("Underline", formatted.get_underline_elements())
        colored = formatted.get_colored_elements()
        self.assertTrue(any(el['text'] == "Red" and el['color'] == "#FF0000" for el in colored))

    def test_truncation(self):
        long_text = "Very long text..." * 100
        truncated = self.formatter.truncate(long_text, max_length=1000)
        self.assertLessEqual(len(truncated), 1003)  # 1000 + '...'
        self.assertTrue(truncated.endswith("..."))

    def test_cyrillic_support(self):
        cyrillic_text = "Привет, **мир**! _Тест_ __подчеркивание__ <color:blue>синий</color>"
        formatted = self.formatter.process(cyrillic_text)
        self.assertIn("мир", formatted.get_bold_elements())
        self.assertIn("Тест", formatted.get_italic_elements())
        self.assertIn("подчеркивание", formatted.get_underline_elements())
        colored = formatted.get_colored_elements()
        self.assertTrue(any(el['text'] == "синий" and el['color'] == "blue" for el in colored))

if __name__ == '__main__':
    unittest.main() 