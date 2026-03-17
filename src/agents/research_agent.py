import os
from typing import Dict, Any, Optional
from .base_agent import BaseAgent

class ResearchAgent(BaseAgent):
    def __init__(self, api_key: Optional[str] = None):
        """
        Research agent for web searching and information gathering.
        Uses Tavily API for web search capabilities.
        """
        system_prompt = """သင်သည် Research Agent ဖြစ်ပါသည်။ သင်၏တာဝန်မှာ web search လုပ်ပြီး အချက်အလက်များရှာဖွေရန် ဖြစ်သည်။

သင့်လုပ်ဆောင်နိုင်သောအရာများ:
- သတင်းအချက်အလက်များရှာဖွေခြင်း
- နောက်ဆုံးရလဒ်များစစ်ဆေးခြင်း
- Technical documentation ရှာဖွေခြင်း
- Real-time information ရယူခြင်း

အသုံးပြုသော language များ:
- Myanmar (မြန်မာဘာသာ)
- English

တုံ့ပြန်ပုံစံ:
- ရှာဖွေတွေ့ရှိသောအချက်အလက်များကို စုစည်းတင်ပြပါ
- အရင်းအမြစ်များကို ဖော်ပြပါ
- တိကျသောအချက်အလက်များကို ဦးစွာတင်ပြပါ"""
        
        super().__init__(
            name="Research Agent",
            system_prompt=system_prompt,
            api_key=api_key
        )
        
        self.tavily_api_key = api_key or os.getenv("TAVILY_API_KEY")
    
    def get_agent_type(self) -> str:
        return "research"
    
    def can_handle(self, message: str) -> bool:
        """
        Check if the message requires research/search capabilities.
        """
        research_keywords = [
            "search", "find", "look for", "research", "ရှာ", "ရှာဖွေ", "သတင်း",
            "news", "latest", "recent", "current", "နောက်ဆုံး", "လတ်တလော",
            "information", "data", "statistics", "အချက်အလက်", "စာရင်းအင်း",
            "documentation", "docs", "tutorial", "guide", "စာတမ်း", "လမ်းညွှန်"
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in research_keywords)
    
    def search_web(self, query: str) -> str:
        """
        Perform web search using Tavily API.
        Note: This is a placeholder - actual implementation will use Tavily API
        """
        # TODO: Implement Tavily API integration
        # For now, return a mock response
        return f"🔍 '{query}' အတွက် web search လုပ်ဆောင်နေပါသည်။\n\n" \
               f"အကယ်၍ Tavily API key ရှိပါက၊ တကယ့် search ရလဒ်များကို ပြန်လည်တင်ပြပါမည်။\n" \
               f"လောလောဆယ်တော့ Gemini model ကိုသာ အသုံးပြုပြီး တုံ့ပြန်ပေးပါသည်။"
    
    def process_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Process research-related messages.
        """
        if not self.can_handle(message):
            return f"❌ {self.name} အနေဖြင့် ဤ message ကို handle လုပ်နိုင်မည် မဟုတ်ပါ။"
        
        # Add search context to the prompt
        search_context = {
            "search_capability": "Web search with Tavily API",
            "current_status": "API integration pending"
        }
        
        if context:
            search_context.update(context)
        
        return super().process_message(message, search_context)
