import requests

API_KEY = 'YOUR_YOUTUBE_API_KEY'
SEARCH_QUERY = 'cooking tutorial recipe'
MAX_RESULTS = 50

def fetch_video_ids(query, max_results=50):
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

    video_ids = [item['id']['videoId'] for item in data.get('items', [])]
    return video_ids

video_ids = fetch_video_ids(SEARCH_QUERY, MAX_RESULTS)
print(video_ids)
