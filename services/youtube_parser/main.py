# import fastapi 
# from . import yt_scrape
# from dotenv import load_dotenv
# import os

# app = fastapi.FastAPI()

# # Initialize YouTubeScraper
# load_dotenv()
# api_key = os.getenv("YOUTUBE_API_KEY")
# if not api_key:
#     raise ValueError("YOUTUBE_API_KEY environment variable not set")
# scraper = yt_scrape.YouTubeScraper(api_key)

# @app.get("/")
# def read_root():
#     return {"message": "Hello, World!"}

# @app.post("/scrape_channel")
# async def scrape_channel(handle: str, language: str = "en", quantity: int = 200):
#     channel_id = scraper.get_channel_id_by_handle(handle)
#     result = scraper.process_videos(type="channel_id", arg=channel_id)
#     return result 

# @app.post("/scrape_query")
# async def scrape_query(query: str, language: str = "en", quantity: int = 50):
#     result = scraper.process_videos(type="query", arg=query)
#     return result 

# @app.post("/scrape_video_id")
# async def scrape_video_id(id: str, language: str = "en"):
#     result = scraper.process_videos(type="id", arg=id)
#     return result 


# if __name__ == "__main__":
#     load_dotenv()
#     MONGODB_KEY = os.getenv('MONGODB_KEY')
#     MONGODB_NAME = os.getenv('MONGODB_NAME')
#     me.connect(MONGODB_NAME, host=MONGODB_KEY)
#     all_results = {
#         "search_results": [],
#         "channel_results": {}
#     }
    
#     search_query = "cooking tutorial recipe"
#     results = process_videos(50, 'en', type="query", arg=search_query)
#     all_results["search_results"] = [json.loads(result) for result in results]
    
#     handles = ['@YOOXICMAN', '@1mincook', '@TryToEat']

#     for handle in handles:
#         try:
#             print(f"\nFetching videos from {handle}...")
#             channel_id = yt_scrape.get_channel_id_by_handle(handle)
#             results2 = process_videos(50, 'ko', type="channel_id", arg=channel_id)
#             all_results["channel_results"][handle] = [json.loads(result) for result in results2]
            
#         except Exception as e:
#             print(f"Error for {handle}: {e}")
    
#     # Save to MongoDB
#     print("\nSaving results to MongoDB...")
#     save_to_mongodb(all_results)
    
#     # Also save to JSON file as backup
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     with open(f'youtube_results_{timestamp}.json', 'w', encoding='utf-8') as f:
#         json.dump(all_results, f, ensure_ascii=False, indent=2)


# import mongoengine as me
# from type import Video
# def save_to_mongodb(results_dict: dict[list[dict]]) -> None:
#     """
#     Save video results to MongoDB
    
#     Args:
#         results_dict: Dictionary containing search_results and channel_results
#     """
#     for video_data in results_dict["search_results"]:
#         try:
#             video = Video(
#                 title=video_data["title"],
#                 video_id=video_data["video_id"],
#                 is_generated=video_data["is_generated"],
#                 language_code=video_data["language_code"],
#                 snippets=video_data["snippets"],
#                 source_type="search"
#             )
#             video.save()
#         except me.NotUniqueError:
#             print(f"Video {video_data['video_id']} already exists in database")
#         except Exception as e:
#             print(f"Error saving video {video_data['video_id']}: {str(e)}")

#     for channel_handle, videos in results_dict["channel_results"].items():
#         for video_data in videos:
#             try:
#                 video = Video(
#                     title=video_data["title"],
#                     video_id=video_data["video_id"],
#                     is_generated=video_data["is_generated"],
#                     language_code=video_data["language_code"],
#                     snippets=video_data["snippets"],
#                     source_type=channel_handle
#                 )
#                 video.save()
#             except me.NotUniqueError:
#                 print(f"Video {video_data['video_id']} already exists in database")
#             except Exception as e:
#                 print(f"Error saving video {video_data['video_id']}: {str(e)}")

