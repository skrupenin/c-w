import unittest
import os
from unittest.mock import patch, MagicMock
from main import process_airtable_to_pdf

class TestIntegration(unittest.TestCase):
    @patch('main.AirtableClient')
    def test_end_to_end(self, MockAirtableClient):
        # Mock records
        mock_records = [
            {
                'id': 'rec1',
                'title': 'Test Title',
                'sequence': 1,
                'attribute1': ['Attr1', 'Attr2'],
                'content': '**Bold** _Italic_ __Underline__',
            },
            {
                'id': 'rec2',
                'title': 'Second',
                'sequence': 2,
                'attribute1': ['Attr3'],
                'content': 'Normal text',
            }
        ]
        instance = MockAirtableClient.return_value
        instance.get_records.return_value = mock_records

        output_path = 'test_integration_output.pdf'
        result = process_airtable_to_pdf(output_path=output_path)
        self.assertTrue(result.success)
        self.assertTrue(os.path.exists(output_path))
        self.assertEqual(result.record_count, 2)
        os.remove(output_path)

    @patch('main.AirtableClient')
    def test_error_handling(self, MockAirtableClient):
        instance = MockAirtableClient.return_value
        instance.get_records.side_effect = Exception('Airtable error')
        result = process_airtable_to_pdf(output_path='should_not_exist.pdf')
        self.assertFalse(result.success)
        self.assertIn('Airtable error', result.error)

if __name__ == '__main__':
    unittest.main() 