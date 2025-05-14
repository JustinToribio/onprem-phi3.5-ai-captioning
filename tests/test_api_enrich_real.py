import io
from fastapi.testclient import TestClient
from app.core.config import get_settings
from PIL import Image
from app.main import app


def test_enrich_endpoint_real_model():
    # Confirm the app is running in test mode
    settings = get_settings()
    print("Test mode:", settings.test_mode)

    # Tiny 1x1 red image (minimizes inference time)
    image = Image.new("RGB", (1, 1), color=(255, 0, 0))
    image_bytes = io.BytesIO()  # Create an in-memory binary stream
    image.save(image_bytes, format="PNG")  # Save the image to the binary stream
    image_bytes.seek(0)  # Rewind the stream to the beginning

    client = TestClient(app)
    response = client.post(
        "/api/enrich",
        files={"file": ("tiny.png", image_bytes, "image/png")},
        data={"asset_id": "real123"}
    )

    assert response.status_code == 200
    result = response.json()["result"]

    # Validate expected keys — content will vary slightly
    assert "caption" in result
    assert "tags" in result
    assert result["source"] == "phi3.5"

    print("Generated caption:", result["caption"])
    print("Generated tags:", result["tags"])
    print("Source:", result["source"])    
