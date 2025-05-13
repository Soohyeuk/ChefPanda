from type import Ingredient, InstructionStep, Recipe
import openai
from typing import List
from pathlib import Path
from dotenv import load_dotenv
import os

class RecipeGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.openai = openai.OpenAI(api_key=self.api_key)
        self._load_prompts()
        self.recipe = None 

    def _load_prompts(self):
        """Load prompt templates from text files"""
        prompts_dir = Path(__file__).parent / "prompts"
        
        with open(prompts_dir / "recipe_system.txt", "r") as f:
            self.system_prompt = f.read().strip()
            
        with open(prompts_dir / "recipe_extraction.txt", "r") as f:
            self.extraction_prompt_template = f.read().strip()

    def generate_recipe(self, transcript: str) -> Recipe:
        """
        Generate a complete recipe from a video transcript using OpenAI.
        
        Args:
            transcript (str): The video transcript to parse
            
        Returns:
            Recipe: A Recipe object containing title, ingredients, and steps
            
        Raises:
            RuntimeError: If recipe generation fails
        """
        prompt = self.extraction_prompt_template.format(transcript=transcript)
        
        try:
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7  # Balanced between creativity and accuracy
            )
            self.recipe = Recipe.model_validate_json(response.choices[0].message.content) #validates the response against the Recipe schema
            return self.recipe
        except openai.APIError as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Failed to generate recipe: {str(e)}")

    def receive_ingredients(self) -> List[Ingredient]:
        """
        Extract just the ingredients list from a transcript.
            
        Returns:
            List[Ingredient]: List of ingredients with quantities
        """
        return self.recipe.ingredients

    def receive_steps(self) -> List[InstructionStep]:
        """
        Extract just the instruction steps from a transcript.
        
        Returns:
            List[InstructionStep]: List of numbered instruction steps
        """
        return self.recipe.steps

    def receive_servings(self) -> str:
        """
        Extract the number of servings from a transcript.
        
        Returns:
            str: Number of servings
        """
        return self.recipe.servings
    
    def receive_prep_time(self) -> str:
        """
        Extract the preparation time from a transcript.
        
        Returns:
            str: Preparation time
        """
        return self.recipe.prep_time
    
    def receive_cook_time(self) -> str: 
        """
        Extract the cooking time from a transcript.
        
        Returns:
            str: Cooking time
        """
        return self.recipe.cook_time
    
    def receive_nutritional_info(self) -> str:
        """
        Extract the nutritional information from a transcript.
        
        Returns:
            str: Nutritional information
        """
        return self.recipe.nutritional_info

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set OPENAI_API_KEY environment variable")

    # Sample transcript
    sample_transcript = """
    Hey guys! Welcome back to my channel. Today I'm super excited to share my favorite chocolate chip cookie recipe with you all. These are seriously the best cookies ever, and you guys have been requesting this recipe like crazy in the comments.

    Before we get started, don't forget to hit that like button and subscribe if you're new here! Okay, let's get into it.

    So first, grab your flour - you want about two and a quarter cups of that. Then you'll need a cup of butter, make sure it's nice and soft at room temperature. For the sugar, I like to use both regular and brown sugar, about three quarters cup each. That brown sugar really gives it that amazing chewy texture.

    You'll also need a couple of eggs, some vanilla - just a teaspoon of that. Oh, and don't forget your baking soda and a bit of salt. And of course, the star of the show - chocolate chips! I usually throw in about two cups, but honestly, who's counting? Sometimes I add more because, come on, can you ever have too many chocolate chips?

    This recipe makes enough for about 12 people, but in my house, they disappear way faster! 

    Alright, so first thing's first, get your oven going at 375. While that's heating up, we're gonna cream our butter and sugars together. Just keep mixing until it gets nice and fluffy... yeah, just like that! Now add in those eggs one at a time, and your vanilla.

    In another bowl, we're mixing our dry ingredients. Once that's combined, slowly add it to your wet mixture. Don't overmix it guys, that's super important! Then fold in all those chocolate chips.

    Now here's my secret tip - I like to chill the dough for about 10 minutes while I line my baking sheets. Makes them come out perfect every time!

    Drop spoonfuls onto your baking sheets - I use a tablespoon, but you can make them bigger if you want. They'll need about 10 to 12 minutes in the oven. You want them just slightly golden on the edges. Let them cool for a few minutes on the tray before moving them.

    The prep for this is pretty quick, maybe 15 minutes tops, and then just 12 minutes to bake. Super easy!

    And there you have it, guys! Look how amazing these turned out. If you make these, don't forget to tag me on Instagram! See you in the next video!
    """

    # Create recipe generator instance
    generator = RecipeGenerator(api_key)
    try:
        # Generate recipe
        recipe = generator.generate_recipe(sample_transcript)
        
        # Print the results
        print("\nGenerated Recipe:")
        print(f"Title: {recipe.title}")
        print("\nIngredients:")
        for ing in recipe.ingredients:
            print(f"- {ing.quantity} {ing.name}")
        
        print("\nInstructions:")
        for step in recipe.steps:
            print(f"{step.step_number}. {step.description}")
        
        print(f"\nServings: {recipe.servings}")
        print(f"Prep Time: {recipe.prep_time}")
        print(f"Cook Time: {recipe.cook_time}")
        print("\nNutritional Information (per serving):")
        if recipe.nutritional_info:
            for key, value in recipe.nutritional_info.items():
                print(f"{key.capitalize()}: {value}")
        else:
            print("No nutritional information available")

    except Exception as e:
        print(f"Error: {str(e)} has occured")

