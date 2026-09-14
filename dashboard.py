import tkinter as tk
from tkinter import font as tkfont
from datetime import datetime
from memory_store import load_memories

# ---------------- Colors ----------------
BG_DARK = "#0F172A"
CARD_BG = "#1E293B"
TEXT_LIGHT = "#E2E8F0"
TEXT_MUTED = "#94A3B8"
ACCENT_BLUE = "#38BDF8"
GREEN = "#22C55E"

def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good Morning"
    elif hour < 17:
        return "Good Afternoon"
    else:
        return "Good Evening"

def time_ago(timestamp_str):
    try:
        ts = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        diff = datetime.now() - ts
        if diff.days > 0:
            return f"{diff.days} day(s) ago"
        hours = diff.seconds // 3600
        if hours > 0:
            return f"{hours} hour(s) ago"
        minutes = diff.seconds // 60
        return f"{minutes} min(s) ago" if minutes > 0 else "Just now"
    except:
        return timestamp_str

def open_dashboard(parent, user_name="Harini"):
    win = tk.Toplevel(parent)
    win.title("MemoryMate AI - Dashboard")
    win.geometry("480x650")
    win.configure(bg=BG_DARK)

    heading_font = tkfont.Font(family="Segoe UI", size=18, weight="bold")
    section_font = tkfont.Font(family="Segoe UI", size=12, weight="bold")
    normal_font = tkfont.Font(family="Segoe UI", size=10)

    # ---- Header ----
    greeting = tk.Label(win, text=f"{get_greeting()}, {user_name} 👋",
                         font=heading_font, bg=BG_DARK, fg=ACCENT_BLUE)
    greeting.pack(pady=(20, 2), anchor="w", padx=20)

    subtitle = tk.Label(win, text="Your Personal Memory Assistant",
                         font=("Segoe UI", 9), bg=BG_DARK, fg=TEXT_MUTED)
    subtitle.pack(anchor="w", padx=20, pady=(0, 15))

    # ---- Recent Memories Section ----
    memories = load_memories()

    memories_card = tk.Frame(win, bg=CARD_BG)
    memories_card.pack(fill="both", expand=True, padx=20, pady=8)

    tk.Label(memories_card, text="🧠 Recent Memories", font=section_font,
             bg=CARD_BG, fg=TEXT_LIGHT).pack(anchor="w", padx=15, pady=(15, 10))

    if memories:
        recent = list(reversed(memories[-5:]))  # last 5, newest first
        for m in recent:
            item = tk.Frame(memories_card, bg="#273449")
            item.pack(fill="x", padx=15, pady=5)
            tk.Label(item, text=f"\"{m['text'].strip()}\"", font=normal_font,
                     bg="#273449", fg=TEXT_LIGHT, anchor="w", wraplength=400,
                     justify="left").pack(anchor="w", padx=10, pady=(8, 2))
            tk.Label(item, text=time_ago(m['timestamp']), font=("Segoe UI", 8),
                     bg="#273449", fg=TEXT_MUTED, anchor="w").pack(anchor="w", padx=10, pady=(0, 8))
    else:
        tk.Label(memories_card, text="No memories saved yet.\nRecord your first memory!",
                 font=normal_font, bg=CARD_BG, fg=TEXT_MUTED, justify="left").pack(anchor="w", padx=15, pady=10)

    # ---- AI Insight Section (real data) ----
    total = len(memories)
    today_count = sum(1 for m in memories if m['timestamp'].startswith(datetime.now().strftime("%Y-%m-%d")))

    insight_card = tk.Frame(win, bg="#1E3A5F")
    insight_card.pack(fill="x", padx=20, pady=15)

    if total == 0:
        insight_text = "💡 Start recording to build your memory timeline."
    else:
        insight_text = f"💡 You have {total} saved memories total, {today_count} added today."

    tk.Label(insight_card, text=insight_text, font=("Segoe UI", 10, "italic"),
             bg="#1E3A5F", fg=ACCENT_BLUE, wraplength=420, justify="left").pack(padx=15, pady=12, anchor="w")

    win.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_dashboard(root)
    root.mainloop()