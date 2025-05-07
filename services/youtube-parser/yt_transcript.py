from youtube_transcript_api import YouTubeTranscriptApi
from type import FetchedTranscript
import json 

def get_transcript(video_id: str, language: str = 'en') -> FetchedTranscript:
    """
    Fetch transcript for a given video ID.
    
    Args:
        video_id: YouTube video ID
        language: Language code for the transcript (default: 'en')
    
    Returns:
        FetchedTranscript object
    """
    ytt_api = YouTubeTranscriptApi()
    return ytt_api.fetch(video_id, languages=[language])

def transcript_to_json(transcript: FetchedTranscript, title: str) -> str:
    """
    Convert transcript to JSON format.
    
    Args:
        transcript: FetchedTranscript object
        title: Video title
    
    Returns:
        JSON string containing transcript data
    """
    snippets = ""
    for snippet in transcript.snippets:
        snippets += (snippet.text + ". ")

    transcript_json = {
        "title": title,
        "video_id": transcript.video_id,
        "is_generated": transcript.is_generated,
        "language_code": transcript.language_code,
        "snippets": snippets
    }

    return json.dumps(transcript_json, indent=2, ensure_ascii=False)



