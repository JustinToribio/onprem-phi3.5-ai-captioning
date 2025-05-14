from pydantic_settings import BaseSettings
from typing import Dict, List

# Apply configs with dependency injection
class Settings(BaseSettings):
    model_id: str = "microsoft/Phi-3.5-vision-instruct"
    user_prompt: str = "Describe what is shown in this image."
    user_prompt_verbose: str = "You are a metadata expert. Provide a detailed description of this image with rich context."
    max_tokens: int = 20
    test_mode: bool = False

    keywords: Dict[str, List[str]] = {
        "sports": ["basketball", "football", "snowboarding"],
        "automobiles": ["car", "truck", "van"],
        "toys": ["teddy", "yo-yo", "kite"],
        "test": ["solid red"]
    }

def get_settings():
    return Settings()
