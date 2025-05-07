import requests
from dotenv import load_dotenv
import os


load_dotenv()
API_KEY = os.getenv('YOUTUBE_API_KEY')
if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found in environment variables")

SEARCH_QUERY = 'cooking tutorial recipe'
MAX_RESULTS = 50

def fetch_videos(query: str, max_results: int = 50) -> list[tuple[str, str]]:
    """
    Fetch video IDs and titles from YouTube search.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 50)
    
    Returns:
        List of tuples containing (video_id, title)
    """
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

    videos = [(item['id']['videoId'], item['snippet']['title']) 
             for item in data.get('items', [])]
    return videos

videos = fetch_videos(SEARCH_QUERY, MAX_RESULTS)
