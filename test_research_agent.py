#!/usr/bin/env python3
"""
Test script for the upgraded Research Agent with real-time search capabilities.
Demonstrates sports news, international news, and Myanmar news search.
"""

import os
from dotenv import load_dotenv
from src.agents.research_agent import ResearchAgent

def test_research_agent():
    """Test the enhanced Research Agent with various search queries."""
    
    # Load environment variables
    load_dotenv()
    
    # Initialize Research Agent
    print("🔍 Initializing Enhanced Research Agent...")
    research_agent = ResearchAgent()
    
    # Test queries
    test_queries = [
        {
            "query": "နောက်ဆုံးဘောလုံးသတင်းများ",
            "description": "Myanmar - Latest football news"
        },
        {
            "query": "international news asia",
            "description": "English - International Asia news"
        },
        {
            "query": "myanmar news today",
            "description": "Myanmar - Local news search"
        },
        {
            "query": "basketball latest news",
            "description": "English - Basketball news"
        },
        {
            "query": "အားကစားသတင်းလတ်တလော",
            "description": "Myanmar - Latest sports news"
        }
    ]
    
    print(f"\n🧪 Running {len(test_queries)} test queries...")
    print("=" * 60)
    
    for i, test_case in enumerate(test_queries, 1):
        query = test_case["query"]
        description = test_case["description"]
        
        print(f"\n📝 Test {i}: {description}")
        print(f"🔍 Query: '{query}'")
        print("-" * 40)
        
        try:
            # Check if agent can handle the query
            if research_agent.can_handle(query):
                print("✅ Agent can handle this query")
                
                # Process the query
                result = research_agent.process_message(query)
                
                # Display result (truncated for readability)
                if len(result) > 500:
                    print(f"📄 Result (first 500 chars):\n{result[:500]}...")
                    print(f"📊 Full result length: {len(result)} characters")
                else:
                    print(f"📄 Result:\n{result}")
                
            else:
                print("❌ Agent cannot handle this query")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("\n" + "=" * 60)
    
    # Test individual search methods
    print("\n🎯 Testing individual search methods...")
    print("=" * 60)
    
    search_methods = [
        ("Sports News", lambda: research_agent.search_sports_news("football")),
        ("International News", lambda: research_agent.search_international_news("global")),
        ("Myanmar News", lambda: research_agent.search_myanmar_news()),
        ("Web Search", lambda: research_agent.search_web("latest technology news"))
    ]
    
    for method_name, method_func in search_methods:
        print(f"\n🔍 Testing {method_name}...")
        try:
            result = method_func()
            if len(result) > 300:
                print(f"📄 Result (first 300 chars):\n{result[:300]}...")
            else:
                print(f"📄 Result:\n{result}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        print("-" * 40)

def test_agent_info():
    """Display agent information."""
    load_dotenv()
    research_agent = ResearchAgent()
    
    print("\n🤖 Research Agent Information:")
    print("=" * 40)
    info = research_agent.get_info()
    for key, value in info.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    print("🚀 Enhanced Research Agent Test Suite")
    print("=" * 60)
    
    # Check API keys
    tavily_key = os.getenv("TAVILY_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    print(f"🔑 Tavily API Key: {'✅ Configured' if tavily_key else '❌ Missing'}")
    print(f"🔑 Gemini API Key: {'✅ Configured' if gemini_key else '❌ Missing'}")
    
    if not tavily_key:
        print("\n⚠️  Warning: Tavily API key not found!")
        print("   Set TAVILY_API_KEY in your .env file for real search results.")
        print("   Without it, the agent will return mock responses.\n")
    
    if not gemini_key:
        print("\n❌ Error: Gemini API key not found!")
        print("   Set GEMINI_API_KEY in your .env file to use the agent.")
        exit(1)
    
    test_agent_info()
    test_research_agent()
    
    print("\n🎉 Test completed!")
    print("\n💡 Tips:")
    print("- Configure TAVILY_API_KEY for real search results")
    print("- Try queries like: 'football news', 'international news', 'myanmar news'")
    print("- Use Myanmar or English language for best results")
