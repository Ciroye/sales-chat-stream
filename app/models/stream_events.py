import json


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
