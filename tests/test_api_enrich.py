import io
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from PIL import Image
from app.main import app
from app.services.enrichment_agent import EnrichmentAgent
from app.api.routes_agent import get_enrichment_agent


def override_enrichment_agent():
    mock_captioner = MagicMock()
    mock_tagger = MagicMock()
    mock_mam = MagicMock()

    mock_captioner.generate_caption.return_value = "A red square"
    mock_tagger.extract_tags.return_value = ["test"]

    return EnrichmentAgent(
        captioner=mock_captioner,
        tagger=mock_tagger,
        mam=mock_mam
    )


def test_enrich_endpoint_with_mocked_agent():
    # Override the real agent with a mocked version
    app.dependency_overrides[get_enrichment_agent] = override_enrichment_agent

    # Create an in-memory image file
    image = Image.new("RGB", (1, 1), color=(255, 0, 0))
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    client = TestClient(app)
    response = client.post(
        "/api/enrich",
        files={"file": ("test.png", image_bytes, "image/png")},
        data={"asset_id": "test123"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "result": {
            "caption": "A red square",
            "tags": ["test"],
            "source": "phi3.5"
        }
    }

    # Clean up override
    app.dependency_overrides.clear()
