from pydantic import BaseModel
from typing import Optional, Dict


class ToolDecision(BaseModel):
    tool: Optional[str]
    arguments: Dict = {}