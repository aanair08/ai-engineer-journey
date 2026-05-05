from fastapi import APIRouter
from app.services.file_service import read_file
from app.services.ai_service import ask_ai
from pydantic import BaseModel
from app.services.vector_service import search


router = APIRouter()

class AskRequest(BaseModel):
    filenames: list[str]
    question: str
    session_id: str
chat_memory = {}

@router.post("/ask")
async def ask_question(request: AskRequest):
    filenames = request.filenames
    question = request.question

    relevant_chunks = search(question, filenames)

    context = "\n".join(relevant_chunks)
    history = chat_memory.get(request.session_id, [])
    
    messages = []

    messages.extend(history)

    messages.append({
        "role": "system",
        "content": f"""
    Answer ONLY using provided context.
    If not found, say: 'Answer not found in document.'

    Context:
    {context}
    """
    })

    messages.append({
        "role": "user",
        "content": question
    })

    answer = ask_ai(messages)
    
    chat_memory.setdefault(request.session_id, []).extend([
    {"role": "user", "content": question},
    {"role": "assistant", "content": answer}
    ])
    
    return {
        "answer": answer,
        "context_used": relevant_chunks  
    }
