from fastapi import APIRouter, UploadFile, File, Form, Depends
from app.services.enrichment_agent import EnrichmentAgent
from app.services.caption_service import CaptionService
from app.services.tagging_service import TaggingService
from app.services.mam_service import MockMAMClient
from app.core.config import get_settings, Settings

router = APIRouter()

# Dependency-injected factory function
def get_enrichment_agent(settings: Settings = Depends(get_settings)):
    return EnrichmentAgent(
        captioner=CaptionService(settings),
        tagger=TaggingService(settings.keywords),
        mam=MockMAMClient()
    )

@router.post("/enrich")
async def enrich_metadata(
    file: UploadFile = File(...),  # Should come from the "file upload field" of a multipart/form-data request, required
    asset_id: str = Form(...),  # Should come from the "asset_id" field of a multipart/form-data request, required
    agent: EnrichmentAgent = Depends(get_enrichment_agent)  # Dependency injection
):
    image_bytes = await file.read()
    result = agent.process(image_bytes, asset_id)
    return {"result": result}
