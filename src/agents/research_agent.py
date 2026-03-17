import os
from typing import Dict, Any, Optional
from .base_agent import BaseAgent
from src.tools.search_tools import SearchTools, search_web, search_sports, search_international_news, search_myanmar_news

class ResearchAgent(BaseAgent):
    def __init__(self, api_key: Optional[str] = None):
        """
        Enhanced Research agent with real-time search capabilities.
        Uses Tavily API for web search and Myanmar language summarization.
        """
        system_prompt = """သင်သည် Research Agent ဖြစ်ပါသည်။ သင်၏တာဝန်မှာ real-time web search လုပ်ပြီး နောက်ဆုံးရသတင်းအချက်အလက်များရှာဖွေရန် ဖြစ်သည်။

သင့်လုပ်ဆောင်နိုင်သောအရာများ:
- 🔍 Real-time web search (Tavily API အသုံးပြု)
- 📰 နောက်ဆုံးအားကစားသတင်းများရှာဖွေခြင်း
- 🌍 နိုင်ငံတကာသတင်းများရှာဖွေခြင်း
- 🇲🇲 မြန်မာနိုင်ငံသတင်းများရှာဖွေခြင်း
- 📊 အချက်အလက်များစုစည်းတင်ပြခြင်း
- 🗣️ မြန်မာဘာသာဖြင့် အကျဉ်းချုပ်တင်ပြခြင်း

အသုံးပြုသော language များ:
- Myanmar (မြန်မာဘာသာ) - အဓိကဘာသာ
- English - ရှာဖွေရာတွင်အသုံးပြု

တုံ့ပြန်ပုံစံ:
- 🔍 ရှာဖွေတွေ့ရှိသောနောက်ဆုံးသတင်းများကို မြန်မာဘာသာဖြင့် စုစည်းတင်ပြပါ
- 📊 အရင်းအမြစ်များနှင့် လင့်ခ်များကို ဖော်ပြပါ
- ⚡ တိကျသောနှင့် နောက်ဆုံးရသတင်းများကို ဦးစွာတင်ပြပါ
- 🎯 အားကစား၊ နိုင်ငံတကာ၊ မြန်မာသတင်းများကို အထူးပြုလုပ်ဆောင်ပါ"""
        
        super().__init__(
            name="Research Agent",
            system_prompt=system_prompt,
            api_key=api_key
        )
        
        self.tavily_api_key = api_key or os.getenv("TAVILY_API_KEY")
        self.search_tools = SearchTools(self.tavily_api_key)
    
    def get_agent_type(self) -> str:
        return "research"
    
    def can_handle(self, message: str) -> bool:
        """
        Check if the message requires research/search capabilities.
        Enhanced with sports and news keywords.
        """
        research_keywords = [
            # General search
            "search", "find", "look for", "research", "ရှာ", "ရှာဖွေ", "သတင်း",
            
            # News related
            "news", "latest", "recent", "current", "နောက်ဆုံး", "လတ်တလော", "သတင်း",
            "update", "breaking", "headline", "အပ်ဒိတ်", "ခေါင်းစဉ်",
            
            # Sports
            "sport", "sports", "football", "soccer", "basketball", "tennis",
            "အားကစား", "ဘောလုံး", "ဘက်စုးဘော", "တင်းနစ်", "ပြိုင်ကား",
            "match", "game", "score", "goal", "player", "team", "ပွဲ", "ဂိုး", "အသင်း",
            
            # International
            "international", "world", "global", "asia", "europe", "america",
            "နိုင်ငံတကာ", "ကမ္ဘာ", "အာရှ", "ဥရောပ", "အမေရိက",
            
            # Myanmar
            "myanmar", "burma", "မြန်မာ", "ရန်ကုန်", "မန္တလေး",
            
            # Information/data
            "information", "data", "statistics", "အချက်အလက်", "စာရင်းအင်း",
            "documentation", "docs", "tutorial", "guide", "စာတမ်း", "လမ်းညွှန်"
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in research_keywords)
    
    def search_web(self, query: str) -> str:
        """
        Perform web search using Tavily API with Myanmar formatting.
        """
        return search_web(query, self.tavily_api_key)
    
    def search_sports_news(self, sport: str = "football") -> str:
        """
        Search for latest sports news with Myanmar formatting.
        """
        return search_sports(sport, self.tavily_api_key)
    
    def search_international_news(self, region: str = "global") -> str:
        """
        Search for international news with Myanmar formatting.
        """
        return search_international_news(region, self.tavily_api_key)
    
    def search_myanmar_news(self) -> str:
        """
        Search for Myanmar-specific news with Myanmar formatting.
        """
        return search_myanmar_news(self.tavily_api_key)
    
    def process_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Process research-related messages with enhanced search capabilities.
        """
        if not self.can_handle(message):
            return f"❌ {self.name} အနေဖြင့် ဤ message ကို handle လုပ်နိုင်မည် မဟုတ်ပါ။"
        
        message_lower = message.lower()
        
        # Check for specific search types
        if any(keyword in message_lower for keyword in ["sport", "sports", "အားကစား", "ဘောလုံး", "football", "ဘက်စုးဘော"]):
            # Extract sport type if mentioned
            sport = "football"  # default
            for s in ["football", "soccer", "basketball", "tennis", "cricket", "ဘောလုံး", "ဘက်စုးဘော", "တင်းနစ်"]:
                if s in message_lower:
                    sport = s
                    break
            return self.search_sports_news(sport)
        
        elif any(keyword in message_lower for keyword in ["international", "world", "global", "နိုင်ငံတကာ", "ကမ္ဘာ"]):
            # Extract region if mentioned
            region = "global"  # default
            for r in ["asia", "europe", "america", "africa", "အာရှ", "ဥရောပ", "အမေရိက"]:
                if r in message_lower:
                    region = r
                    break
            return self.search_international_news(region)
        
        elif any(keyword in message_lower for keyword in ["myanmar", "burma", "မြန်မာ", "ရန်ကုန်"]):
            return self.search_myanmar_news()
        
        else:
            # General web search
            return self.search_web(message)
