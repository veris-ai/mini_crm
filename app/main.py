import os
from typing import Dict

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from .schema import ChatRequest, ChatResponse
from . import get_crm_chat_service

from veris_ai import veris
from veris_ai import init_observability, instrument_fastapi_app

load_dotenv()

if os.getenv("OTEL_SERVICE_NAME") == 'mini_crm':
    init_observability()
else:
    print("Not initializing observability")

app = FastAPI(title="Mini CRM Lead Qualifier")


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    try:
        service = get_crm_chat_service(req.session_id)
        result = await service.process_message(req.message)
        return ChatResponse(
            reply=result.get("reply", ""),
            tool_calls=result.get("tool_calls", []),
            data=result.get("data", {}),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if os.getenv("OTEL_SERVICE_NAME") == 'mini_crm':
    instrument_fastapi_app(app)
else:
    print("Not instrumenting fastapi app")

veris.set_fastapi_mcp(fastapi=app)
veris.fastapi_mcp.mount_http()
