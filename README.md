# Streaming API Service

This is a FastAPI-based streaming service that provides a structured way to implement streaming responses.

## Project Structure

```
app/
├── api/
│   └── routes.py         # API endpoints
├── core/
│   └── config.py         # Configuration settings
├── models/
│   └── stream_events.py  # Stream event models and types
├── services/
│   └── stream_service.py # Business logic implementation
└── main.py              # Application entry point
```

## How to Implement Your Logic

1. The main file you need to modify is `app/services/stream_service.py`
2. Create a new class that inherits from `BaseStreamService`
3. Override the `process_stream` method with your implementation
4. The method should follow the same pattern as the mock implementation:
   - Yield generation step
   - Process the stream and yield message deltas
   - Yield message complete
   - Yield post-processing step
   - Yield finalization step
   - Yield end event

Example implementation:

```python
from app.services.stream_service import BaseStreamService

class YourStreamService(BaseStreamService):
    async def process_stream(self, agent_id: str, query: str):
        yield f"data: {StreamEventsV1.stepping(StreamSteppingTypeV1.GENERATION)}\n\n"
        
        # Your implementation here
        final_message = ""
        async for chunk in your_stream_implementation(query):
            final_message += chunk
            yield f"data: {StreamEventsV1.message_delta(chunk)}\n\n"
            
        yield f"data: {StreamEventsV1.message_complete(final_message)}\n\n"
        yield f"data: {StreamEventsV1.stepping(StreamSteppingTypeV1.POST_PROCESSING)}\n\n"
        yield f"data: {StreamEventsV1.stepping(StreamSteppingTypeV1.FINALIZATION)}\n\n"
        yield f"data: {StreamEventsV1.end()}\n\n"
```

## Running the Service

1. Install dependencies:
```bash
pip install fastapi uvicorn
```

2. Run the service:
```bash
uvicorn app.main:app --reload
```

3. Access the API at `http://localhost:8000/stream?query=your_query` 