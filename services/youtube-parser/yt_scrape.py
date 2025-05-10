import requests
from dotenv import load_dotenv
import os


def fetch_videos_by_id(query: str, max_results: int = 50) -> list[tuple[str, str]]:
    """
    Fetch video IDs and titles from YouTube search.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 50)
    
    Returns:
        List of tuples containing (video_id, title)
    """
    load_dotenv()
    API_KEY = os.getenv('YOUTUBE_API_KEY')
    if not API_KEY:
        raise ValueError("YOUTUBE_API_KEY not found in environment variables")
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': max_results,
        'key': API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    return [(item['id']['videoId'], item['snippet']['title']) 
             for item in data.get('items', [])]


def get_channel_id_by_handle(handle: str) -> str:
    """
    Resolve a YouTube handle (e.g. '@TryToEat') to a channel ID.
    """
    load_dotenv()
    API_KEY = os.getenv('YOUTUBE_API_KEY')
    if not API_KEY:
        raise ValueError("YOUTUBE_API_KEY not found in environment variables")
    url = 'https://www.googleapis.com/youtube/v3/channels'
    params = {
        'part': 'id',
        'forHandle': handle.lstrip('@'),
        'key': API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    items = data.get('items', [])
    if not items:
        raise ValueError(f"Channel not found for handle: {handle}")
    
    return items[0]['id']

def fetch_channel_videos_by_id(channel_id: str, max_results: int = 200) -> list[tuple[str, str]]:
    """
    Fetch video IDs and titles from a specific YouTube channel.
    """
    load_dotenv()
    API_KEY = os.getenv('YOUTUBE_API_KEY')
    if not API_KEY:
        raise ValueError("YOUTUBE_API_KEY not found in environment variables")
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part': 'snippet',
        'channelId': channel_id,
        'type': 'video',
        'order': 'date',
        'maxResults': max_results,
        'key': API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    return [(item['id']['videoId'], item['snippet']['title']) 
            for item in data.get('items', [])]

