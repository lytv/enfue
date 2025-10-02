#!/usr/bin/env python3
"""
Semantic Search and Natural Language Search Demo for Enfue Companies
This script demonstrates advanced Typesense features with practical examples
"""

import typesense
import json
import time
from typing import List, Dict, Any

# Typesense configuration
TYPESENSE_CONFIG = {
    'api_key': 'Hu52dwsas2AdxdE',
    'nodes': [{
        'host': 'localhost',
        'port': '8108',
        'protocol': 'http'
    }],
    'connection_timeout_seconds': 2
}

COLLECTION_NAME = 'enfue_companies'

def create_typesense_client() -> typesense.Client:
    """Create and return Typesense client"""
    return typesense.Client(TYPESENSE_CONFIG)

def demo_semantic_search():
    """Demonstrate Semantic Search capabilities"""
    print("🧠 SEMANTIC SEARCH DEMO")
    print("=" * 50)
    
    client = create_typesense_client()
    
    # Example 1: Search by meaning, not exact keywords
    print("\n1. 🔍 Search by Meaning:")
    print("   Query: 'companies that develop software'")
    print("   Expected: Should find tech/software companies even without exact keywords")
    
    try:
        # This simulates semantic search by using broader terms
        results = client.collections[COLLECTION_NAME].documents.search({
            'q': 'software development technology programming',
            'query_by': 'company_name',
            'per_page': 5
        })
        
        print(f"   Found {results['found']} results:")
        for hit in results['hits']:
            print(f"   - {hit['document']['company_name']} ({hit['document']['location']})")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 2: Search for companies with job opportunities
    print("\n2. 💼 Search for Hiring Companies:")
    print("   Query: 'companies hiring developers'")
    print("   Expected: Should find companies with open positions")
    
    try:
        results = client.collections[COLLECTION_NAME].documents.search({
            'q': 'hiring developers positions opportunities',
            'query_by': 'company_name',
            'filter_by': 'has_positions:=true',
            'per_page': 5
        })
        
        print(f"   Found {results['found']} companies with open positions:")
        for hit in results['hits']:
            print(f"   - {hit['document']['company_name']}: {hit['document']['open_positions']} positions")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 3: Search by company type/industry
    print("\n3. 🏭 Search by Industry Type:")
    print("   Query: 'technology companies'")
    print("   Expected: Should find tech-related companies")
    
    try:
        results = client.collections[COLLECTION_NAME].documents.search({
            'q': 'technology tech software IT digital',
            'query_by': 'company_name',
            'per_page': 5
        })
        
        print(f"   Found {results['found']} tech companies:")
        for hit in results['hits']:
            print(f"   - {hit['document']['company_name']} ({hit['document']['location']})")
            
    except Exception as e:
        print(f"   Error: {e}")

def demo_natural_language_search():
    """Demonstrate Natural Language Search capabilities"""
    print("\n💬 NATURAL LANGUAGE SEARCH DEMO")
    print("=" * 50)
    
    client = create_typesense_client()
    
    # Example 1: Location-based queries
    print("\n1. 📍 Location-based Queries:")
    
    natural_queries = [
        "Show me companies in Da Nang",
        "Find companies located in Ho Chi Minh City",
        "Companies in Hue city"
    ]
    
    for query in natural_queries:
        print(f"\n   Query: '{query}'")
        
        # Parse natural language to structured query
        if "da nang" in query.lower():
            location = "Da Nang"
        elif "ho chi minh" in query.lower():
            location = "Ho Chi Minh"
        elif "hue" in query.lower():
            location = "Hue"
        else:
            location = None
        
        if location:
            try:
                results = client.collections[COLLECTION_NAME].documents.search({
                    'q': '*',
                    'query_by': 'company_name',
                    'filter_by': f'location:={location}',
                    'per_page': 3
                })
                
                print(f"   Found {results['found']} companies in {location}:")
                for hit in results['hits']:
                    print(f"   - {hit['document']['company_name']}")
                    
            except Exception as e:
                print(f"   Error: {e}")
    
    # Example 2: Job-related queries
    print("\n2. 💼 Job-related Queries:")
    
    job_queries = [
        "Companies with open positions",
        "Show me companies that are hiring",
        "Companies with more than 5 job openings"
    ]
    
    for query in job_queries:
        print(f"\n   Query: '{query}'")
        
        # Parse natural language to structured query
        if "more than 5" in query.lower():
            filter_by = "open_positions:>5"
        elif "hiring" in query.lower() or "open positions" in query.lower():
            filter_by = "has_positions:=true"
        else:
            filter_by = None
        
        if filter_by:
            try:
                results = client.collections[COLLECTION_NAME].documents.search({
                    'q': '*',
                    'query_by': 'company_name',
                    'filter_by': filter_by,
                    'per_page': 3
                })
                
                print(f"   Found {results['found']} companies:")
                for hit in results['hits']:
                    print(f"   - {hit['document']['company_name']}: {hit['document']['open_positions']} positions")
                    
            except Exception as e:
                print(f"   Error: {e}")
    
    # Example 3: Complex queries
    print("\n3. 🔍 Complex Queries:")
    
    complex_queries = [
        "Tech companies in Da Nang with open positions",
        "Show me the biggest companies by number of positions",
        "Companies starting with 'A' in Ho Chi Minh"
    ]
    
    for query in complex_queries:
        print(f"\n   Query: '{query}'")
        
        try:
            if "tech companies in da nang with open positions" in query.lower():
                results = client.collections[COLLECTION_NAME].documents.search({
                    'q': 'tech technology software',
                    'query_by': 'company_name',
                    'filter_by': 'location:=Da Nang && has_positions:=true',
                    'per_page': 3
                })
                
            elif "biggest companies by number of positions" in query.lower():
                results = client.collections[COLLECTION_NAME].documents.search({
                    'q': '*',
                    'query_by': 'company_name',
                    'sort_by': 'open_positions:desc',
                    'per_page': 3
                })
                
            elif "companies starting with 'a'" in query.lower():
                results = client.collections[COLLECTION_NAME].documents.search({
                    'q': 'A*',
                    'query_by': 'company_name',
                    'filter_by': 'location:=Ho Chi Minh',
                    'per_page': 3
                })
            
            else:
                continue
            
            print(f"   Found {results['found']} results:")
            for hit in results['hits']:
                print(f"   - {hit['document']['company_name']} ({hit['document']['location']}) - {hit['document']['open_positions']} positions")
                
        except Exception as e:
            print(f"   Error: {e}")

def demo_advanced_search_features():
    """Demonstrate advanced search features that support semantic understanding"""
    print("\n🚀 ADVANCED SEARCH FEATURES")
    print("=" * 50)
    
    client = create_typesense_client()
    
    # Example 1: Fuzzy matching (typo tolerance)
    print("\n1. 🔤 Fuzzy Matching (Typo Tolerance):")
    
    fuzzy_queries = ["enfue", "enfu", "enfuee", "tech", "tehc", "tecnology"]
    
    for query in fuzzy_queries:
        print(f"\n   Query: '{query}'")
        
        try:
            results = client.collections[COLLECTION_NAME].documents.search({
                'q': query,
                'query_by': 'company_name',
                'per_page': 2
            })
            
            print(f"   Found {results['found']} results:")
            for hit in results['hits']:
                print(f"   - {hit['document']['company_name']}")
                
        except Exception as e:
            print(f"   Error: {e}")
    
    # Example 2: Multi-field search
    print("\n2. 🔍 Multi-field Search:")
    
    try:
        results = client.collections[COLLECTION_NAME].documents.search({
            'q': 'tech da nang',
            'query_by': 'company_name,location',
            'per_page': 5
        })
        
        print(f"   Found {results['found']} results matching 'tech' in company name or 'da nang' in location:")
        for hit in results['hits']:
            print(f"   - {hit['document']['company_name']} ({hit['document']['location']})")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 3: Weighted search
    print("\n3. ⚖️ Weighted Search:")
    
    try:
        results = client.collections[COLLECTION_NAME].documents.search({
            'q': 'tech software',
            'query_by': 'company_name',
            'query_by_weights': '2',  # Higher weight for company_name
            'per_page': 5
        })
        
        print(f"   Found {results['found']} results with weighted scoring:")
        for hit in results['hits']:
            print(f"   - {hit['document']['company_name']} (Score: {hit.get('text_match', 'N/A')})")
            
    except Exception as e:
        print(f"   Error: {e}")

def demo_search_analytics():
    """Demonstrate search analytics and performance"""
    print("\n📊 SEARCH ANALYTICS & PERFORMANCE")
    print("=" * 50)
    
    client = create_typesense_client()
    
    # Performance test
    print("\n1. ⚡ Performance Test:")
    
    test_queries = [
        "*",
        "tech",
        "da nang",
        "open positions",
        "enfue"
    ]
    
    for query in test_queries:
        start_time = time.time()
        
        try:
            results = client.collections[COLLECTION_NAME].documents.search({
                'q': query,
                'query_by': 'company_name',
                'per_page': 10
            })
            
            end_time = time.time()
            search_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            print(f"   Query: '{query}' - {search_time:.2f}ms - {results['found']} results")
            
        except Exception as e:
            print(f"   Query: '{query}' - Error: {e}")
    
    # Search statistics
    print("\n2. 📈 Search Statistics:")
    
    try:
        # Get total companies
        total_results = client.collections[COLLECTION_NAME].documents.search({
            'q': '*',
            'query_by': 'company_name',
            'per_page': 1
        })
        
        # Get companies with positions
        hiring_results = client.collections[COLLECTION_NAME].documents.search({
            'q': '*',
            'query_by': 'company_name',
            'filter_by': 'has_positions:=true',
            'per_page': 1
        })
        
        # Get location distribution
        location_results = client.collections[COLLECTION_NAME].documents.search({
            'q': '*',
            'query_by': 'company_name',
            'facet_by': 'location',
            'per_page': 1
        })
        
        print(f"   Total Companies: {total_results['found']}")
        print(f"   Companies with Open Positions: {hiring_results['found']}")
        print(f"   Location Distribution:")
        
        if 'facet_counts' in location_results and location_results['facet_counts']:
            for facet in location_results['facet_counts'][0]['counts']:
                print(f"     - {facet['value']}: {facet['count']} companies")
        
    except Exception as e:
        print(f"   Error: {e}")

def main():
    """Main demo function"""
    print("🎯 TYPESENSE SEMANTIC & NATURAL LANGUAGE SEARCH DEMO")
    print("=" * 60)
    print("This demo shows how Typesense can understand meaning and natural language")
    print("even without explicit semantic search models.")
    print()
    
    try:
        # Test connection
        client = create_typesense_client()
        client.collections.retrieve()
        print("✅ Connected to Typesense successfully")
        
        # Run demos
        demo_semantic_search()
        demo_natural_language_search()
        demo_advanced_search_features()
        demo_search_analytics()
        
        print("\n🎉 Demo completed successfully!")
        print("\n💡 Key Takeaways:")
        print("   - Typesense provides excellent fuzzy matching and typo tolerance")
        print("   - Multi-field search allows semantic-like understanding")
        print("   - Natural language can be parsed into structured queries")
        print("   - Advanced filtering enables complex search scenarios")
        print("   - Performance is excellent even with complex queries")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("Make sure Typesense server is running on localhost:8108")

if __name__ == "__main__":
    main()
