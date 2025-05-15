"""
YouTube video scraping and transcript processing functionality.
"""

import requests # type: ignore
from .type import FetchedTranscript, FetchedTranscriptSnippet
from youtube_transcript_api import YouTubeTranscriptApi # type: ignore
from typing import List, Tuple, Dict, Any, Optional



class YouTubeScraper:
    def __init__(self, api_key:str, language:str = "en", max_results:int=50): 
        self.api_key = api_key
        self.language = language
        self.max_results = max_results

    def _convert_transcript(self, ytt_transcript: Any) -> FetchedTranscript:
        """Convert YouTubeTranscriptApi transcript to our FetchedTranscript type"""
        snippets = [
            FetchedTranscriptSnippet(
                text=item['text'],
                start=item['start'],
                duration=item['duration']
            )
            for item in ytt_transcript
        ]
        return FetchedTranscript(
            snippets=snippets,
            video_id=ytt_transcript.video_id,
            language_code=ytt_transcript.language_code,
            is_generated=ytt_transcript.is_generated
        )

    def get_transcript(self, video_id: str) -> FetchedTranscript:
        """
        Fetch transcript for a given video ID.
        
        Args:
            video_id: YouTube video ID

        Returns:
            FetchedTranscript object
        """
        ytt_api = YouTubeTranscriptApi()
        ytt_transcript = ytt_api.fetch(video_id, languages=self.language)
        return self._convert_transcript(ytt_transcript)

    def transcript_to_dict(self, transcript: FetchedTranscript, title: str) -> Dict[str, Any]:
        """
        Convert transcript to JSON format.
        
        Args:
            transcript: FetchedTranscript object
            title: Video title
        
        Returns:
            Dictionary containing transcript data
        """
        snippets = ""
        for snippet in transcript.snippets:
            snippets += (snippet.text + ". ")

        transcript_dict = {
            "title": title,
            "video_id": transcript.video_id,
            "is_generated": transcript.is_generated,
            "language_code": transcript.language_code,
            "snippets": snippets
        }

        return transcript_dict

    def fetch_videos_by_query(self, query: str) -> List[Tuple[str, str]]:
        """
        Fetch video IDs and titles from YouTube search.
        
        Args:
            query: Search query string
        
        Returns:
            List of tuples containing (video_id, title)
        """
        url = 'https://www.googleapis.com/youtube/v3/search'
        params: Dict[str, Any] = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'maxResults': self.max_results,
            'key': self.api_key
        }
        response = requests.get(url, params=params)
        data = response.json()

        return [(item['id']['videoId'], item['snippet']['title']) 
                for item in data.get('items', [])]

    def fetch_channel_videos_by_id(self, channel_id: str) -> List[Tuple[str, str]]:
        """
        Fetch video IDs and titles from a specific YouTube channel.

        Args:
            channel_id: YouTube channel ID
        
        Returns:
            List of tuples containing (video_id, title)
        """
        url = 'https://www.googleapis.com/youtube/v3/search'
        params: Dict[str, Any] = {
            'part': 'snippet',
            'channelId': channel_id,
            'type': 'video',
            'order': 'date',
            'maxResults': self.max_results,
            'key': self.api_key
        }
        response = requests.get(url, params=params)
        data = response.json()

        return [(item['id']['videoId'], item['snippet']['title']) 
                for item in data.get('items', [])]

    def get_channel_id_by_handle(self, handle: str) -> str:
        """
        Resolve a YouTube handle (e.g. '@TryToEat') to a channel ID.

        Args:
            handle: YouTube handle (e.g. '@TryToEat')
        
        Returns:
            Channel ID
        """
        url = 'https://www.googleapis.com/youtube/v3/channels'
        params: Dict[str, Any] = {
            'part': 'id',
            'forHandle': handle.lstrip('@'),
            'key': self.api_key
        }
        response = requests.get(url, params=params)
        data = response.json()

        items = data.get('items', [])
        if not items:
            raise ValueError(f"Channel not found for handle: {handle}")
        
        return items[0]['id']

    def fetch_video_by_id(self, video_id: str) -> List[Tuple[str, str]]:
        """
        Fetch video details by ID and return a list of (video_id, title) tuples.
        """
        url = 'https://www.googleapis.com/youtube/v3/videos'
        params: Dict[str, Any] = {
            'part': 'snippet',
            'id': video_id,
            'key': self.api_key
        }
        response = requests.get(url, params=params)
        data = response.json()
        items = data.get('items', [])
        return [(item['id'], item['snippet']['title']) for item in items]

    def process_videos(self, type: str = "id", arg: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Process videos by fetching them and their transcripts.
        Retries 3 times if there is an error per video. 

        Args:
            type: Type of search to perform
            arg: Argument for the search
        Returns:
            List of dicts containing video and transcript data
        """
        if arg is None:
            raise ValueError("arg parameter cannot be None")

        if type == "id":
            videos = self.fetch_video_by_id(arg)
        elif type == "query": 
            videos = self.fetch_videos_by_query(arg)
        elif type == 'channel_id': 
            videos = self.fetch_channel_videos_by_id(arg)
        else:
            raise ValueError(f"Invalid type: {type}")
        
        results = []
        for video_id, title in videos:
            for attempt in range(4):
                try:
                    transcript = self.get_transcript(video_id)
                    dict = self.transcript_to_dict(transcript, title)
                    results.append(dict)
                    break 
                except Exception as e:
                    if attempt < 3:
                        print(f"Error processing video {video_id} (attempt {attempt+1}): {str(e)}. Retrying...")
                    else:
                        print(f"Failed to process video {video_id} after 4 attempts: {str(e)}")

        return results




