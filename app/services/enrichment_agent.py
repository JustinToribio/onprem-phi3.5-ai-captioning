from app.utils.image_io import load_image_from_bytes

class EnrichmentAgent:
    def __init__(self, captioner, tagger, mam):
        self.captioner = captioner
        self.tagger = tagger
        self.mam = mam

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
