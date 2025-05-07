from pydantic import BaseModel


class FetchedTranscriptSnippet(BaseModel):
    text: str 
    start: float
    duration: float

class FetchedTranscript(BaseModel):
    snippets: list[FetchedTranscriptSnippet]
    video_id: str
    language_code: str
    is_generated: bool
