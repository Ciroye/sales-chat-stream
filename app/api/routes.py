from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from app.services.stream_service import BaseStreamService

router = APIRouter()
stream_service = BaseStreamService()


@router.get("/stream")
async def stream_endpoint(request: Request):
    agent_id = request.query_params.get("agent_id", "default-agent")
    query = request.query_params.get("query", "Say something nice!")

    return StreamingResponse(
        stream_service.process_stream(agent_id, query), media_type="text/event-stream"
    )


@router.get("/")
async def health_check():
    return {"status": "ok"}
