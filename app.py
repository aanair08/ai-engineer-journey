from fastapi import FastAPI, UploadFile, File
import os
from ai_services import ask_ai


app = FastAPI()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return{"message":"AI Docs Assistant Running"}

@app.post("/upload")
async def upload_fiile(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return {"filename": file.filename}

def read_file(filename):
    path = os.path.join(UPLOAD_DIR, filename)
    
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    
@app.post("/ask")
async def ask_question(filename: str, question: str):
    content = read_file(filename)
    MAX_CHARS = 3000

    content = content[:MAX_CHARS]

    prompt = f"""
    You are a strict assistant.

    Only answer using the provided document.
    If the answer is not found, say: "Answer not found in document."

    Keep answers short and precise.

    Document:
    {content}

    Question:
    {question}
    """

    answer = ask_ai(prompt)

    if "not found" in answer.lower():
        return {"answer": "No relevant answer found in document"}

    return {"answer": answer}