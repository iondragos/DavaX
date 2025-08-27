import json

from openai import OpenAI

from llm.tools import get_summary_by_title
from retriever.retriever import semantic_retriever

client = OpenAI()

def generate_recommendation(user_question: str, collection) -> str:
    docs, metas = semantic_retriever(user_question, collection)

    context = "\n\n".join(
        [f"Title: {meta['title']}\nSummary: {doc}" for doc, meta in zip(docs, metas)]
    )

    system_prompt = (
        "You are a book recommendation assistant. "
        "Recommend exactly ONE book from the provided context. "
        "After your recommendation, you must call the tool `get_summary_by_title` using the exact title. "
        "Do NOT ask the user anything. Just return a short, friendly recommendation message, "
        "then use the tool to provide the full summary for that book."
    )

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_summary_by_title",
                "description": "Get the full detailed summary for a specific book",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The exact title of the book"
                        }
                    },
                    "required": ["title"]
                }
            }
        }
    ]

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{user_question}\n\nContext:\n{context}"}
    ]

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.0
    )

    first_message = response.choices[0].message

    if not first_message.tool_calls:
        return first_message.content

    tool_call = first_message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)
    title = args.get("title")

    tool_result = get_summary_by_title(title)

    messages.append({
        "role": "assistant",
        "tool_calls": [tool_call]
    })
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "name": "get_summary_by_title",
        "content": tool_result
    })

    final_response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages,
        temperature=0.0
    )

    return final_response.choices[0].message.content
