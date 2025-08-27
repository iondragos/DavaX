from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from retriever.chroma_setup import get_chroma_collection
from llm.recommender import generate_recommendation
from llm.filters import contains_offensive_language
from llm.text_to_speech import speak_text
from llm.image_generator import generate_book_image, build_image_prompt

from fastapi.staticfiles import StaticFiles
import os

from retriever.embeddings import get_embedding
from retriever.loader import build_book_summaries_from_file

app = FastAPI()

app.mount("/images", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "../images")), name="images")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def initialize_collection(collection, filepath="data/book_summaries.txt"):
    book_summaries = build_book_summaries_from_file(filepath)
    for idx, book in enumerate(book_summaries):
        embedding = get_embedding(book["summary"])
        collection.add(
            documents=[book["summary"]],
            embeddings=[embedding],
            metadatas=[{"title": book["title"]}],
            ids=[str(idx)]
        )

collection = get_chroma_collection()

if collection.count() == 0:
    initialize_collection(collection)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/recommend")
def recommend(request: PromptRequest):
    if contains_offensive_language(request.prompt):
        return {"response": "Inappropriate language!"}
    result = generate_recommendation(request.prompt, collection)
    return {"response": result}

@app.post("/image")
def image(request: PromptRequest):
    prompt = build_image_prompt(request.prompt)
    image_path = generate_book_image(prompt)
    return {"image_path": image_path}

@app.post("/speak")
def speak(request: PromptRequest):
    speak_text(request.prompt)
    return {"status": "played"}
