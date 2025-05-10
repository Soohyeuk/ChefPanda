import yt_transcript, yt_scrape
import json
from datetime import datetime
import mongoengine as me
from dotenv import load_dotenv
import os 

class Video(me.Document):
    title = me.StringField(required=True)
    video_id = me.StringField(required=True, unique=True)
    is_generated = me.BooleanField(default=True)
    language_code = me.StringField(required=True)
    snippets = me.StringField()
    source_type = me.StringField(required=True)  # 'search' or 'channel'
    channel_handle = me.StringField()  # Only for channel videos
    created_at = me.DateTimeField(default=datetime.utcnow)

def process_videos(max_results: int = 50, language: str = 'en', search_query: str = None, channel_id: str = None) -> list[str]:
    """
    Process videos by fetching them and their transcripts.
    
    Args:
        search_query: Search query for YouTube videos
        max_results: Maximum number of videos to process
        language: Language code for transcripts
    
    Returns:
        List of JSON strings containing video and transcript data
    """
    if search_query: 
        videos = yt_scrape.fetch_videos_by_id(search_query, max_results)
    
    if channel_id: 
        videos = yt_scrape.fetch_channel_videos_by_id(channel_id)
    
    results = []
    for video_id, title in videos:
        try:
            transcript = yt_transcript.get_transcript(video_id, language)
            json_data = yt_transcript.transcript_to_json(transcript, title)
            results.append(json_data)
        except Exception as e:
            print(f"Error processing video {video_id}: {str(e)}")
            continue
    
    return results

def save_to_mongodb(results_dict):
    """
    Save video results to MongoDB
    
    Args:
        results_dict: Dictionary containing search_results and channel_results
    """
    # Save search results
    for video_data in results_dict["search_results"]:
        try:
            video = Video(
                title=video_data["title"],
                video_id=video_data["video_id"],
                is_generated=video_data["is_generated"],
                language_code=video_data["language_code"],
                snippets=video_data["snippets"],
                source_type="search"
            )
            video.save()
        except me.NotUniqueError:
            print(f"Video {video_data['video_id']} already exists in database")
        except Exception as e:
            print(f"Error saving video {video_data['video_id']}: {str(e)}")

    # Save channel results
    for channel_handle, videos in results_dict["channel_results"].items():
        for video_data in videos:
            try:
                video = Video(
                    title=video_data["title"],
                    video_id=video_data["video_id"],
                    is_generated=video_data["is_generated"],
                    language_code=video_data["language_code"],
                    snippets=video_data["snippets"],
                    source_type="channel",
                    channel_handle=channel_handle
                )
                video.save()
            except me.NotUniqueError:
                print(f"Video {video_data['video_id']} already exists in database")
            except Exception as e:
                print(f"Error saving video {video_data['video_id']}: {str(e)}")

if __name__ == "__main__":
    load_dotenv()
    MONGODB_KEY = os.getenv('MONGODB_KEY')
    MONGODB_NAME = os.getenv('MONGODB_NAME')
    me.connect(MONGODB_NAME, host=MONGODB_KEY)
    all_results = {
        "search_results": [],
        "channel_results": {}
    }
    
    search_query = "cooking tutorial recipe"
    results = process_videos(50, 'en', search_query)
    all_results["search_results"] = [json.loads(result) for result in results]
    
    handles = ['@YOOXICMAN', '@1mincook', '@TryToEat']

    for handle in handles:
        try:
            print(f"\nFetching videos from {handle}...")
            channel_id = yt_scrape.get_channel_id_by_handle(handle)
            results2 = process_videos(50, 'ko', channel_id=channel_id)
            all_results["channel_results"][handle] = [json.loads(result) for result in results2]
            
        except Exception as e:
            print(f"Error for {handle}: {e}")
    
    # Save to MongoDB
    print("\nSaving results to MongoDB...")
    save_to_mongodb(all_results)
    
    # Also save to JSON file as backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f'youtube_results_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

