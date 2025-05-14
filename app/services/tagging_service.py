class TaggingService:
    def __init__(self, keywords: dict):
        self.keywords = keywords

    def extract_tags(self, caption: str):
        tags = []
        for tag, words in self.keywords.items():
            if any(word in caption.lower() for word in words):
                tags.append(tag)
        return tags
