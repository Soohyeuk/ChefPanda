from pydantic import BaseModel # type: ignore
from mongoengine import Document, StringField, BooleanField, DateTimeField # type: ignore
from typing import List, Dict
from datetime import datetime

class FetchedTranscriptSnippet(BaseModel):
    text: str 
    start: float
    duration: float

class FetchedTranscript(BaseModel):
    snippets: list[FetchedTranscriptSnippet]
    video_id: str
    language_code: str
    is_generated: bool

class Ingredient(BaseModel):
    name: str
    quantity: str

class InstructionStep(BaseModel):
    step_number: int
    description: str

class Recipe(BaseModel):
    title: str
    ingredients: List[Ingredient]
    steps: List[InstructionStep]
    servings: str | None = None
    prep_time: str | None = None
    cook_time: str | None = None
    nutritional_info: Dict[str, float] | None = None

class Video(Document):
    title = StringField(required=True)
    video_id = StringField(required=True, unique=True)
    is_generated = BooleanField(default=True)
    language_code = StringField(required=True)
    snippets = StringField()
    source_type = StringField(required=True)  # 'search' or 'channel id'
    created_at = DateTimeField(default=datetime.utcnow)