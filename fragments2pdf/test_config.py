from config import Config
from airtable_client import AirtableClient

def test_config():
    """Test configuration loading and validation."""
    try:
        Config.validate()
        print("✅ Configuration validation successful")
    except ValueError as e:
        print(f"❌ Configuration validation failed: {e}")
        return False
    return True

def test_airtable_connection():
    """Test Airtable connection and data retrieval."""
    try:
        client = AirtableClient()
        records = client.get_records()
        print(f"✅ Successfully retrieved {len(records)} records from Airtable")
        
        # Print first record as sample
        if records:
            print("\nSample record:")
            print(f"Title: {records[0]['title']}")
            print(f"Sequence: {records[0]['sequence']}")
            print(f"Attribute1: {records[0]['attribute1']}")
            print(f"Content length: {len(records[0]['content'])} characters")
#            print(f"Comments count: {len(records[0]['comments'])}")
        
        return True
    except Exception as e:
        print(f"❌ Airtable connection test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing configuration and Airtable integration...\n")
    
    config_ok = test_config()
    if config_ok:
        airtable_ok = test_airtable_connection()
        
    print("\nTest summary:")
    print(f"Configuration: {'✅ Passed' if config_ok else '❌ Failed'}")
    if config_ok:
        print(f"Airtable connection: {'✅ Passed' if airtable_ok else '❌ Failed'}") 