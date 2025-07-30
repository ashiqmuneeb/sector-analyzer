import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()

def get_gemini_api_key():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        logger.error("GEMINI_API_KEY not found in environment variables")
        raise ValueError("GEMINI_API_KEY environment variable not set")
    return key