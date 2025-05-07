from youtube_transcript_api import YouTubeTranscriptApi
from type import FetchedTranscript
import json 


def transcript_to_json(transcript: FetchedTranscript) -> str: 
    snippets = ""
    for snippet in transcript.snippets:
        snippets += (snippet.text + ". ")

    transcript_json = {
        "video_id": transcript.video_id,
        "is_generated": transcript.is_generated,
        "language_code": transcript.language_code,
        "snippets": snippets
    }

    return json.dumps(transcript_json, indent=2, ensure_ascii=False)
        

ytt_api = YouTubeTranscriptApi()
a = ytt_api.fetch("Nr9UU06PHi0", languages=['ko'])

print(transcript_to_json(a))


