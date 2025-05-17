from pyairtable import Api, Table
from config import Config

class AirtableClient:
    def __init__(self):
        """Initialize the Airtable client with configuration."""
        Config.validate()
        self.api = Api(Config.AIRTABLE_API_KEY)
        self.table = Table(
            Config.AIRTABLE_API_KEY,
            Config.AIRTABLE_BASE_ID,
            Config.AIRTABLE_TABLE_ID
        )

    def get_records(self):
        """
        Fetch all records from the configured Airtable table.
        
        Returns:
            list: List of records with required fields.
            
        Raises:
            ValueError: If required fields are missing from records.
        """
        records = self.table.all()
        validated_records = []
        
        for record in records:
            fields = record['fields']
            
            # Validate required fields
            required_fields = [
                Config.FIELD_TITLE,
                Config.FIELD_SEQUENCE,
                Config.FIELD_ATTRIBUTE1,
                Config.FIELD_CONTENT
            ]
            
            missing_fields = [field for field in required_fields if field not in fields]
            if missing_fields:
                raise ValueError(f"Record {record['id']} is missing required fields: {', '.join(missing_fields)}")
            
            # Create validated record with all required fields
            validated_record = {
                'id': record['id'],
                'title': fields[Config.FIELD_TITLE],
                'sequence': fields[Config.FIELD_SEQUENCE],
                'attribute1': fields[Config.FIELD_ATTRIBUTE1],
                'content': fields[Config.FIELD_CONTENT],
#                'comments': fields.get(Config.FIELD_COMMENTS, [])
            }
            
            validated_records.append(validated_record)
        
        # Sort records by sequence number
        validated_records.sort(key=lambda x: x['sequence'])
        
        return validated_records

    def get_record_count(self):
        """
        Get the total number of records in the table.
        
        Returns:
            int: Number of records.
        """
        return len(self.table.all())
