import os
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

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
        
    def search_tavily(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Perform web search using Tavily API.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            Search results dictionary
        """
        if not self.api_key:
            return {
                "success": False,
                "error": "Tavily API key not configured",
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
            
            response = requests.post(
                f"{self.base_url}/search",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "success": False,
                    "error": f"API request failed: {response.status_code}",
                    "results": []
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Search failed: {str(e)}",
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
        Format search results for Myanmar language presentation.
        
        Args:
            results: Search results from Tavily API
            
        Returns:
            Formatted Myanmar language summary
        """
        if not results.get("success", False):
            return f"❌ ရှာဖွေမှုမအောင်မြင်ပါ: {results.get('error', 'အမည်မသိသောအမှား')}"
        
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
