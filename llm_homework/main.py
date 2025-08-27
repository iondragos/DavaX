from llm.filters import contains_offensive_language
from llm.image_generator import generate_book_image, build_image_prompt
from retriever.chroma_setup import get_chroma_collection
from retriever.loader import build_book_summaries_from_file
from retriever.embeddings import get_embedding
from llm.recommender import generate_recommendation
from llm.text_to_speech import speak_text
from llm.speech_to_text import record_and_transcribe

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

def main():
    print("📚 Welcome to the Smart Librarian Chatbot!")
    print("Ask me for book recommendations based on your interests.")
    print("Type 'exit' to quit.\n")

    collection = get_chroma_collection()

    if collection.count() == 0:
        initialize_collection(collection)

    while True:
        print("\n🧠 Choose input mode:")
        print("1. 🎤 Voice")
        print("2. ⌨️  Text")
        mode = input("Select (1 or 2 or exit): ").strip()

        if mode.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        if mode == "1":
            user_input = record_and_transcribe()
            print(f"🗣️ You said: {user_input}")
        elif mode == "2":
            user_input = input("💬 You: ").strip()
        else:
            print("❌ Invalid option. Try again.")
            continue

        if contains_offensive_language(user_input):
            print("🤖 AI: I'm here to help with respectful and appropriate questions. Please try again.\n")
            continue

        reply = generate_recommendation(user_input, collection)
        print(f"\n🤖 AI: {reply}\n")

        play = input("🔊 Would you like to hear this aloud? (y/n): ").strip().lower()
        if play == "y":
            try:
                speak_text(reply)
            except Exception as e:
                print(f"❌ Error during TTS playback: {e}")

        img = input("🖼️ Do you want a generated image for this book? (y/n): ").strip().lower()
        if img == "y":
            prompt = build_image_prompt(reply)
            try:
                image_path = generate_book_image(prompt)
                print(f"📂 Image saved at: {image_path}")
            except Exception as e:
                print(f"❌ Image generation failed: {e}")

if __name__ == "__main__":
    main()
