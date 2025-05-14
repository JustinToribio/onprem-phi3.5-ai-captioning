from app.services.inference import run_caption_inference
from app.core.config import Settings

class CaptionService:
    def __init__(self, settings: Settings):
        self.prompt = settings.user_prompt
        self.model_id = settings.model_id
        self.test_mode = settings.test_mode

    def generate_caption(self, image):
        return run_caption_inference(image, self.prompt, self.model_id, test_mode=self.test_mode)
