from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator
import asyncio
import json

app = FastAPI()


class StreamSteppingTypeV1:
    GENERATION = "generation"
    POST_PROCESSING = "post_processing"
    FINALIZATION = "finalization"


class StreamEventTypeV1:
    MESSAGE_DELTA = "message_delta"
    MESSAGE_COMPLETE = "message_complete"
    STEPPING = "stepping"
    END = "end"


class StreamEventsV1:
    @staticmethod
    def message_delta(delta: str) -> str:
        return json.dumps(
            {"event": StreamEventTypeV1.MESSAGE_DELTA, "data": {"delta": delta}}
        )

    @staticmethod
    def message_complete(final_message: str) -> str:
        return json.dumps(
            {
                "event": StreamEventTypeV1.MESSAGE_COMPLETE,
                "data": {"final_message": final_message},
            }
        )

    @staticmethod
    def stepping(type: str) -> str:
        return json.dumps({"event": StreamEventTypeV1.STEPPING, "data": {"type": type}})

    @staticmethod
    def end() -> str:
        return json.dumps({"event": StreamEventTypeV1.END})


async def stream_sales_chat_v_1() -> AsyncGenerator[str, None]:
    yield f"data: {StreamEventsV1.stepping(StreamSteppingTypeV1.GENERATION)}\n\n"

    sales_responses = [
        "Hello, how are you?",
        "I'm doing well, thank you!",
        "What's your name?",
        "My name is John Doe.",
        "What is your favorite color?",
        "My favorite color is blue.",
        "What is your favorite food?",
    ]

    for response in sales_responses:
        yield f"data: {StreamEventsV1.message_delta(response)}\n\n"
        await asyncio.sleep(0.6)

    yield f"data: {StreamEventsV1.message_complete(''.join(sales_responses))}\n\n"
    yield f"data: {StreamEventsV1.stepping(StreamSteppingTypeV1.POST_PROCESSING)}\n\n"
    yield f"data: {StreamEventsV1.stepping(StreamSteppingTypeV1.FINALIZATION)}\n\n"
    yield f"data: {StreamEventsV1.end()}\n\n"


@app.get("/stream")
async def stream_endpoint():
    return StreamingResponse(stream_sales_chat_v_1(), media_type="text/event-stream")


@app.get("/")
async def health_check():
    return {"status": "ok"}
