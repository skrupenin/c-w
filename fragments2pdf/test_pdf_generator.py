import unittest
import os
from pdf_generator import PDFGenerator
from reportlab.lib.pagesizes import A5, landscape

class TestPDFGenerator(unittest.TestCase):
    def setUp(self):
        self.test_output = "test_output.pdf"
        self.generator = PDFGenerator(self.test_output)

    def tearDown(self):
        if os.path.exists(self.test_output):
            os.remove(self.test_output)

    def test_pdf_creation(self):
        """Test basic PDF creation and page size (landscape)."""
        canvas = self.generator.create_pdf()
        self.assertEqual(canvas._pagesize, landscape(A5))  # Compare with ReportLab's A5 landscape

    def test_page_layout(self):
        """Test page layout with all elements in landscape."""
        self.generator.create_pdf()
        self.generator.create_page(
            title="Test Title",
            sequence=1,
            attributes=["Attr1", "Attr2"],
            content="Test content",
            comment_count=5
        )
        self.generator.save()
        
        # Verify file was created
        self.assertTrue(os.path.exists(self.test_output))
        self.assertGreater(os.path.getsize(self.test_output), 0)

    def test_text_wrapping(self):
        """Test text wrapping functionality in landscape."""
        self.generator.create_pdf()
        long_text = "This is a very long text that should be wrapped " * 10
        self.generator.create_page(
            title="Wrapping Test",
            sequence=1,
            attributes=[],
            content=long_text
        )
        self.generator.save()
        
        # Verify file was created
        self.assertTrue(os.path.exists(self.test_output))
        self.assertGreater(os.path.getsize(self.test_output), 0)

    def test_cyrillic_support(self):
        """Test Cyrillic character support in landscape."""
        self.generator.create_pdf()
        cyrillic_text = "Привет, мир! This is a mixed text."
        self.generator.create_page(
            title="Cyrillic Test",
            sequence=1,
            attributes=["Тест"],
            content=cyrillic_text
        )
        self.generator.save()
        
        # Verify file was created
        self.assertTrue(os.path.exists(self.test_output))
        self.assertGreater(os.path.getsize(self.test_output), 0)

if __name__ == '__main__':
    unittest.main() 