#!/usr/bin/env python3
"""
Setup script for Enfue Companies Search Demo with Typesense
This script creates a Typesense collection and imports CSV data
"""

import typesense
import csv
import json
import os
import time
from typing import List, Dict, Any

# Typesense configuration
TYPESENSE_CONFIG = {
    'api_key': os.environ.get('TYPESENSE_API_KEY', 'Hu52dwsas2AdxdE'),
    'nodes': [{
        'host': os.environ.get('TYPESENSE_HOST', 'localhost').replace('http://', '').replace('https://', ''),
        'port': os.environ.get('TYPESENSE_PORT', '8108'),
        'protocol': 'http'
    }],
    'connection_timeout_seconds': 10
}

COLLECTION_NAME = 'enfue_companies'

def create_typesense_client() -> typesense.Client:
    """Create and return Typesense client"""
    return typesense.Client(TYPESENSE_CONFIG)

def create_collection_schema() -> Dict[str, Any]:
    """Define the collection schema for companies data"""
    return {
        "name": COLLECTION_NAME,
        "fields": [
            {
                "name": "company_name",
                "type": "string",
                "facet": False
            },
            {
                "name": "location", 
                "type": "string",
                "facet": True
            },
            {
                "name": "open_positions",
                "type": "int32",
                "facet": True
            },
            {
                "name": "has_positions",
                "type": "bool",
                "facet": True
            }
        ],
        "default_sorting_field": "open_positions"
    }

def parse_csv_data(csv_file_path: str) -> List[Dict[str, Any]]:
    """Parse CSV file and convert to Typesense documents"""
    documents = []
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        # Skip the header row
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header
        
        for row_num, row in enumerate(csv_reader, start=1):
            if len(row) >= 1:  # At least one field
                # The CSV has a special format where each row is a single quoted string
                # containing comma-separated values
                row_content = row[0] if row else ""
                
                # Remove outer quotes and split by comma
                if row_content.startswith('"') and row_content.endswith('"'):
                    row_content = row_content[1:-1]  # Remove outer quotes
                
                # Split by comma, but be careful with quoted fields
                fields = []
                current_field = ""
                in_quotes = False
                
                for char in row_content:
                    if char == '"':
                        in_quotes = not in_quotes
                    elif char == ',' and not in_quotes:
                        fields.append(current_field.strip())
                        current_field = ""
                        continue
                    current_field += char
                
                # Add the last field
                if current_field:
                    fields.append(current_field.strip())
                
                # Clean up fields - remove quotes
                cleaned_fields = []
                for field in fields:
                    if field.startswith('"') and field.endswith('"'):
                        field = field[1:-1]
                    cleaned_fields.append(field)
                
                if len(cleaned_fields) >= 3:
                    company_name = cleaned_fields[0]
                    location = cleaned_fields[1]
                    positions_text = cleaned_fields[2]
                    
                    # Extract number from positions text (e.g., "2 open positions" -> 2)
                    open_positions = 0
                    if positions_text and positions_text != "0 open positions":
                        try:
                            # Extract number from text like "2 open positions"
                            import re
                            numbers = re.findall(r'\d+', positions_text)
                            if numbers:
                                open_positions = int(numbers[0])
                        except (ValueError, IndexError):
                            open_positions = 0
                    
                    document = {
                        "id": f"company_{row_num}",
                        "company_name": company_name,
                        "location": location,
                        "open_positions": open_positions,
                        "has_positions": open_positions > 0
                    }
                    
                    documents.append(document)
    
    return documents

def setup_collection(client: typesense.Client) -> bool:
    """Create or recreate the collection"""
    try:
        # Delete existing collection if it exists
        try:
            client.collections[COLLECTION_NAME].delete()
            print(f"✅ Deleted existing collection: {COLLECTION_NAME}")
        except Exception:
            pass  # Collection doesn't exist, that's fine
        
        # Create new collection
        collection_schema = create_collection_schema()
        client.collections.create(collection_schema)
        print(f"✅ Created collection: {COLLECTION_NAME}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating collection: {e}")
        return False

def import_data(client: typesense.Client, csv_file_path: str) -> bool:
    """Import CSV data to Typesense"""
    try:
        print("📊 Parsing CSV data...")
        documents = parse_csv_data(csv_file_path)
        print(f"✅ Parsed {len(documents)} companies from CSV")
        
        # Import documents in batches
        batch_size = 50
        total_imported = 0
        
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            client.collections[COLLECTION_NAME].documents.import_(batch)
            total_imported += len(batch)
            print(f"📤 Imported batch: {total_imported}/{len(documents)} companies")
        
        print(f"✅ Successfully imported {total_imported} companies to Typesense")
        return True
        
    except Exception as e:
        print(f"❌ Error importing data: {e}")
        return False

def test_search(client: typesense.Client) -> None:
    """Test some sample searches"""
    print("\n🔍 Testing search functionality...")
    
    # Test searches
    test_queries = [
        {"q": "enfue", "query_by": "company_name"},
        {"q": "Da Nang", "query_by": "location"},
        {"q": "tech", "query_by": "company_name"},
        {"q": "*", "query_by": "company_name", "filter_by": "has_positions:=true"},
        {"q": "*", "query_by": "company_name", "sort_by": "open_positions:desc"}
    ]
    
    for i, query in enumerate(test_queries, 1):
        try:
            result = client.collections[COLLECTION_NAME].documents.search(query)
            print(f"Test {i}: Found {result['found']} results for query: {query['q']}")
        except Exception as e:
            print(f"Test {i}: Error - {e}")

def main():
    """Main setup function"""
    print("🚀 Setting up Enfue Companies Search Demo with Typesense")
    print("=" * 60)
    
    # Check if CSV file exists
    csv_file_path = "Run_Browser_Agent_With_A_Goal_In_Background_2025-10-02T03_02_40.209Z.csv"
    if not os.path.exists(csv_file_path):
        print(f"❌ CSV file not found: {csv_file_path}")
        print("Please make sure the CSV file is in the same directory as this script")
        return
    
    try:
        # Create Typesense client
        print("🔌 Connecting to Typesense...")
        client = create_typesense_client()
        
        # Test connection with retry logic
        max_retries = 5
        for attempt in range(max_retries):
            try:
                client.collections.retrieve()
                print("✅ Connected to Typesense successfully")
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"⚠️ Connection attempt {attempt + 1} failed: {e}")
                    print("⏳ Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    print(f"❌ Failed to connect to Typesense after {max_retries} attempts: {e}")
                    print("⚠️ Continuing without Typesense setup...")
                    return
        
        # Setup collection
        if not setup_collection(client):
            return
        
        # Import data
        if not import_data(client, csv_file_path):
            return
        
        # Test search functionality
        test_search(client)
        
        print("\n🎉 Setup completed successfully!")
        print("You can now use the search demo application")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        print("\nMake sure Typesense server is running:")
        print("docker run -p 8108:8108 -v/tmp/data:/data typesense/typesense:29.0 --data-dir /data --api-key=Hu52dwsas2AdxdE")

if __name__ == "__main__":
    main()
