from typing import AsyncGenerator
import asyncio
from app.models.stream_events import StreamEventsV1, StreamSteppingTypeV1


class BaseStreamService:
    async def process_stream(
        self, agent_id: str, query: str
    ) -> AsyncGenerator[str, None]:
        """
        This is the main method that your coworker should implement.
        It should follow the same pattern as the mock implementation but with their own logic.

        Args:
            agent_id: The ID of the agent processing the request
            query: The user's query

        Yields:
            Stream events in the format: f"data: {event_json}\n\n"
        """
        yield f"data: {StreamEventsV1.stepping(StreamSteppingTypeV1.GENERATION)}\n\n"

        # TODO: Replace this with actual implementation
        final_message = ""
        async for chunk in self._mock_stream_response(query):
            final_message += chunk
            yield f"data: {StreamEventsV1.message_delta(chunk)}\n\n"

        yield f"data: {StreamEventsV1.message_complete(final_message)}\n\n"
        yield f"data: {StreamEventsV1.stepping(StreamSteppingTypeV1.POST_PROCESSING)}\n\n"
        yield f"data: {StreamEventsV1.stepping(StreamSteppingTypeV1.FINALIZATION)}\n\n"
        yield f"data: {StreamEventsV1.end()}\n\n"

    async def _mock_stream_response(self, query: str) -> AsyncGenerator[str, None]:
        """Mock streaming response that simulates an LLM response."""
        responses = {
            "hello": "Hello! How can I help you today?",
            "weather": "I'm sorry, I don't have access to real-time weather data. I'm just a mock LLM for testing purposes.",
            "help": "I'm a mock LLM service for testing streaming responses. You can ask me anything, but I'll just return this message.",
        }

        response = responses.get(
            query.lower(), "This is a mock streaming response. Your query was: " + query
        )

        words = response.split()
        for word in words:
            yield word + " "
            await asyncio.sleep(0.1)
