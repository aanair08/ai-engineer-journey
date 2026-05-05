from fastapi import APIRouter, UploadFile, File
from app.services.file_service import save_file
from app.services.vector_service import store_chunks

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    filename = save_file(file.filename, content)

    text = content.decode("utf-8")
    chunks = split_text(text)

    store_chunks(chunks, filename) 

    return {"filename": filename}


def split_text(text, chunk_size=200):
    words = text.split()
    
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    
    return chunks