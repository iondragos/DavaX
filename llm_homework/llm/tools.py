from retriever.loader import build_book_summaries_from_file

SUMMARY_FILE_PATH = "data/book_summaries.txt"

book_summaries_list = build_book_summaries_from_file(SUMMARY_FILE_PATH)
book_summaries_dict = {entry["title"]: entry["summary"] for entry in book_summaries_list}

def get_summary_by_title(title: str) -> str:
    return book_summaries_dict.get(title, "Sorry, no detailed summary available for this title.")
