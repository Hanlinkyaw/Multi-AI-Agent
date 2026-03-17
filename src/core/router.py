from typing import Dict, List, Optional, Any
from ..agents.base_agent import BaseAgent
from ..agents.research_agent import ResearchAgent
from ..agents.devops_agent import DevOpsAgent

class AgentRouter:
    def __init__(self, api_key: Optional[str] = None):
        """
        Router for directing messages to appropriate agents based on intent detection.
        """
        self.api_key = api_key
        self.agents: Dict[str, BaseAgent] = {}
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all available agents."""
        try:
            self.agents["research"] = ResearchAgent(self.api_key)
            self.agents["devops"] = DevOpsAgent(self.api_key)
            self.agents["general"] = GeneralAgent(self.api_key)
        except Exception as e:
            print(f"❌ Agent initialization error: {e}")
    
    def route_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Route message to the most appropriate agent.
        
        Args:
            message: User message to route
            context: Additional context for routing
            
        Returns:
            Dictionary with agent response and metadata
        """
        try:
            # Detect intent and select agent
            selected_agent = self._select_agent(message)
            
            if not selected_agent:
                return {
                    "success": False,
                    "error": "No suitable agent found",
                    "message": "တောင်းဆိုမှုကို handle လုပ်နိုင်သော agent မရှိပါ"
                }
            
            # Process message with selected agent
            response = selected_agent.process_message(message, context)
            
            return {
                "success": True,
                "agent": selected_agent.name,
                "agent_type": selected_agent.get_agent_type(),
                "response": response,
                "model": selected_agent.model.get_model_name()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Message routing တွင် error ဖြစ်ပါသည်: {str(e)}"
            }
    
    def _select_agent(self, message: str) -> Optional[BaseAgent]:
        """
        Select the most appropriate agent based on message content.
        Priority order: Research > DevOps > General
        """
        # Check for research intent first
        if "research" in self.agents and self.agents["research"].can_handle(message):
            return self.agents["research"]
        
        # Check for DevOps intent second
        if "devops" in self.agents and self.agents["devops"].can_handle(message):
            return self.agents["devops"]
        
        # Default to general agent
        if "general" in self.agents:
            return self.agents["general"]
        
        return None
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents."""
        status = {
            "total_agents": len(self.agents),
            "agents": {}
        }
        
        for agent_name, agent in self.agents.items():
            status["agents"][agent_name] = agent.get_info()
        
        return status
    
    def add_agent(self, agent_type: str, agent: BaseAgent):
        """Add a new agent to the router."""
        self.agents[agent_type] = agent
    
    def remove_agent(self, agent_type: str) -> bool:
        """Remove an agent from the router."""
        if agent_type in self.agents:
            del self.agents[agent_type]
            return True
        return False


class GeneralAgent(BaseAgent):
    """
    General purpose agent for handling non-specialized conversations.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        system_prompt = """သင်သည် General AI Assistant ဖြစ်ပါသည်။ သင်၏တာဝန်မှာ အထွေထွေစကားပြောဆိုခြင်း၊ 
        အကူအညီပေးခြင်း၊ နှင့် အခြား specialized agents များမှ handle မလုပ်နိုင်သော 
        တောင်းဆိုမှုများကို တုံ့ပြန်ခြင်းဖြစ်သည်။

        သင့်လုပ်ဆောင်နိုင်သောအရာများ:
        - အထွေထွေစကားပြောဆိုခြင်း
        - အကူအညီတောင်းဆိုခြင်း
        - အချက်အလက်ရှင်းလင်းချက်ပေးခြင်း
        - လမ်းညွှန်ချက်ပေးခြင်း

        အသုံးပြုသော language များ:
        - Myanmar (မြန်မာဘာသာ) - အဓိက
        - English

        တုံ့ပြန်ပုံစံ:
        - ရိုင်းရင်းပြီး ကောင်းမွန်စွာတုံ့ပြန်ပါ
        - အကယ်၍ specialized help လိုအပ်ပါက၊ သက်ဆိုင်ရာ agent ကို ညွှန်ပြပါ
        - အကူအညီပေးနိုင်သမျှ ကူညီပါ"""
        
        super().__init__(
            name="General Agent",
            system_prompt=system_prompt,
            api_key=api_key
        )
    
    def get_agent_type(self) -> str:
        return "general"
    
    def can_handle(self, message: str) -> bool:
        """General agent can handle any message."""
        return True  # Always returns True as fallback
