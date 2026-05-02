from fastapi import APIRouter, UploadFile, File
from app.services.file_service import save_file

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    filename = save_file(file.filename, content)

    return {"filename": filename}