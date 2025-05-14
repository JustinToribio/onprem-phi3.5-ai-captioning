from app.services.caption_service import CaptionService
from app.services.tagging_service import TaggingService
from app.services.mam_service import MockMAMClient
from app.utils.image_io import load_image_from_bytes

class EnrichmentAgent:
    def __init__(self):
        self.captioner = CaptionService()
        self.tagger = TaggingService()
        self.mam = MockMAMClient()

    def process(self, image_bytes: bytes, asset_id: str):
        image = load_image_from_bytes(image_bytes)
        caption = self.captioner.generate_caption(image)
        tags = self.tagger.extract_tags(caption)
        metadata = {
            "caption": caption,
            "tags": tags,
            "source": "phi3.5"
        }
        self.mam.push_metadata(asset_id, metadata)
        return metadata
