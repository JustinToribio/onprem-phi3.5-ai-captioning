from fastapi import APIRouter, UploadFile, File, Form
from app.services.enrichment_agent import EnrichmentAgent

router = APIRouter()

@router.post("/enrich")
async def enrich_metadata(
    file: UploadFile = File(...),  # Should come from the "file upload field" of a multipart/form-data request, required
    asset_id: str = Form(...)  # Should come from the "asset_id" field of a multipart/form-data request, required
):
    image_bytes = await file.read()
    agent = EnrichmentAgent()
    result = agent.process(image_bytes, asset_id)
    return {"result": result}
