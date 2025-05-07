from youtube_transcript_api import YouTubeTranscriptApi
from type import FetchedTranscript
import json 


def transcript_to_json(transcript: FetchedTranscript) -> str: 
    transcript_storage = {}
    for snippet in transcript.snippets: 
        transcript_storage[snippet.start] = snippet.text
    

    
    return "!"

        

ytt_api = YouTubeTranscriptApi()
a = ytt_api.fetch("UYhKDweME3A")

transcript_to_json(a)

