from fastapi import APIRouter
from pydantic import BaseModel
from app.services.agent_service import run_agent

router = APIRouter()


class AgentRequest(BaseModel):
    question: str


@router.post("/agent")
async def ask_agent(request: AgentRequest):
    response = run_agent(request.question)

    return {
        "response": response
    }