import os, json
from typing import Dict, Any
from openai import OpenAI
from ..config import get_difficulty_profile

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))