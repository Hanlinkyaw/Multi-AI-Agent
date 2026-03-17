import os
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import logging

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
        self.base_url = "https://api.tavily.com"
        
        # Check if API key is available
        if not self.api_key:
            logger.error("TAVILY_API_KEY is missing from environment variables")
        else:
            logger.info("SearchTools initialized with Tavily API key")
        
    def search_tavily(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Perform web search using Tavily API with enhanced error handling.
        
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
        
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "api_key": self.api_key,
                "query": query,
                "search_depth": "basic",
                "include_answer": True,
                "include_raw_content": False,
                "max_results": max_results,
                "include_domains": [],
                "exclude_domains": []
            }
            
            logger.info(f"Making search request for query: '{query}'")
            
            response = requests.post(
                f"{self.base_url}/search",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info("Search request successful")
                return response.json()
            elif response.status_code == 401:
                error_msg = "Invalid API key - authentication failed"
                logger.error(f"Authentication error: {response.text}")
                return {
                    "success": False,
                    "error": error_msg,
                    "error_type": "authentication_error",
                    "status_code": response.status_code,
                    "api_response": response.text,
                    "results": []
                }
            elif response.status_code == 429:
                error_msg = "API rate limit exceeded - please try again later"
                logger.error(f"Rate limit error: {response.text}")
                return {
                    "success": False,
                    "error": error_msg,
                    "error_type": "rate_limit_error",
                    "status_code": response.status_code,
                    "api_response": response.text,
                    "results": []
                }
            elif response.status_code == 402:
                error_msg = "Payment required - quota exceeded"
                logger.error(f"Payment required error: {response.text}")
                return {
                    "success": False,
                    "error": error_msg,
                    "error_type": "payment_required",
                    "status_code": response.status_code,
                    "api_response": response.text,
                    "results": []
                }
            elif response.status_code == 400:
                error_msg = "Bad request - invalid query parameters"
                logger.error(f"Bad request error: {response.text}")
                return {
                    "success": False,
                    "error": error_msg,
                    "error_type": "bad_request",
                    "status_code": response.status_code,
                    "api_response": response.text,
                    "results": []
                }
            else:
                error_msg = f"API request failed with status code {response.status_code}"
                logger.error(f"API error {response.status_code}: {response.text}")
                return {
                    "success": False,
                    "error": error_msg,
                    "error_type": "api_error",
                    "status_code": response.status_code,
                    "api_response": response.text,
                    "results": []
                }
                
        except requests.exceptions.Timeout:
            error_msg = "Search request timed out - please try again"
            logger.error("Request timeout error")
            return {
                "success": False,
                "error": error_msg,
                "error_type": "timeout_error",
                "results": []
            }
        except requests.exceptions.ConnectionError:
            error_msg = "Connection error - unable to reach Tavily API"
            logger.error("Connection error")
            return {
                "success": False,
                "error": error_msg,
                "error_type": "connection_error",
                "results": []
            }
        except requests.exceptions.RequestException as e:
            error_msg = f"Request error: {str(e)}"
            logger.error(f"Request exception: {str(e)}")
            return {
                "success": False,
                "error": error_msg,
                "error_type": "request_error",
                "results": []
            }
        except Exception as e:
            error_msg = f"Unexpected error during search: {str(e)}"
            logger.error(f"Unexpected error: {str(e)}")
            return {
                "success": False,
                "error": error_msg,
                "error_type": "unexpected_error",
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
                "authentication_error": "❌ **API Key မှားနေပါသည် (401)**\n\nTavily API key ကို စစ်ဆေးပြီး မှန်ကန်သော key ကို ထည့်ပေးပါ။\n\nFree tier သုံးပါက key ကို ပြန်လည်စစ်ဆေးပါ။",
                "rate_limit_error": "❌ **Free Tier Quota ပြည့်သွားပါသည် (429)**\n\nTavily Free tier ရဲ့ လစဉ်အသုံးပြုနှုန်းပြည့်သွားပါပြီ။\n\nအဖြေရှင်းများ:\n- ခဏအကြာပြန်လည်ကြိုးစားပါ (မိနစ်အနည်းငယ်စောင့်ပါ)\n- Free tier ကို upgrade လုပ်ပါက ပိုမိုအသုံးပြုနိုင်ပါသည်\n- နောက်ထပ် ရက်များတွင် ပြန်လည်ကြိုးစားပါ",
                "payment_required": "❌ **Free Tier Quota ကုန်ဆုံးသွားပါသည် (402)**\n\nTavily Free tier ရဲ့ လစဉ် quota ကုန်ဆုံးသွားပါပြီ။\n\nအဖြေရှင်းများ:\n- နောက်ထပ် ရက်များတွင် ပြန်လည်ကြိုးစားပါ (quota ပြန်ဖြည့်ပါသည်)\n- Paid plan သို့ upgrade လုပ်ပါက ပိုမိုအသုံးပြုနိုင်ပါသည်\n- ယခုလအတွင်း ပြန်လည်ကြိုးစားမပါနှင့်",
                "bad_request": "❌ **တောင်းဆိုမှုမှားနေပါသည် (400)**\n\nရှာဖွေစရာကို ပြန်စစ်ဆေးပြီး ကြိုးစားပါ။\n\nအကြံပြုချက်: ရိုးရှင်းသော keywords များကို အသုံးပြုပါ။",
                "timeout_error": "❌ **တောင်းဆိုမှုကြာနေပါသည်**\n\nအင်တာနက်ချိတ်ဆက်မှုကို စစ်ဆေးပြီး ပြန်ကြိုးစားပါ။\n\nFree tier တွင် တစ်ခါလစ် နှေးနိုင်ပါသည်။",
                "connection_error": "❌ **ချိတ်ဆက်မှုပြဿနာ**\n\nအင်တာနက်ချိတ်ဆက်မှုကို စစ်ဆေးပါ။\n\nTavily API server များကို ရောက်နိုင်မရောက် စစ်ဆေးပါ။",
                "request_error": f"❌ **တောင်းဆိုမှုအမှား**\n\n{error_msg}",
                "api_error": f"❌ **API အမှား ({status_code})**\n\n{error_msg}\n\nFree tier အတွက် တချို့ API ကန့်သတ်ချက်များ ှိနိုင်ပါသည်။",
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
