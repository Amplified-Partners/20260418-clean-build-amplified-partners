"""
Research Pipe Configuration
Centralized config: API keys, model names, endpoints.
"""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    def load_dotenv(path):
        """Stub if dotenv not available."""
        pass

# Paths
BASE = Path.home() / "amplified"
CONFIG_ENV = Path.home() / ".config" / "amplified" / ".env"

# Load environment
load_dotenv(CONFIG_ENV)

class ResearchPipeConfig:
    """Configuration for the research pipe."""
    
    # API Keys
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    EXA_API_KEY = os.getenv("EXA_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    
    # Models
    HAIKU_MODEL = "claude-opus-4-1"
    QWEN_MODEL = "qwen2.5:14b"
    
    # Ollama (local)
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    
    # API Endpoints
    EXA_ENDPOINT = "https://api.exa.ai/search"
    ARXIV_ENDPOINT = "http://export.arxiv.org/api/query"
    TAVILY_ENDPOINT = "https://api.tavily.com/search"
    
    # File paths
    OUTPUT_AUDIT_TRAILS = BASE / "output_audit_trails"
    PROMPTS_DIR = BASE
    
    # Constraints
    MAX_RESULTS_PER_SEARCH = 100
    MAX_AUDIT_TRAIL_RESULTS = 20
    JSON_ONLY = True


def get_config():
    """Return the config singleton."""
    return ResearchPipeConfig()
