from app.services.inference import run_caption_inference
from app.core.config import Settings

class CaptionService:
    def __init__(self, settings: Settings):
        self.prompt_basic = settings.user_prompt
        self.prompt_verbose = settings.user_prompt_verbose
        self.max_tokens = settings.max_tokens
        self.model_id = settings.model_id
        self.test_mode = settings.test_mode

    def generate_caption(self, image, verbose=False):
        user_prompt = self.prompt_verbose if verbose else self.prompt_basic
        return run_caption_inference(
            image, user_prompt, self.model_id, self.max_tokens, test_mode=self.test_mode, verbose=verbose
            )
