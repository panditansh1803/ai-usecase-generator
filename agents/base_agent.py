from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

class BaseAgent(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.logger = logging.getLogger(name)
        
    @abstractmethod
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's main task"""
        pass
    
    def log_info(self, message: str):
        self.logger.info(f"[{self.name}] {message}")