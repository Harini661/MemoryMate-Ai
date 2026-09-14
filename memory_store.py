import json
import os
from datetime import datetime

MEMORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memories.json")

def load_memories():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_memory(text):
    memories = load_memories()
    new_memory = {"text": text, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    memories.append(new_memory)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memories, f, indent=2, ensure_ascii=False)
    print("Memory saved:", text, "at", new_memory["timestamp"])

def show_all_memories():
    memories = load_memories()
    print("--- ALL MEMORIES ---")
    for m in memories:
        print(m["timestamp"], "-", m["text"])
    return memories

def search_memories(query):
    memories = load_memories()
    query_words = query.lower().split()
    results = []
    for m in memories:
        if any(word in m["text"].lower() for word in query_words):
            results.append(m)
    print("--- SEARCH RESULTS for", query, "---")
    if results:
        for r in results:
            print(r["timestamp"], "-", r["text"])
    else:
        print("No matching memories found.")
    return results

def delete_memory(index):
    memories = load_memories()
    if 0 <= index < len(memories):
        deleted = memories.pop(index)
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memories, f, indent=2, ensure_ascii=False)
        return deleted
    return None