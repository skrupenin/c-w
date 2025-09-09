from pyairtable import Table
from config import Config
from datetime import datetime
from tqdm import tqdm

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

        self.required_fields = [
            Config.FIELD_TITLE,
            Config.FIELD_SEQUENCE,
            Config.FIELD_ATTRIBUTE1,
            Config.FIELD_CONTENT,
            Config.FIELD_LAST_MODIFIED
        ]

    def _validate_record(self, record):
        fields = record['fields']
        
        # Validate required fields

        
        missing_fields = [field for field in self.required_fields if field not in fields]
        if missing_fields:
            raise ValueError(f"Record {record['id']} is missing required fields: {', '.join(missing_fields)}")
        
        # Create validated record with all required fields
        validated_record = {
            'id': record['id'],
            'title': fields[Config.FIELD_TITLE],
            'sequence': fields[Config.FIELD_SEQUENCE],
            'attribute1': fields[Config.FIELD_ATTRIBUTE1],
            'content': fields[Config.FIELD_CONTENT],
            'last_modified': datetime.fromisoformat(fields[Config.FIELD_LAST_MODIFIED].replace('Z', '+00:00'))
        }

        return validated_record

    def get_records(self, modified_since=None, fragment_ids=None):
        """
        Fetch records from the configured Airtable table.
        
        Args:
            modified_since (datetime, optional): If provided, only return records modified on or after this date.
            fragment_ids (list, optional): If provided, only return records with these sequence IDs.
            
        Returns:
            list: List of records with required fields.
            
        Raises:
            ValueError: If required fields are missing from records.
        """
        formula_parts = []
        if fragment_ids:
            formula_parts.append("OR(" + ",".join(f"{{Порядковый номер}}={seq}" for seq in fragment_ids) + ")")
        if modified_since:
            formula_parts.append(f"IS_AFTER({{Last modified time}}, DATETIME_PARSE('{modified_since}'))")
        formula = "AND(" + ",".join(formula_parts) + ")" if len(formula_parts) > 1 else (formula_parts[0] if formula_parts else "")

        records = self.table.all(formula=formula, sort=[f"{Config.FIELD_ATTRIBUTE1}"])

        validated_records = []
        
        for record in tqdm(records, desc="Processing Airtable records"):
            validated_record = self._validate_record(record)

            comments = self.table.comments(record['id'])
            if len(comments) > 0:
                joint_comments = "\n".join([("Q: " + comment.text) for comment in comments])
                validated_record['content'] = '<span style="color:#AFABAB;mso-style-textfill-fill-color:#AFABAB;">'+joint_comments + "</span>\n\n" + validated_record['content']
                
            validated_records.append(validated_record)
                
        return validated_records

    def get_record_count(self):
        """
        Get the total number of records in the table.
        
        Returns:
            int: Number of records.
        """
        return len(self.table.all())
