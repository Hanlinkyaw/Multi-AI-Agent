from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import os
from src.core.model import GeminiModel

class BaseAgent(ABC):
    def __init__(self, name: str, system_prompt: str, api_key: Optional[str] = None):
        """
        Base class for all agents in the multi-agent system.
        
        Args:
            name: Agent identifier
            system_prompt: System prompt for the agent
            api_key: Gemini API key (optional, uses env var if not provided)
        """
        self.name = name
        self.system_prompt = system_prompt
        self.model = GeminiModel(api_key)
        
    @abstractmethod
    def get_agent_type(self) -> str:
        """Return the type of agent."""
        pass
    
    @abstractmethod
    def can_handle(self, message: str) -> bool:
        """Check if this agent can handle the given message."""
        pass
    
    def process_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Process a message using the agent's specialized capabilities.
        
        Args:
            message: User message to process
            context: Additional context for processing
            
        Returns:
            Agent response
        """
        try:
            # Build the full prompt with system message
            full_prompt = self._build_prompt(message, context)
            
            # Generate response using Gemini
            response = self.model.generate_response(full_prompt)
            
            return response
            
        except Exception as e:
            return f"❌ {self.name} တွင် error ဖြစ်ပါသည်: {str(e)}"
    
    def _build_prompt(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Build the complete prompt for the AI model.
        
        Args:
            message: User message
            context: Additional context
            
        Returns:
            Complete prompt
        """
        prompt_parts = [
            f"System: {self.system_prompt}",
            f"User: {message}"
        ]
        
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
            prompt_parts.insert(-1, f"Context: {context_str}")
        
        return "\n\n".join(prompt_parts)
    
    def get_info(self) -> Dict[str, str]:
        """Get agent information."""
        return {
            "name": self.name,
            "type": self.get_agent_type(),
            "model": self.model.get_model_name()
        }
