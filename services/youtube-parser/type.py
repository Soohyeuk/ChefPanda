from pydantic import BaseModel
import mongoengine as me
from typing import Optional, List, Dict
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

class Video(me.Document):
    title = me.StringField(required=True)
    video_id = me.StringField(required=True, unique=True)
    is_generated = me.BooleanField(default=True)
    language_code = me.StringField(required=True)
    snippets = me.StringField()
    source_type = me.StringField(required=True)  # 'search' or 'channel id'
    created_at = me.DateTimeField(default=datetime.utcnow)