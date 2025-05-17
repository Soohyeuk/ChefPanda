"""
FastAPI server for YouTube video parsing and recipe generation.
"""

import fastapi # type: ignore
from fastapi import HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from .yt_scrape import YouTubeScraper
from .recipe_gen import RecipeGenerator
from .types import ScrapeRequest, QueryRequest, VideoRequest
from dotenv import load_dotenv # type: ignore
import os
from contextlib import asynccontextmanager
from typing import List, Dict, Any

yt_api_key = None 
openai_api_key = None 

@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    """
    Lifespan context manager for FastAPI application.
    Handles startup and shutdown events.
    """
    load_dotenv()
    global yt_api_key, openai_api_key
    yt_api_key = os.getenv("YOUTUBE_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not yt_api_key:
        raise ValueError("YOUTUBE_API_KEY environment variable not set")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    yield  

app = fastapi.FastAPI(
    title="ChefPanda YouTube Parser",
    description="Service for scraping and parsing YouTube cooking videos",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/scrape_channel")
async def scrape_channel(request: ScrapeRequest) -> List[Dict[str, Any]]:
    """
    Scrape recipes from a YouTube channel.
    
    Args:
        request: ScrapeRequest containing:
            - handle: YouTube channel handle (e.g. '@yooxicman')
            - language: Language code (default: 'en')
            - quantity: Number of videos to scrape (default: 200)
            
    Returns:
        List[Dict[str, Any]]: List of recipe dictionaries
    """
    try:
        scraper = YouTubeScraper(yt_api_key, request.language, request.quantity)
        channel_id = scraper.get_channel_id_by_handle(request.handle)
        result = scraper.process_videos(type="channel_id", arg=channel_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

    try:
        recipes = []
        recipe_gen = RecipeGenerator(openai_api_key) 
        
        # Process videos in batches to avoid timeouts
        batch_size = 1  # Process one video at a time to ensure reliability
        for i in range(0, len(result), batch_size):
            batch = result[i:i + batch_size]
            for video in batch:
                try:
                    recipe = recipe_gen.generate_recipe(str(video))
                    recipes.append(recipe.model_dump())
                except Exception as e:
                    print(f"Error processing video {i}: {str(e)}")
                    continue
                
        if not recipes:
            raise HTTPException(status_code=404, detail="No recipes could be generated from the videos")
            
        return recipes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing recipes: {str(e)}")

@app.post("/scrape_query")
async def scrape_query(request: QueryRequest) -> List[Dict[str, Any]]:
    """
    Search and scrape recipes based on a query.
    
    Args:
        request: QueryRequest containing:
            - query: Search query string
            - language: Language code (default: 'en')
            - quantity: Number of videos to scrape (default: 50)
            
    Returns:
        List[Dict[str, Any]]: List of recipe dictionaries
    """
    try:
        scraper = YouTubeScraper(yt_api_key, request.language, request.quantity)
        result = scraper.process_videos(type="query", arg=request.query)
        if not result:
            raise HTTPException(status_code=404, detail="No videos found for query")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

    try:
        recipes = []
        recipe_gen = RecipeGenerator(openai_api_key)
        
        # Process videos in batches to avoid timeouts
        batch_size = 1  # Process one video at a time to ensure reliability
        for i in range(0, len(result), batch_size):
            batch = result[i:i + batch_size]
            for video in batch:
                try:
                    recipe = recipe_gen.generate_recipe(str(video))
                    recipes.append(recipe.model_dump())
                except Exception as e:
                    print(f"Error processing video {i}: {str(e)}")
                    continue
                
        if not recipes:
            raise HTTPException(status_code=404, detail="No recipes could be generated from the videos")
            
        return recipes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing recipes: {str(e)}")

@app.post("/scrape_video_id")
async def scrape_video_id(request: VideoRequest) -> Dict[str, Any]:
    """
    Scrape a recipe from a specific video ID.
    
    Args:
        request: VideoRequest containing:
            - id: YouTube video ID
            - language: Language code (default: 'en')
            
    Returns:
        Dict[str, Any]: Recipe dictionary
    """
    try:
        # Initialize scraper and get video
        scraper = YouTubeScraper(yt_api_key, request.language)
        results = scraper.process_videos(type="id", arg=request.id)
        if not results:
            raise HTTPException(status_code=404, detail="Video not found or no transcript available")
            
        # Generate recipe
        try:
            recipe_gen = RecipeGenerator(openai_api_key)
            recipe = recipe_gen.generate_recipe(str(results[0]))  # Process first (and only) result
            return recipe.model_dump()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating recipe: {str(e)}")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")

@app.get("/status")
async def get_status() -> Dict[str, Any]:
    """
    Get service health status and API key validity.
    
    Returns:
        Dict[str, Any]: Status information including:
            - service: Overall service status
            - youtube_api: YouTube API key status
            - openai_api: OpenAI API key status
    """
    try:
        # Basic validation of API keys
        yt_status = "valid" if yt_api_key and len(yt_api_key) > 20 else "invalid"
        openai_status = "valid" if openai_api_key and len(openai_api_key) > 20 else "invalid"
        
        return {
            "service": "healthy",
            "youtube_api": yt_status,
            "openai_api": openai_status,
            "version": app.version
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking status: {str(e)}")




@app.get("/languages")
async def get_supported_languages() -> Dict[str, List[Dict[str, str]]]:
    """
    Get list of supported languages for video transcription and recipe generation.
    
    Returns:
        Dict[str, List[Dict[str, str]]]: Supported languages with codes
    """
    # Add or modify languages based on what your service actually supports
    supported_languages = [
        {"code": "en", "name": "English"},
        {"code": "es", "name": "Spanish"},
        {"code": "fr", "name": "French"},
        {"code": "de", "name": "German"},
        {"code": "it", "name": "Italian"},
        {"code": "pt", "name": "Portuguese"},
        {"code": "ja", "name": "Japanese"},
        {"code": "ko", "name": "Korean"},
        {"code": "zh", "name": "Chinese"}
    ]
    
    return {"supported_languages": supported_languages}

@app.get("/limits")
async def get_rate_limits() -> Dict[str, Any]:
    """
    Get current rate limits and quota information.
    
    Returns:
        Dict[str, Any]: Rate limit information for APIs
    """
    try:
        # You would typically implement actual quota checking here
        # This is a placeholder implementation
        return {
            "youtube_api": {
                "daily_quota": 10000,
                "quota_remaining": 9000,
                "reset_time": "midnight PT"
            },
            "openai_api": {
                "requests_per_min": 60,
                "tokens_per_min": 40000,
                "reset_period": "per minute"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking rate limits: {str(e)}")

@app.get("/recipe/format")
async def get_recipe_format() -> Dict[str, Any]:
    """
    Get the schema/format of recipe responses.
    
    Returns:
        Dict[str, Any]: Recipe format specification
    """
    return {
        "format_version": "1.0",
        "recipe_schema": {
            "title": "string",
            "description": "string",
            "ingredients": ["string"],
            "instructions": ["string"],
            "metadata": {
                "video_id": "string",
                "channel": "string",
                "language": "string",
                "duration": "string",
                "timestamp": "string"
            }
        }
    }

@app.get("/videos/status")
async def get_videos_status(video_ids: str) -> Dict[str, Any]:
    """
    Check processing status for multiple videos.
    
    Args:
        video_ids: Comma-separated list of video IDs
        
    Returns:
        Dict[str, Any]: Status information for each video
    """
    try:
        ids = video_ids.split(",")
        statuses = {}
        
        for vid_id in ids:
            # You would typically check a database or cache for actual status
            # This is a placeholder implementation
            statuses[vid_id] = {
                "status": "completed",  # or "processing", "failed", etc.
                "progress": 100,  # percentage
                "error": None
            }
            
        return {"video_statuses": statuses}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking video status: {str(e)}")


