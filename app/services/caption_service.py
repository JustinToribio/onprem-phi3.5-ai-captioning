from app.services.inference import run_caption_inference

class CaptionService:
    def generate_caption(self, image):
        return run_caption_inference(image)
