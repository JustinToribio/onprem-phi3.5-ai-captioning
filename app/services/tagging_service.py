from app.core.config import KEYWORDS

class TaggingService:
    def extract_tags(self, caption: str):
        tags = []
        for tag, words in KEYWORDS.items():
            if any(word in caption.lower() for word in words):
                tags.append(tag)
        return tags
