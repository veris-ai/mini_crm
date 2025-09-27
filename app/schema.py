from typing import Dict, List, Literal

from pydantic import BaseModel, Field


class Lead(BaseModel):
    id: int
    name: str
    contact: str
    industry: str
    status: Literal["new", "working", "qualified", "disqualified"]
    notes: List[str] = Field(default_factory=list)


class ChatRequest(BaseModel):
    message: str
    session_id: str


class ChatResponse(BaseModel):
    reply: str
    tool_calls: List[Dict]
    data: Dict


class CRMRunContext(BaseModel):
    """Per-run context for capturing tool calls and structured outputs."""

    tool_calls: List[Dict] = Field(default_factory=list)
    data: Dict = Field(default_factory=dict)


