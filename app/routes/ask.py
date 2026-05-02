from fastapi import APIRouter
from app.services.file_service import read_file
from app.services.ai_service import ask_ai
from pydantic import BaseModel
from app.services.embedding_service import get_embedding
import numpy as np

router = APIRouter()

class AskRequest(BaseModel):
    filenames: list[str]
    question: str
vector_store = []

@router.post("/ask")
async def ask_question(request: AskRequest):
    filenames = request.filenames
    question = request.question


    process_documents(filenames)

    # Step 2: Retrieve relevant chunks
    relevant_chunks = search(question)

    context = "\n".join(relevant_chunks)
    
    prompt = f"""
    Only answer using the provided content.
    If not found, say: 'Answer not found in document.'

    Content:
    {context}

    Question:
    {question}
    """
    answer = ask_ai(prompt)

    return {
        "answer": answer,
        "context_used": relevant_chunks  # helpful for debugging
    }

def  find_relevant_chunks(content, question):
    sentences = content.split(".")

    relevant = []

    for sentence in sentences:
        if any(word.lower() in sentence.lower() for word in question.split()):
            relevant.append(sentence)

    return ". ".join(relevant[:5])

def split_text(text, chunk_size=200):
    words = text.split()
    
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    
    return chunks

def process_documents(filenames):
    global vector_store
    vector_store = []  # reset for simplicity

    for filename in filenames:
        content = read_file(filename)
        chunks = split_text(content)

        for chunk in chunks:
            embedding = get_embedding(chunk)
            vector_store.append({
                "text": chunk,
                "embedding": embedding
            })

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def search(query, top_k=3):
    query_embedding = get_embedding(query)

    scores = []

    for item in vector_store:
        score = cosine_similarity(query_embedding, item["embedding"])
        scores.append((score, item["text"]))

    scores.sort(reverse=True)

    return [text for _, text in scores[:top_k]]