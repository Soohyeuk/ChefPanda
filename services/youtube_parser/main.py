"""
FastAPI server for YouTube video parsing and recipe generation.
"""

import fastapi # type: ignore
from fastapi import HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from .yt_scrape import YouTubeScraper
from .recipe_gen import RecipeGenerator
from dotenv import load_dotenv # type: ignore
import os
from contextlib import asynccontextmanager
from typing import List, Dict, Any

class ScrapeRequest(BaseModel):
    handle: str
    language: str = "en"
    quantity: int = 200

class QueryRequest(BaseModel):
    query: str
    language: str = "en"
    quantity: int = 50

class VideoRequest(BaseModel):
    id: str
    language: str = "en"

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
async def scrape_query(request: QueryRequest) -> Dict[str, Any]:
    """
    Search and scrape recipes based on a query.
    
    Args:
        request: QueryRequest containing:
            - query: Search query string
            - language: Language code (default: 'en')
            - quantity: Number of videos to scrape (default: 50)
    """
    try:
        scraper = YouTubeScraper(yt_api_key, request.language, request.quantity)
        results = scraper.process_videos(type="query", arg=request.query)
        if not results:
            raise HTTPException(status_code=404, detail="No videos found for query")
        
        recipe_gen = RecipeGenerator(openai_api_key)
        recipe = recipe_gen.generate_recipe(str(results))
        return recipe.model_dump()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/scrape_video_id")
async def scrape_video_id(request: VideoRequest) -> Dict[str, Any]:
    """
    Scrape a recipe from a specific video ID.
    
    Args:
        request: VideoRequest containing:
            - id: YouTube video ID
            - language: Language code (default: 'en')
    """
    try:
        scraper = YouTubeScraper(yt_api_key, request.language)
        a = scraper.fetch_video_by_id(request.id)
        results = scraper.process_videos(type="id", arg=request.id)
        if not results:
            raise HTTPException(status_code=404, detail="Video not found or no transcript available")
        
        recipe_gen = RecipeGenerator(openai_api_key)
        recipe = recipe_gen.generate_recipe(str(results))
        return recipe.model_dump()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


