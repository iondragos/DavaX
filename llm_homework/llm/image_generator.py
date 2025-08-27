from openai import OpenAI
import os
import requests
from uuid import uuid4

client = OpenAI()
IMAGE_DIR = "images"

def build_image_prompt(reply: str) -> str:
    return (
        f"A cinematic illustrated book cover for the novel described here: '{reply}'. "
        f"Include symbolic imagery, dramatic lighting, and a thematic scene from the story. "
        f"Use a painterly, fantasy-inspired style. No text in the picture."
    )

def generate_book_image(prompt: str, size: str = "512x512", save: bool = True) -> str:
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

    print("🎨 Generating image...")

    response = client.images.generate(
        model="dall-e-2",  # or "dall-e-3"
        prompt=prompt,
        size=size,
        # quality="standard", #for dalle3 only
        n=1
    )

    image_url = response.data[0].url

    if not save:
        return image_url

    filename = f"{uuid4().hex}.png"
    filepath = os.path.join(IMAGE_DIR, filename)

    img_data = requests.get(image_url).content
    with open(filepath, "wb") as f:
        f.write(img_data)

    return filepath
