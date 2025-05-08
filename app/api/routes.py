from fastapi import APIRouter, File, UploadFile, HTTPException
from app.utils.image_io import load_image_from_bytes
from app.services.inference import run_caption_inference

router = APIRouter()

@router.post("/infer")
async def infer_image(file: UploadFile = File(...)):
    try:
        # file is an UploadFile instance automatically parsed by FastAPI from multipart/form-data
        # file.file is a file-like object pointing to the raw binary content
        image_bytes = await file.read() # Asynchronously read the entire file into memory as bytes (non-blocking)
        image = load_image_from_bytes(image_bytes) # Convert bytes to PIL Image
        caption = run_caption_inference(image)
        return {"caption": caption}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
