from pydantic_settings import BaseSettings
from typing import Dict, List

# Apply configs with dependency injection
class Settings(BaseSettings):
    model_id: str = "microsoft/Phi-3.5-vision-instruct"
    user_prompt: str = "Describe what is shown in this image."
    keywords: Dict[str, List[str]] = {
        "sports": ["basketball", "football", "snowboarding"],
        "automobiles": ["car", "truck", "van"],
        "toys": ["teddy", "yo-yo", "kite"],
        "test": ["no variations"]
    }

def get_settings():
    return Settings()
