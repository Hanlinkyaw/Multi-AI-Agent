#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from src.core.router import AgentRouter

def test_multi_agent_system():
    """Test the multi-agent system with different message types."""
    
    # Load environment variables
    load_dotenv()
    
    print("🤖 Multi-Agent System Test")
    print("=" * 50)
    
    # Initialize router
    try:
        router = AgentRouter()
        print("✅ Agent Router initialized successfully")
        
        # Show agent status
        status = router.get_agent_status()
        print(f"📊 Total Agents: {status['total_agents']}")
        for agent_type, agent_info in status['agents'].items():
            print(f"  - {agent_type}: {agent_info['name']} ({agent_info['model']})")
        
        print("\n" + "=" * 50)
        print("🧪 Testing Different Message Types")
        print("=" * 50)
        
        # Test messages
        test_messages = [
            {
                "message": "လောလောဆယ်သတင်းများကို ရှာပေးပါ",
                "expected_agent": "research"
            },
            {
                "message": "run df -h",
                "expected_agent": "devops"
            },
            {
                "message": "system status ကို စစ်ဆေးပေးပါ",
                "expected_agent": "devops"
            },
            {
                "message": "docker ps ကို လုပ်ပေးပါ",
                "expected_agent": "devops"
            },
            {
                "message": "ကျွန်ုပ်တို့အကြောင်း ပြောပြပါ",
                "expected_agent": "general"
            }
        ]
        
        for i, test in enumerate(test_messages, 1):
            print(f"\n📝 Test {i}: {test['message']}")
            print(f"Expected Agent: {test['expected_agent']}")
            print("-" * 30)
            
            result = router.route_message(test['message'])
            
            if result['success']:
                print(f"✅ Agent: {result['agent']}")
                print(f"📄 Response: {result['response'][:200]}...")
            else:
                print(f"❌ Error: {result['error']}")
        
        print("\n" + "=" * 50)
        print("🎯 Test Complete!")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_multi_agent_system()
