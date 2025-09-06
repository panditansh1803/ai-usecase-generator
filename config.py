import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for API keys and settings"""
    
    # API Keys - Get these from respective platforms
    TAVILY_API_KEY = os.getenv('TAVILY_API_KEY', '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')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyDmYw1Aj_1HnPKupL7dSV1fB9FDi6B-eDg')
    SERPER_API_KEY = os.getenv('SERPER_API_KEY', 'a8f9b832973daab2c56fd901d759619e98396ed5')
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '')
    
    # Search Configuration
    MAX_SEARCH_RESULTS = 10
    SEARCH_TIMEOUT = 30
    
    # Agent Configuration
    AGENT_TIMEOUT = 120
    MAX_RETRIES = 3
    
    # Output Configuration
    OUTPUT_DIR = 'outputs'
    LOG_LEVEL = 'INFO'
    
    # Model Configuration
    DEFAULT_MODEL = 'GEMINI'
    TEMPERATURE = 0.7
    MAX_TOKENS = 2000
    
    # Validation
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        missing_keys = []
        
        if not cls.TAVILY_API_KEY:
            missing_keys.append('TAVILY_API_KEY')
        
        if not cls.GEMINI_API_KEY and not cls.SERPER_API_KEY:
            missing_keys.append('GEMINI_API_KEY or SERPER_API_KEY')
        
        if missing_keys:
            raise ValueError(f"Missing required configuration: {', '.join(missing_keys)}")
        
        return True
    
    @classmethod
    def get_api_keys(cls):
        """Get dictionary of available API keys"""
        return {
            'tavily': cls.TAVILY_API_KEY,
            'openai': cls.GEMINI_API_KEY,
            'serper': cls.SERPER_API_KEY,
            'huggingface': cls.HUGGINGFACE_API_KEY
        }
    
    @classmethod
    def print_config_status(cls):
        """Print configuration status for debugging"""
        print("Configuration Status:")
        print(f"- Tavily API: {'✅' if cls.TAVILY_API_KEY else '❌'}")
        print(f"- OpenAI API: {'✅' if cls.GEMINI_API_KEY else '❌'}")
        print(f"- Serper API: {'✅' if cls.SERPER_API_KEY else '❌'}")
        print(f"- HuggingFace API: {'✅' if cls.HUGGINGFACE_API_KEY else '❌'}")
        print(f"- Output Directory: {cls.OUTPUT_DIR}")
        print(f"- Max Search Results: {cls.MAX_SEARCH_RESULTS}")

# Create output directory if it doesn't exist
import os
os.makedirs(Config.OUTPUT_DIR, exist_ok=True)