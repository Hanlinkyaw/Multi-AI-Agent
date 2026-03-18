import os
from typing import Dict, Any, Optional
from .base_agent import BaseAgent
from src.tools.search_tools import SearchTools, search_web, search_sports, search_international_news, search_myanmar_news
import logging

# Set up logging for the research agent
logger = logging.getLogger(__name__)

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
- ⚠️ အမှားပြများကို မြန်မာဘာသာဖြင့် ရှင်းလင်းတင်ပြခြင်း

အသုံးပြုသော language များ:
- Myanmar (မြန်မာဘာသာ) - အဓိကဘာသာ
- English - ရှာဖွေရာတွင်အသုံးပြု

တုံ့ပြန်ပုံစံ:
- 🔍 ရှာဖွေတွေ့ရှိသောနောက်ဆုံးသတင်းများကို မြန်မာဘာသာဖြင့် စုစည်းတင်ပြပါ
- 📊 အရင်းအမြစ်များနှင့် လင့်ခ်များကို ဖော်ပြပါ
- ⚡ တိကျသောနှင့် နောက်ဆုံးရသတင်းများကို ဦးစွာတင်ပြပါ
- 🎯 အားကစား၊ နိုင်ငံတကာ၊ မြန်မာသတင်းများကို အထူးပြုလုပ်ဆောင်ပါ
- ❌ အမှားပြဖြစ်ပါက အမှားအကြောင်းရင်းခံကို မြန်မာဘာသာဖြင့် ရှင်းလင်းပြပါ"""
        
        super().__init__(
            name="Research Agent",
            system_prompt=system_prompt,
            api_key=api_key
        )
        
        self.tavily_api_key = api_key or os.getenv("TAVILY_API_KEY")
        self.search_tools = SearchTools(self.tavily_api_key)
        
        # Log initialization status
        if self.tavily_api_key:
            logger.info("ResearchAgent initialized with Tavily API key")
        else:
            logger.warning("ResearchAgent initialized without Tavily API key")
    
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
    
    def search_web(self, query: str) -> Dict[str, Any]:
        """
        Perform web search and return raw data only.
        """
        logger.info(f"ResearchAgent performing web search for: '{query}'")
        try:
            return search_web(query, self.tavily_api_key)
        except Exception as e:
            logger.error(f"Web search failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def search_sports_news(self, sport: str = "football") -> Dict[str, Any]:
        """
        Search for sports news and return raw data only.
        """
        logger.info(f"ResearchAgent performing sports news search for: '{sport}'")
        try:
            return search_sports(sport, self.tavily_api_key)
        except Exception as e:
            logger.error(f"Sports news search failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def search_international_news(self, region: str = "global") -> Dict[str, Any]:
        """
        Search for international news and return raw data only.
        """
        logger.info(f"ResearchAgent performing international news search for: '{region}'")
        try:
            return search_international_news(region, self.tavily_api_key)
            
            try:
                # Use Gemini model for summarization
                response = self.model.generate_content(summary_prompt)
                summary = response.text
                
                # Add source links at the bottom
                links_section = f"\n\n**🌍 {region} သတင်းများရာထားအညွှန်းများ:**\n"
                for i, result in enumerate(results_list[:5], 1):
                    title = result.get("title", "")
                    url = result.get("url", "")
                    links_section += f"{i}. [{title}]({url})\n"
                
                return summary + links_section
                
            except Exception as e:
                logger.error(f"Failed to generate international news summary: {str(e)}")
                # Fallback to original search results if summarization fails
                return search_results
                
        except Exception as e:
            logger.error(f"International news search failed: {str(e)}")
            return f"❌ **{region} နိုင်ငံတကာသတင်းရှာဖွေမှုမအောင်မြင်ပါ**\n\nအမှားအကြောင်းရင်းခံ: {str(e)}"
    
    def search_myanmar_news(self) -> str:
        """
        Search for Myanmar-specific news with Myanmar formatting and AI-powered summarization.
        """
        logger.info("ResearchAgent performing Myanmar news search")
        try:
            # Get search results from Tavily
            search_results = search_myanmar_news(self.tavily_api_key)
            logger.info("Myanmar news search completed successfully")
            
            # If search failed, return error
            if not search_results.get("success", False):
                return search_results
            
            # Extract content for summarization
            results_list = search_results.get("results", [])
            answer = search_results.get("answer", "")
            
            if not results_list and not answer:
                return "❌ **မြန်မာနိုင်ငံတကာသတင်းများမရှိပါသည်**\n\nနောက်ဆုံး မြန်မာနိုင်ငံတကာသတင်းများမရှိပါသည်။"
            
            # Prepare content for AI analysis
            content_to_analyze = f"""
            မြန်မာနိုင်ငံတကာသတင်းများတွေ့ရှိသောအကြောင်းအရာများ:
            
            အဖြေရှင်းများ:
            {answer}
            
            ရှာဖွေရလဒ်ရလဒ်များ:
            """
            
            for i, result in enumerate(results_list[:5], 1):
                title = result.get("title", "")
                content = result.get("content", "")
                url = result.get("url", "")
                published_date = result.get("published_date", "")
                
                content_to_analyze += f"""
                {i}. {title}
                အကြောင်းအရာ: {content[:300]}...
                ထုတ်ပြန်ချိန်: {published_date}
                လင့်ခ်: {url}
                
                """
            
            # Generate Myanmar summary using Gemini
            summary_prompt = f"""သင်သည် ကူညီသော Myanmar news research assistant ဖြစ်ပါ။ မြန်မာနိုင်ငံတကာသတင်းများကို စိစစ်ပြီး မြန်မာဘာသာဖြင့် ရှင်းလင်းပြပေးပါ။

            လုပ်ဆောင်းချက်များ:
            - အဓိပ္ပာယ်ဖွင့်ဆိုချက်ကို ရိုးရှင်းပါ
            - Key Myanmar facts များကို bullet points ဖြင့်ဖော်ပါ
            - Technical jargon များကိုရှောင်းပါ
            - Friendly conversational Myanmar style ဖြင့်ရေးပါ
            - Links များကို အောက်ဆုံးတွင် references အဖြစ်သာပါ
            - 100% Myanmar language output

            မြန်မာနိုင်ငံတကာသတင်းများတွေ့ရှိသောအကြောင်းအရာများ:
            {content_to_analyze}

            ယခုရှိသောအကြောင်းအရာများကို မြန်မာဘာသာဖြင့် စိစစ်ပြီး ရှင်းလင်းပေးပါ။"""
            
            try:
                # Use Gemini model for summarization
                response = self.model.generate_content(summary_prompt)
                summary = response.text
                
                # Add source links at the bottom
                links_section = "\n\n**🇲🇲 မြန်မာနိုင်ငံတကာသတင်းများရာထားအညွှန်းများ:**\n"
                for i, result in enumerate(results_list[:5], 1):
                    title = result.get("title", "")
                    url = result.get("url", "")
                    links_section += f"{i}. [{title}]({url})\n"
                
                return summary + links_section
                
            except Exception as e:
                logger.error(f"Failed to generate Myanmar news summary: {str(e)}")
                # Fallback to original search results if summarization fails
                return search_results
                
        except Exception as e:
            logger.error(f"Myanmar news search failed: {str(e)}")
            return f"❌ **မြန်မာနိုင်ငံတကာသတင်းရှာဖွေမှုမအောင်မြင်ပါ**\n\nအမှားအကြောင်းရင်းခံ: {str(e)}"
    
    def process_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Process research-related messages with AI-powered analysis and summarization.
        """
        if not self.can_handle(message):
            logger.warning(f"ResearchAgent cannot handle message: '{message}'")
            return f"❌ {self.name} အနေဖြင့် ဤ message ကို handle လုပ်နိုင်မည် မဟုတ်ပါ။"
        
        logger.info(f"ResearchAgent processing message: '{message}'")
        message_lower = message.lower()
        
        try:
            # Get search results first
            search_results = None
            search_type = "general"
            
            # Check for specific search types
            if any(keyword in message_lower for keyword in ["sport", "sports", "အားကစား", "ဘောလုံး", "football", "ဘက်စုးဘော"]):
                # Extract sport type if mentioned
                sport = "football"  # default
                for s in ["football", "soccer", "basketball", "tennis", "cricket", "ဘောလုံး", "ဘက်စုးဘော", "တင်းနစ်"]:
                    if s in message_lower:
                        sport = s
                        break
                search_results = search_sports(sport, self.tavily_api_key)
                search_type = "sports"
            
            elif any(keyword in message_lower for keyword in ["international", "world", "global", "နိုင်ငံတကာ", "ကမ္ဘာ"]):
                # Extract region if mentioned
                region = "global"  # default
                for r in ["asia", "europe", "america", "africa", "အာရှ", "ဥရောပ", "အမေရိက"]:
                    if r in message_lower:
                        region = r
                        break
                search_results = search_international_news(region, self.tavily_api_key)
                search_type = "international"
            
            elif any(keyword in message_lower for keyword in ["myanmar", "burma", "မြန်မာ", "ရန်ကုန်"]):
                search_results = search_myanmar_news(self.tavily_api_key)
                search_type = "myanmar"
            
            else:
                # General web search
                search_results = search_web(message, self.tavily_api_key)
                search_type = "general"
            
            # Now analyze the search results with AI
            return self._analyze_search_results(search_results, message, search_type)
                
        except Exception as e:
            logger.error(f"ResearchAgent process_message failed: {str(e)}")
            return f"❌ **{self.name} တွင် error ဖြစ်ပါသည်**\n\nအမှားအကြောင်းရင်းခံ: {str(e)}"
    
    def _analyze_search_results(self, search_results: Any, original_query: str, search_type: str) -> str:
        """
        Analyze search results with AI and generate Myanmar summary.
        Handles both dictionary and string responses from search tools.
        """
        # Debug logging to see what we're getting
        logger.debug(f"Raw search results type: {type(search_results)}")
        logger.debug(f"Raw search results content: {str(search_results)[:500]}...")
        
        # Handle string responses (formatted Myanmar output)
        if isinstance(search_results, str):
            logger.info("Received formatted string response from search tool")
            # If it's already a formatted string, check if it's an error
            if "❌" in search_results or "**" in search_results:
                # This looks like an error, but still go through AI analysis
                content_to_analyze = f"""
                ရှာဖွေတွေ့ရှိသောအကြောင်းအရာများ ({search_type}) - Error Response:
                
                မေးခွန်း: {original_query}
                
                ရှာဖွေရလဒ်ရလဒ်များ:
                {search_results}
                """
            else:
                # Try to parse it as JSON if it looks like JSON
                try:
                    import json
                    parsed_results = json.loads(search_results)
                    logger.info("Successfully parsed string as JSON")
                    search_results = parsed_results
                except (json.JSONDecodeError, Exception):
                    logger.warning("Could not parse string as JSON, treating as plain text")
                    # Still go through AI analysis even for plain text
                    content_to_analyze = f"""
                    ရှာဖွေတွေ့ရှိသောအကြောင်းအရာများ ({search_type}) - Plain Text:
                    
                    မေးခွန်း: {original_query}
                    
                    ရှာဖွေရလဒ်ရလဒ်များ:
                    {search_results[:1000]}...
                    """
        
        # Handle dictionary responses
        if isinstance(search_results, dict):
            logger.info("Processing dictionary response from search tool")
            
            # Check if search failed - but still go through AI analysis
            if not search_results.get("success", False):
                logger.warning("Search tool reported failure, but still analyzing with AI")
                # Extract whatever content we can for analysis
                results_list = search_results.get("results", [])
                answer = search_results.get("answer", "")
                error_msg = search_results.get("error", "")
                
                content_to_analyze = f"""
                ရှာဖွေတွေ့ရှိသောအကြောင်းအရာများ ({search_type}) - Error Response:
                
                မေးခွန်း: {original_query}
                
                အမှားအကြောင်းရင်းခံ: {error_msg}
                
                အဖြေရှင်းများ: {answer}
                
                ရှာဖွေရလဒ်ရလဒ်များ:
                """
                
                for i, result in enumerate(results_list[:3], 1):
                    title = result.get("title", "")
                    content = result.get("content", "")
                    url = result.get("url", "")
                    
                    content_to_analyze += f"""
                    {i}. {title}
                    အကြောင်းအရာ: {content[:200]}...
                    လင့်ခ်: {url}
                    
                    """
            else:
                # Extract content for analysis
                results_list = search_results.get("results", [])
                answer = search_results.get("answer", "")
                
                if not results_list and not answer:
                    content_to_analyze = f"""
                    ရှာဖွေတွေ့ရှိသောအကြောင်းအရာများ ({search_type}) - No Results:
                    
                    မေးခွန်း: {original_query}
                    
                    ရှာဖွေရလဒ်ရလဒ်များ: မရှိပါသည်။
                    """
                else:
                    # Prepare content for AI analysis
                    content_to_analyze = f"""
                    ရှာဖွေတွေ့ရှိသောအကြောင်းအရာများ ({search_type}):
                    
                    မေးခွန်း: {original_query}
                    
                    အဖြေရှင်းများ:
                    {answer}
                    
                    ရှာဖွေရလဒ်ရလဒ်များ:
                    """
                    
                    for i, result in enumerate(results_list[:5], 1):
                        title = result.get("title", "")
                        content = result.get("content", "")
                        url = result.get("url", "")
                        published_date = result.get("published_date", "")
                        
                        content_to_analyze += f"""
                        {i}. {title}
                        အကြောင်းအရာ: {content[:300]}...
                        ထုတ်ပြန်ချိန်: {published_date}
                        လင့်ခ်: {url}
                        
                        """
            
            # Generate strict Myanmar summary using Gemini
            if search_type == "sports":
                summary_prompt = f"""You are a professional News Reader and Summarizer. Your role is to READ and EXPLAIN search results in fluent Myanmar language, not just find and paste links. Never provide raw links as your primary answer.

                TWO-STEP PROCESS:
                Step 1 (Search): Search tool has found the news
                Step 2 (Summarize): Read ALL text from search results and write final response in Myanmar

                STRICT RESPONSE STRUCTURE:
                ခေါင်းစဉ်: [သတင်းခေါင်းစဉ်]
                
                အနှစ်ချုပ်: [အခြေအနေအရပ်ရပ်ကို မြန်မာလို အသေးစိတ် အသေးစိတ်]
                
                အချက်အလက်များ: [Bullet points ဖြင့် အရေးကြီးအချက်များပြရန်]

                CRITICAL REQUIREMENTS:
                - READ ALL content from search tool results
                - NEVER just list links
                - SYNTHESIZE answer from the content
                - Write in natural Myanmar language
                - Structure exactly as specified above

                ရှာဖွေရလဒ်ရလဒ်များ:
                {content_to_analyze}

                ယခုရှိသောအကြောင်းအရာများကို အပြည့်ဖတ်ပြီး မြန်မာဘာသာဖြင့် ရှင်းလင်းပေးပါ။"""
            
            elif search_type == "international":
                summary_prompt = f"""You are a professional News Reader and Summarizer. Your role is to READ and EXPLAIN search results in fluent Myanmar language, not just find and paste links. Never provide raw links as your primary answer.

                TWO-STEP PROCESS:
                Step 1 (Search): Search tool has found the news
                Step 2 (Summarize): Read ALL text from search results and write final response in Myanmar

                STRICT RESPONSE STRUCTURE:
                ခေါင်းစဉ်: [သတင်းခေါင်းစဉ်]
                
                အနှစ်ချုပ်: [အခြေအနေအရပ်ရပ်ကို မြန်မာလို အသေးစိတ် အသေးစိတ်]
                
                အချက်အလက်များ: [Bullet points ဖြင့် အရေးကြီးအချက်များပြရန်]

                CRITICAL REQUIREMENTS:
                - READ ALL content from search tool results
                - NEVER just list links
                - SYNTHESIZE answer from the content
                - Write in natural Myanmar language
                - Structure exactly as specified above

                ရှာဖွေရလဒ်ရလဒ်များ:
                {content_to_analyze}

                ယခုရှိသောအကြောင်းအရာများကို အပြည့်ဖတ်ပြီး မြန်မာဘာသာဖြင့် ရှင်းလင်းပေးပါ။"""
        
            elif search_type == "myanmar":
                summary_prompt = f"""You are a professional News Reader and Summarizer. Your role is to READ and EXPLAIN search results in fluent Myanmar language, not just find and paste links. Never provide raw links as your primary answer.

                TWO-STEP PROCESS:
                Step 1 (Search): Search tool has found the news
                Step 2 (Summarize): Read ALL text from search results and write final response in Myanmar

                STRICT RESPONSE STRUCTURE:
                ခေါင်းစဉ်: [သတင်းခေါင်းစဉ်]
                
                အနှစ်ချုပ်: [အခြေအနေအရပ်ရပ်ကို မြန်မာလို အသေးစိတ် အသေးစိတ်]
                
                အချက်အလက်များ: [Bullet points ဖြင့် အရေးကြီးအချက်များပြရန်]

                CRITICAL REQUIREMENTS:
                - READ ALL content from search tool results
                - NEVER just list links
                - SYNTHESIZE answer from the content
                - Write in natural Myanmar language
                - Structure exactly as specified above

                ရှာဖွေရလဒ်ရလဒ်များ:
                {content_to_analyze}

                ယခုရှိသောအကြောင်းအရာများကို အပြည့်ဖတ်ပြီး မြန်မာဘာသာဖြင့် ရှင်းလင်းပေးပါ။"""
        
            else:  # general
                summary_prompt = f"""You are a professional News Reader and Summarizer. Your role is to READ and EXPLAIN search results in fluent Myanmar language, not just find and paste links. Never provide raw links as your primary answer.

                TWO-STEP PROCESS:
                Step 1 (Search): Search tool has found the news
                Step 2 (Summarize): Read ALL text from search results and write final response in Myanmar

                STRICT RESPONSE STRUCTURE:
                ခေါင်းစဉ်: [သတင်းခေါင်းစဉ်]
                
                အနှစ်ချုပ်: [အခြေအနေအရပ်ရပ်ကို မြန်မာလို အသေးစိတ် အသေးစိတ်]
                
                အချက်အလက်များ: [Bullet points ဖြင့် အရေးကြီးအချက်များပြရန်]
                REQUIREMENTS:
                - READ all search results carefully
                - ANALYZE the content and extract key information
                - WRITE a cohesive summary in 100% Myanmar language
                - Structure exactly as specified above
                - No English content in the summary
                - Links only in Sources section at the bottom

                ရှာဖွေရလဒ်ရလဒ်များ:
                {content_to_analyze}

                ယခုရှိသောအကြောင်းအရာများကို ဖတ်ပြီး မြန်မာဘာသာဖြင့် ရှင်းလင်းပေးပါ။"""
        
        try:
            # Generate AI summary
            response = self.model.generate_content(summary_prompt)
            summary = response.text
            
            # Add source links at the very end
            links_section = "\n\n**[Sources]**\n"
            for i, result in enumerate(results_list[:5], 1):
                title = result.get("title", "")
                url = result.get("url", "")
                links_section += f"{i}. {title}: {url}\n"
            
            return summary + links_section
            
        except Exception as e:
            logger.error(f"Failed to generate AI summary: {str(e)}")
            return str(search_results)
        
        # Handle unexpected types
        else:
            logger.error(f"Unexpected search results type: {type(search_results)}")
            return f"❌ **ရှာဖွေမှုမအောင်မြင်ပါ**\n\nရှာဖွေရလဒ်အမျိုးအစားမမှန်ပါ: {type(search_results)}"
