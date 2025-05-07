import yt_transcript, yt_scrape

def process_videos(search_query: str, max_results: int = 50, language: str = 'en') -> list[str]:
    """
    Process videos by fetching them and their transcripts.
    
    Args:
        search_query: Search query for YouTube videos
        max_results: Maximum number of videos to process
        language: Language code for transcripts
    
    Returns:
        List of JSON strings containing video and transcript data
    """
    # Fetch videos
    videos = yt_scrape.fetch_videos(search_query, max_results)
    
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

if __name__ == "__main__":
    # Example usage
    search_query = "cooking tutorial recipe"
    results = process_videos(search_query)
    
    # Print results
    for json_data in results:
        print(json_data)
        print("-" * 80)

