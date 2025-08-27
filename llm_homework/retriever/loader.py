def build_book_summaries_from_file(filepath: str):
    book_summaries = []
    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    current_title = None
    current_summary_lines = []

    for line in lines:
        line = line.strip()
        if line.startswith("## Title:"):
            if current_title and current_summary_lines:
                book_summaries.append({
                    "title": current_title,
                    "summary": " ".join(current_summary_lines).strip()
                })
                current_summary_lines = []
            current_title = line.replace("## Title:", "").strip()
        elif line:
            current_summary_lines.append(line)

    if current_title and current_summary_lines:
        book_summaries.append({
            "title": current_title,
            "summary": " ".join(current_summary_lines).strip()
        })

    return book_summaries
