import os
import traceback
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

# Import Tavily SDK
try:
    from tavily import TavilyClient
    TAVILY_SDK_AVAILABLE = True
except ImportError:
    TAVILY_SDK_AVAILABLE = False
    logging.warning("Tavily SDK not installed. Please run: pip install tavily-python")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SearchTools:
    """
    Real-time search tools using Tavily API for web search.
    Supports sports news, international news, and general web search.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize SearchTools with Tavily API key.
        
        Args:
            api_key: Tavily API key (optional, uses env var if not provided)
        """
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        
        # Check if API key is available
        if not self.api_key:
            logger.error("TAVILY_API_KEY is missing from environment variables")
        else:
            logger.info(f"SearchTools initialized with Tavily API key (length: {len(self.api_key)})")
            logger.info(f"API Key starts with: {self.api_key[:10]}...")
        
        # Initialize Tavily client
        self.client = None
        if self.api_key and TAVILY_SDK_AVAILABLE:
            try:
                self.client = TavilyClient(api_key=self.api_key)
                logger.info("Tavily client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Tavily client: {str(e)}")
                logger.error(f"Traceback: {traceback.format_exc()}")
        
    def search_tavily(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Perform web search using Tavily Python SDK with robust error handling.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            Search results dictionary with detailed error information
        """
        # Check API key first
        if not self.api_key:
            error_msg = "API Key is missing in Environment"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "error_type": "missing_api_key",
                "results": []
            }
        
        # Check if Tavily SDK is available
        if not TAVILY_SDK_AVAILABLE:
            error_msg = "Tavily SDK not installed. Please run: pip install tavily-python"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "error_type": "sdk_missing",
                "results": []
            }
        
        # Check if client is initialized
        if not self.client:
            error_msg = "Tavily client not initialized"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "error_type": "client_not_initialized",
                "results": []
            }
        
        try:
            logger.info(f"Making Tavily search request for query: '{query}'")
            logger.info(f"Max results: {max_results}")
            
            # Use Tavily SDK search method
            response = self.client.search(
                query=query,
                max_results=max_results,
                include_answer=True,
                include_raw_content=False,
                search_depth="basic"
            )
            
            logger.info("Tavily search request successful")
            logger.info(f"Response keys: {list(response.keys()) if isinstance(response, dict) else 'Not a dict'}")
            
            # Ensure response has expected structure
            if isinstance(response, dict):
                response["success"] = True
                return response
            else:
                logger.error(f"Unexpected response type: {type(response)}")
                return {
                    "success": False,
                    "error": f"Unexpected response type: {type(response)}",
                    "error_type": "unexpected_response_type",
                    "results": []
                }
                
        except Exception as e:
            error_msg = str(e)
            error_type = "unknown"
            
            # Log full traceback for debugging
            logger.error(f"Search failed with exception: {error_msg}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            
            # Try to identify specific error types
            if "401" in error_msg or "unauthorized" in error_msg.lower() or "authentication" in error_msg.lower():
                error_type = "authentication_error"
                error_msg = f"Invalid API key - authentication failed: {error_msg}"
            elif "429" in error_msg or "rate limit" in error_msg.lower() or "quota" in error_msg.lower():
                error_type = "rate_limit_error"
                error_msg = f"API rate limit exceeded: {error_msg}"
            elif "402" in error_msg or "payment required" in error_msg.lower():
                error_type = "payment_required"
                error_msg = f"Payment required - quota exceeded: {error_msg}"
            elif "400" in error_msg or "bad request" in error_msg.lower():
                error_type = "bad_request"
                error_msg = f"Bad request - invalid query parameters: {error_msg}"
            elif "timeout" in error_msg.lower():
                error_type = "timeout_error"
                error_msg = f"Request timeout: {error_msg}"
            elif "connection" in error_msg.lower():
                error_type = "connection_error"
                error_msg = f"Connection error: {error_msg}"
            else:
                error_type = "unexpected_error"
                error_msg = f"Unexpected error: {error_msg}"
            
            return {
                "success": False,
                "error": error_msg,
                "error_type": error_type,
                "results": []
            }
    
    def search_sports_news(self, sport: str = "football", max_results: int = 5) -> Dict[str, Any]:
        """
        Search for latest sports news.
        
        Args:
            sport: Sport type (football, basketball, tennis, etc.)
            max_results: Maximum number of results
            
        Returns:
            Sports news results
        """
        query = f"latest {sport} news today sports updates"
        return self.search_tavily(query, max_results)
    
    def search_international_news(self, region: str = "global", max_results: int = 5) -> Dict[str, Any]:
        """
        Search for international news.
        
        Args:
            region: Region focus (asia, europe, global, etc.)
            max_results: Maximum number of results
            
        Returns:
            International news results
        """
        query = f"latest international news {region} today world updates"
        return self.search_tavily(query, max_results)
    
    def search_myanmar_news(self, max_results: int = 5) -> Dict[str, Any]:
        """
        Search for Myanmar-specific news.
        
        Args:
            max_results: Maximum number of results
            
        Returns:
            Myanmar news results
        """
        query = "Myanmar news today latest updates မြန်မာသတင်း"
        return self.search_tavily(query, max_results)
    
    def format_results_for_myanmar(self, results: Dict[str, Any]) -> str:
        """
        Format search results for Myanmar language presentation with enhanced error handling.
        
        Args:
            results: Search results from Tavily API
            
        Returns:
            Formatted Myanmar language summary with detailed error information
        """
        # Check if results is None or empty first
        if not results:
            error_msg = "No response received from search API"
            logger.error("Empty or None response from search API")
            return f"❌ **ရှာဖွေမှုမအောင်မြင်ပါ**\n\n{error_msg}"
        
        # Check if search was successful
        if not results.get("success", False):
            error_type = results.get("error_type", "unknown")
            error_msg = results.get("error", "အမည်မသိသောအမှား")
            status_code = results.get("status_code")
            api_response = results.get("api_response", "")
            
            # Log error for debugging
            logger.error(f"Search failed - Type: {error_type}, Message: {error_msg}, Status: {status_code}")
            
            # Print API key status for debugging
            api_key_status = "Available" if self.api_key else "Missing"
            logger.info(f"API Key Status: {api_key_status}")
            logger.info(f"API Key Value: {self.api_key[:10] + '...' if self.api_key else 'None'}")
            
            # Format user-friendly error messages in Myanmar (enhanced for free tier users)
            error_messages = {
                "missing_api_key": "❌ **API Key ပျောက်နေပါသည်**\n\nTAVILY_API_KEY ကို environment variables ထဲမှာ ထည့်ပေးပါ။\n\nFree tier အတွက် Tavily မှ API key ရယူရန်: https://tavily.com/",
                "sdk_missing": "❌ **Tavily SDK မရှိပါ**\n\nTavily Python SDK ကို install လုပ်ရန်လိုအပ်ပါသည်။\n\nအောက်က command ကို run ပါ: pip install tavily-python",
                "client_not_initialized": "❌ **Tavily Client မစလုပ်နိုင်ပါ**\n\nTavily client ကို initialize လုပ်ရာတွင်အမှားဖြစ်ပါသည်။\n\nAPI key ကိုစစ်ဆေးပြီး ပြန်ကြိုးစားပါ။",
                "authentication_error": "❌ **API Key မှားနေပါသည် (401)**\n\nTavily API key ကို စစ်ဆေးပြီး မှန်ကန်သော key ကို ထည့်ပေးပါ။\n\nFree tier သုံးပါက key ကို ပြန်လည်စစ်ဆေးပါ။",
                "rate_limit_error": "❌ **Free Tier Quota ပြည့်သွားပါသည် (429)**\n\nTavily Free tier ရဲ့ လစဉ်အသုံးပြုနှုန်းပြည့်သွားပါပြီ။\n\nအဖြေရှင်းများ:\n- ခဏအကြာပြန်လည်ကြိုးစားပါ (မိနစ်အနည်းငယ်စောင့်ပါ)\n- Free tier ကို upgrade လုပ်ပါက ပိုမိုအသုံးပြုနိုင်ပါသည်\n- နောက်ထပ် ရက်များတွင် ပြန်လည်ကြိုးစားပါ",
                "payment_required": "❌ **Free Tier Quota ကုန်ဆုံးသွားပါသည် (402)**\n\nTavily Free tier ရဲ့ လစဉ် quota ကုန်ဆုံးသွားပါပြီ။\n\nအဖြေရှင်းများ:\n- နောက်ထပ် ရက်များတွင် ပြန်လည်ကြိုးစားပါ (quota ပြန်ဖြည့်ပါသည်)\n- Paid plan သို့ upgrade လုပ်ပါက ပိုမိုအသုံးပြုနိုင်ပါသည်\n- ယခုလအတွင်း ပြန်လည်ကြိုးစားမပါနှင့်",
                "bad_request": "❌ **တောင်းဆိုမှုမှားနေပါသည် (400)**\n\nရှာဖွေစရာကို ပြန်စစ်ဆေးပြီး ကြိုးစားပါ။\n\nအကြံပြုချက်: ရိုးရှင်းသော keywords များကို အသုံးပြုပါ။",
                "timeout_error": "❌ **တောင်းဆိုမှုကြာနေပါသည်**\n\nအင်တာနက်ချိတ်ဆက်မှုကို စစ်ဆေးပြီး ပြန်ကြိုးစားပါ။\n\nFree tier တွင် တစ်ခါလစ် နှေးနိုင်ပါသည်။",
                "connection_error": "❌ **ချိတ်ဆက်မှုပြဿနာ**\n\nအင်တာနက်ချိတ်ဆက်မှုကို စစ်ဆေးပါ။\n\nTavily API server များကို ရောက်နိုင်မရောက် စစ်ဆေးပါ။",
                "request_error": f"❌ **တောင်းဆိုမှုအမှား**\n\n{error_msg}",
                "api_error": f"❌ **API အမှား ({status_code})**\n\n{error_msg}\n\nFree tier အတွက် တချို့ API ကန့်သတ်ချက်များ ှိနိုင်ပါသည်။",
                "unexpected_response_type": f"❌ **API Response Type မမှန်ပါ**\n\n{error_msg}\n\nAPI ကပြန်လာတဲ့ response type မှားနေပါသည်။",
                "unexpected_error": f"❌ **မမျှော်လင့်ထားသောအမှား**\n\n{error_msg}\n\nFree tier တွင် ဖြစ်တတ်သော ပြဿနာဖြစ်နိုင်ပါသည်။"
            }
            
            # Get the appropriate error message
            user_error_msg = error_messages.get(error_type, f"❌ **API ကပြန်လာတဲ့ Error: {error_type}**\n\nအမှားအကြောင်းရင်းခံ: {error_msg}")
            
            # Add technical details for debugging (if available)
            if status_code:
                user_error_msg += f"\n\n**နည်းပညာအသေးစိတ်:**\n- Status Code: {status_code}"
            if api_response and len(api_response) < 200:
                user_error_msg += f"\n- API Response: {api_response}"
            
            # Add API key debugging info
            user_error_msg += f"\n\n**Debugging Info:**\n- API Key Status: {api_key_status}"
            if self.api_key:
                user_error_msg += f"\n- API Key Length: {len(self.api_key)} chars"
            
            return user_error_msg
        
        formatted_output = []
        formatted_output.append("🔍 **ရှာဖွေတွေ့ရှိသောအကြောင်းအရာများ**")
        formatted_output.append(f"📅 ရှာဖွေခဲ့သည့်ရက်စွဲ: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        formatted_output.append("")
        
        # Add answer if available
        if results.get("answer"):
            formatted_output.append("💡 **အဓိပ္ပာယ်ဖွင့်ဆိုချက်:**")
            formatted_output.append(results["answer"])
            formatted_output.append("")
        
        # Add results
        results_list = results.get("results", [])
        if results_list:
            formatted_output.append("📰 **အဓိကသတင်းများ:**")
            formatted_output.append("")
            
            for i, result in enumerate(results_list[:5], 1):
                title = result.get("title", "ခေါင်းစဉ်မရှိ")
                url = result.get("url", "")
                content = result.get("content", "")[:200] + "..." if len(result.get("content", "")) > 200 else result.get("content", "")
                published_date = result.get("published_date", "")
                
                formatted_output.append(f"**{i}. {title}**")
                if published_date:
                    formatted_output.append(f"📅 ထုတ်ပြန်ချိန်: {published_date}")
                formatted_output.append(f"📄 အကြောင်းအရာ: {content}")
                formatted_output.append(f"🔗 လင့်ခ်: {url}")
                formatted_output.append("")
        else:
            formatted_output.append("❌ ရှာဖွေရလဒ်များမရှိပါ။")
        
        return "\n".join(formatted_output)

# Convenience functions
def search_web(query: str, api_key: Optional[str] = None) -> str:
    """
    Convenience function for web search.
    
    Args:
        query: Search query
        api_key: Tavily API key
        
    Returns:
        Formatted search results in Myanmar
    """
    search_tool = SearchTools(api_key)
    results = search_tool.search_tavily(query)
    return search_tool.format_results_for_myanmar(results)

def search_sports(sport: str = "football", api_key: Optional[str] = None) -> str:
    """
    Convenience function for sports news search.
    
    Args:
        sport: Sport type
        api_key: Tavily API key
        
    Returns:
        Formatted sports news in Myanmar
    """
    search_tool = SearchTools(api_key)
    results = search_tool.search_sports_news(sport)
    return search_tool.format_results_for_myanmar(results)

def search_international_news(region: str = "global", api_key: Optional[str] = None) -> str:
    """
    Convenience function for international news search.
    
    Args:
        region: Region focus
        api_key: Tavily API key
        
    Returns:
        Formatted international news in Myanmar
    """
    search_tool = SearchTools(api_key)
    results = search_tool.search_international_news(region)
    return search_tool.format_results_for_myanmar(results)

def search_myanmar_news(api_key: Optional[str] = None) -> str:
    """
    Convenience function for Myanmar news search.
    
    Args:
        api_key: Tavily API key
        
    Returns:
        Formatted Myanmar news in Myanmar
    """
    search_tool = SearchTools(api_key)
    results = search_tool.search_myanmar_news()
    return search_tool.format_results_for_myanmar(results)
