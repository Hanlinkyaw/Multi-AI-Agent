#!/usr/bin/env python3
"""
Simple test script to verify enhanced error handling for free tier APIs.
Tests 401 (invalid key) and 429 (quota exceeded) scenarios.
"""

import os
import logging
from dotenv import load_dotenv
from src.agents.research_agent import ResearchAgent

# Set up logging to see error messages
logging.basicConfig(level=logging.INFO)

def test_free_tier_errors():
    """Test error handling for free tier limitations."""
    print("🧪 Testing Free Tier Error Handling")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Test 1: Missing API Key
    print("\n1. Testing Missing API Key:")
    print("-" * 40)
    
    # Temporarily remove API key
    original_key = os.getenv("TAVILY_API_KEY")
    os.environ["TAVILY_API_KEY"] = ""
    
    agent = ResearchAgent()
    result = agent.search_web("test query")
    print(f"Result: {result}")
    
    # Test 2: Invalid API Key (simulate 401 error)
    print("\n2. Testing Invalid API Key (401):")
    print("-" * 40)
    
    # Use an invalid key format
    os.environ["TAVILY_API_KEY"] = "invalid_key_format_12345"
    
    agent = ResearchAgent()
    result = agent.search_web("test query")
    print(f"Result: {result}")
    
    # Test 3: Valid key but check if it handles quota limits properly
    if original_key:
        print("\n3. Testing with Valid API Key:")
        print("-" * 40)
        
        os.environ["TAVILY_API_KEY"] = original_key
        agent = ResearchAgent()
        result = agent.search_web("latest news")
        print(f"Result: {result}")
        
        # Test multiple rapid requests to potentially trigger 429
        print("\n4. Testing Rapid Requests (may trigger 429):")
        print("-" * 40)
        
        for i in range(3):
            print(f"\nRequest {i+1}:")
            result = agent.search_web(f"test query {i+1}")
            if "429" in result or "quota" in result.lower():
                print("✅ Rate limit error handled correctly!")
                break
            elif len(result) > 100:  # Successful response
                print("✅ Request successful")
            else:
                print(f"Response: {result}")
    
    print("\n" + "=" * 60)
    print("🎉 Error handling test completed!")
    
    # Restore original key
    if original_key:
        os.environ["TAVILY_API_KEY"] = original_key

if __name__ == "__main__":
    print("🚀 Free Tier Error Handling Test")
    print("=" * 60)
    print("This test verifies that the Research Agent handles:")
    print("- Missing API Key (401)")
    print("- Invalid API Key (401)") 
    print("- Rate Limiting (429)")
    print("- Quota Exceeded (402)")
    print("=" * 60)
    
    test_free_tier_errors()
    
    print("\n💡 Expected Results:")
    print("- Missing API Key: 'API Key ပျောက်နေပါသည်'")
    print("- Invalid Key: 'API Key မှားနေပါသည် (401)'")
    print("- Rate Limit: 'Free Tier Quota ပြည့်သွားပါသည် (429)'")
    print("- Quota Exceeded: 'Free Tier Quota ကုန်ဆုံးသွားပါသည် (402)'")
