from unittest.mock import MagicMock
from app.services.enrichment_agent import EnrichmentAgent
from PIL import Image
import io

def test_enrichment_agent_process():
    # Arrange: Create mocks
    mock_captioner = MagicMock()
    mock_tagger = MagicMock()
    mock_mam = MagicMock()

    # Set return values
    mock_captioner.generate_caption.return_value = "A teddy bear playing basketball"
    mock_tagger.extract_tags.return_value = ["sports", "toys"]

    # Create a 1x1 red PNG image
    image = Image.new("RGB", (1, 1), color=(255, 0, 0))
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    dummy_image_bytes = buf.getvalue()

    # Dummy asset ID
    asset_id = "asset_123"

    # Instantiate agent with mocks
    agent = EnrichmentAgent(
        captioner=mock_captioner,
        tagger=mock_tagger,
        mam=mock_mam
    )

    # Act
    result = agent.process(dummy_image_bytes, asset_id)

    # Assert
    mock_captioner.generate_caption.assert_called_once()
    mock_tagger.extract_tags.assert_called_once_with("A teddy bear playing basketball")
    mock_mam.push_metadata.assert_called_once_with(asset_id, {
        "caption": "A teddy bear playing basketball",
        "tags": ["sports", "toys"],
        "source": "phi3.5"
    })

    assert result == {
        "caption": "A teddy bear playing basketball",
        "tags": ["sports", "toys"],
        "source": "phi3.5"
    }
