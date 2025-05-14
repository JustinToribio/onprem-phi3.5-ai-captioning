from app.utils.image_io import load_image_from_bytes

class EnrichmentAgent:
    def __init__(self, captioner, tagger, mam):
        self.captioner = captioner
        self.tagger = tagger
        self.mam = mam

    def process(self, image_bytes: bytes, asset_id: str):
        reasoning_trace = ["Caption generated using visual features and prompt context."]
        image = load_image_from_bytes(image_bytes)
        caption = self.captioner.generate_caption(image)

        # If caption is None or too short, try again with verbose mode
        if not caption or len(caption.split()) < 15:
            print("Caption too short, trying verbose mode.")
            reasoning_trace.append(f"Initial caption: {caption}")
            reasoning_trace.append("Caption was short, so a second attempt was made using verbose mode.")
            caption = self.captioner.generate_caption(image, verbose=True)

        tags = self.tagger.extract_tags(caption)
        metadata = {
            "caption": caption,
            "tags": tags,
            "source": "phi3.5",
            "reasoning_trace": reasoning_trace,
        }
        self.mam.push_metadata(asset_id, metadata)
        return metadata
