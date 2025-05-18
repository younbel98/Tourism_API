import os
import json

MEMORY_PATH = os.path.join(os.path.dirname(__file__), "../data/memory")
os.makedirs(MEMORY_PATH, exist_ok=True)


def _memory_file(user_id):
    return os.path.join(MEMORY_PATH, f"{user_id}.json")


def get_user_messages(user_id):
    path = _memory_file(user_id)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    # Start conversation with assistant system prompt
    return [
        {
            "role": "system",
            "content": "You are a multilingual tourism assistant. Answer clearly, give ecological facts, quiz questions, and location-based guidance.",
        }
    ]


def save_user_message(user_id, role, content):
    path = _memory_file(user_id)
    history = get_user_messages(user_id)
    history.append({"role": role, "content": content})
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
