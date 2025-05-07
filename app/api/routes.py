from fastapi import APIRouter, File, UploadFile, HTTPException
from app.utils.image_io import load_image
from app.services.inference import run_caption_inference

router = APIRouter()

@router.post("/infer")
async def infer_image(file: UploadFile = File(...)):
    try:
        # file is an UploadFile instance automatically parsed by FastAPI from multipart/form-data
        # file.file is a file-like object pointing to the raw binary content
        image = load_image(file.file)
        caption = run_caption_inference(image)
        return {"caption": caption}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
