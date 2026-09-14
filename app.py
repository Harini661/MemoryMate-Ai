import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import font as tkfont
import whisper
from memory_store import save_memory, search_memories, show_all_memories, load_memories, delete_memory
from reminder_store import save_reminder, get_due_soon_reminders, get_all_reminders
import os
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from plyer import notification
from datetime import datetime

print("Loading Whisper model... please wait")
model = whisper.load_model("base")
print("Model loaded!")

# ---------------- Theme ----------------
BG_DARK = "#111318"
CARD_BG = "#191C22"
BORDER = "#262A33"
TEXT_LIGHT = "#F3F4F6"
TEXT_MUTED = "#8B909C"
ACCENT = "#6366F1"
ACCENT_HOVER = "#4F46E5"

# ---------------- Root Window ----------------
root = tk.Tk()
root.title("MemoryMate AI")
root.geometry("480x800")
root.minsize(420, 600)
root.configure(bg=BG_DARK)
root.grid_rowconfigure(4, weight=1)
root.grid_columnconfigure(0, weight=1)

heading_font = tkfont.Font(family="Segoe UI", size=17, weight="bold")
label_font = tkfont.Font(family="Segoe UI", size=9)
normal_font = tkfont.Font(family="Segoe UI", size=10)
button_font = tkfont.Font(family="Segoe UI", size=10, weight="bold")

# ---------------- Functions ----------------
def record_and_save():
    duration = 5
    sample_rate = 16000
    log("Recording... speak now")
    root.update()
    try:
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()
        audio_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recorded_audio.wav")
        write(audio_path, sample_rate, audio_data)
        log("Converting your voice to text...")
        root.update()
        result = model.transcribe(audio_path, language="en")
        text = result["text"]
        save_memory(text)
        log(f"Memory saved: {text}")
        notification.notify(title="MemoryMate AI", message=f"Memory saved: {text[:50]}", timeout=5)
    except Exception as e:
        log(f"Error: {e}")

def ask_question():
    query = question_entry.get()
    if not query.strip() or query.startswith("Ask something"):
        messagebox.showwarning("Empty", "Please type a question")
        return
    log(f"Question: {query}")
    memories = search_memories(query)
    if memories:
        for m in memories:
            log(f"[{m['timestamp']}] {m['text']}")
    else:
        log("No matching memories found.")
    question_entry.delete(0, tk.END)

def show_all():
    memories = load_memories()
    if not memories:
        log("No memories saved yet.")
        return
    log("---- All Saved Memories ----")
    for i, m in enumerate(memories):
        log(f"[{i}] {m['timestamp']} - {m['text']}")
    log("(To delete, use the Delete button and enter the number)")

def delete_memory_popup():
    show_all()
    popup = tk.Toplevel(root)
    popup.title("Delete Memory")
    popup.geometry("320x180")
    popup.configure(bg=BG_DARK)
    popup.resizable(False, False)
    popup.transient(root)
    popup.grab_set()

    tk.Label(popup, text="🗑️ Delete Memory", font=("Segoe UI", 13, "bold"),
             bg=BG_DARK, fg=TEXT_LIGHT).pack(pady=(20, 10))
    tk.Label(popup, text="Enter memory number to delete:", font=("Segoe UI", 9),
             bg=BG_DARK, fg=TEXT_MUTED).pack(anchor="w", padx=25)

    entry_frame = tk.Frame(popup, bg=CARD_BG, highlightbackground=BORDER, highlightthickness=1)
    entry_frame.pack(fill="x", padx=25, pady=(6, 15))
    num_entry = tk.Entry(entry_frame, font=("Segoe UI", 10), bg=CARD_BG, fg=TEXT_LIGHT,
                          insertbackground=TEXT_LIGHT, relief="flat", bd=0)
    num_entry.pack(fill="x", padx=10, ipady=8)
    num_entry.focus()

    def confirm_delete():
        try:
            idx = int(num_entry.get().strip())
            deleted = delete_memory(idx)
            if deleted:
                log(f"Deleted: {deleted['text']}")
            else:
                log("Invalid memory number.")
        except:
            log("Please enter a valid number.")
        popup.destroy()

    delete_btn = tk.Button(popup, text="Delete", command=confirm_delete, font=button_font,
                            bg="#EF4444", fg="white", activebackground="#DC2626", activeforeground="white",
                            relief="flat", bd=0, padx=10, pady=10, cursor="hand2")
    delete_btn.pack(fill="x", padx=25)
    num_entry.bind("<Return>", lambda e: confirm_delete())

def export_memories():
    memories = load_memories()
    if not memories:
        log("No memories to export.")
        return

    export_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MemoryMate_Export.txt")
    with open(export_path, "w", encoding="utf-8") as f:
        f.write("=== MemoryMate AI - Exported Memories ===\n\n")
        for i, m in enumerate(memories):
            f.write(f"[{i}] {m['timestamp']}\n{m['text']}\n\n")

    log(f"Exported {len(memories)} memories (MemoryMate_Export.txt)")
    notification.notify(title="MemoryMate AI", message="Memories exported!", timeout=5)

def clear_log():
    output_box.configure(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.configure(state="disabled")

def log(message):
    output_box.configure(state="normal")
    output_box.insert(tk.END, message + "\n\n")
    output_box.configure(state="disabled")
    output_box.see(tk.END)

def on_entry_focus_in(event):
    if question_entry.get().startswith("Ask something"):
        question_entry.delete(0, tk.END)
        question_entry.config(fg=TEXT_LIGHT)

def on_entry_focus_out(event):
    if not question_entry.get().strip():
        question_entry.insert(0, "Ask something... e.g. 'project'")
        question_entry.config(fg=TEXT_MUTED)

def on_enter_key(event):
    ask_question()

def open_dashboard_window():
    from dashboard import open_dashboard
    open_dashboard(root)

def add_reminder_popup():
    popup = tk.Toplevel(root)
    popup.title("Add Reminder")
    popup.geometry("360x300")
    popup.configure(bg=BG_DARK)
    popup.resizable(False, False)
    popup.transient(root)
    popup.grab_set()

    tk.Label(popup, text="⏰ New Reminder", font=("Segoe UI", 14, "bold"),
             bg=BG_DARK, fg=TEXT_LIGHT).pack(pady=(20, 15))

    tk.Label(popup, text="What do you need to remember?", font=("Segoe UI", 9),
             bg=BG_DARK, fg=TEXT_MUTED).pack(anchor="w", padx=25)

    task_frame = tk.Frame(popup, bg=CARD_BG, highlightbackground=BORDER, highlightthickness=1)
    task_frame.pack(fill="x", padx=25, pady=(6, 15))
    task_entry = tk.Entry(task_frame, font=("Segoe UI", 10), bg=CARD_BG, fg=TEXT_LIGHT,
                           insertbackground=TEXT_LIGHT, relief="flat", bd=0)
    task_entry.pack(fill="x", padx=10, ipady=8)
    task_entry.focus()

    tk.Label(popup, text="Due date (YYYY-MM-DD)", font=("Segoe UI", 9),
             bg=BG_DARK, fg=TEXT_MUTED).pack(anchor="w", padx=25)

    date_frame = tk.Frame(popup, bg=CARD_BG, highlightbackground=BORDER, highlightthickness=1)
    date_frame.pack(fill="x", padx=25, pady=(6, 20))
    date_entry = tk.Entry(date_frame, font=("Segoe UI", 10), bg=CARD_BG, fg=TEXT_LIGHT,
                           insertbackground=TEXT_LIGHT, relief="flat", bd=0)
    date_entry.pack(fill="x", padx=10, ipady=8)

    def submit():
        task = task_entry.get().strip()
        due_date = date_entry.get().strip()
        if not task:
            messagebox.showwarning("Missing Info", "Please enter a task")
            return
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except:
            messagebox.showerror("Invalid Date", "Please enter date as YYYY-MM-DD")
            return
        save_reminder(task, due_date)
        log(f"Reminder set: {task} due {due_date}")
        notification.notify(title="MemoryMate AI - Reminder Set", message=f"{task} (due {due_date})", timeout=5)
        popup.destroy()

    btn_frame = tk.Frame(popup, bg=BG_DARK)
    btn_frame.pack(fill="x", padx=25)

    cancel_btn = tk.Button(btn_frame, text="Cancel", command=popup.destroy, font=button_font,
                            bg=CARD_BG, fg=TEXT_LIGHT, activebackground="#20242C", activeforeground=TEXT_LIGHT,
                            relief="flat", bd=0, padx=10, pady=10, cursor="hand2")
    cancel_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

    save_btn = tk.Button(btn_frame, text="Save", command=submit, font=button_font,
                          bg=ACCENT, fg="white", activebackground=ACCENT_HOVER, activeforeground="white",
                          relief="flat", bd=0, padx=10, pady=10, cursor="hand2")
    save_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))

    date_entry.bind("<Return>", lambda e: submit())

def check_due_reminders():
    due_soon = get_due_soon_reminders(days_threshold=2)
    for r in due_soon:
        days_left = r["days_left"]
        time_text = "DUE TODAY" if days_left == 0 else ("due tomorrow" if days_left == 1 else f"due in {days_left} days")
        notification.notify(title="MemoryMate AI Reminder", message=f"{r['task']} — {time_text}", timeout=8)
    if due_soon:
        log(f"You have {len(due_soon)} reminder(s) due soon")

def make_flat_button(parent, text, command, bg=ACCENT, hover=ACCENT_HOVER, fg="white"):
    btn = tk.Button(parent, text=text, command=command, font=button_font,
                     bg=bg, fg=fg, activebackground=hover, activeforeground=fg,
                     relief="flat", bd=0, padx=10, pady=11, cursor="hand2")
    btn.bind("<Enter>", lambda e: btn.config(bg=hover))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn

# ---------------- Header ----------------
header = tk.Frame(root, bg=BG_DARK)
header.grid(row=0, column=0, sticky="ew", padx=28, pady=(28, 4))

title_label = tk.Label(header, text="🧠 MemoryMate AI", font=heading_font, bg=BG_DARK, fg=TEXT_LIGHT)
title_label.pack(anchor="w")

subtitle = tk.Label(header, text="Personal on-device memory assistant",
                     font=label_font, bg=BG_DARK, fg=TEXT_MUTED)
subtitle.pack(anchor="w", pady=(2, 0))

divider = tk.Frame(root, bg=BORDER, height=1)
divider.grid(row=1, column=0, sticky="ew", padx=28, pady=(14, 14))

# ---------------- Primary Actions ----------------
actions = tk.Frame(root, bg=BG_DARK)
actions.grid(row=2, column=0, sticky="ew", padx=28)
actions.grid_columnconfigure(0, weight=1)
actions.grid_columnconfigure(1, weight=1)

record_btn = make_flat_button(actions, "🎤 Record Memory", record_and_save)
record_btn.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 8))

dashboard_btn = make_flat_button(actions, "🏠 Dashboard", open_dashboard_window, bg=CARD_BG, hover="#20242C", fg=TEXT_LIGHT)
dashboard_btn.grid(row=1, column=0, sticky="ew", padx=(0, 4), pady=4)

reminder_btn = make_flat_button(actions, "⏰ Reminder", add_reminder_popup, bg=CARD_BG, hover="#20242C", fg=TEXT_LIGHT)
reminder_btn.grid(row=1, column=1, sticky="ew", padx=(4, 0), pady=4)

show_btn = make_flat_button(actions, "📋 Show All Memories", show_all, bg=CARD_BG, hover="#20242C", fg=TEXT_LIGHT)
show_btn.grid(row=2, column=0, columnspan=2, sticky="ew", pady=4)

delete_btn_main = make_flat_button(actions, "🗑️ Delete Memory", delete_memory_popup, bg=CARD_BG, hover="#20242C", fg=TEXT_LIGHT)
delete_btn_main.grid(row=3, column=0, columnspan=2, sticky="ew", pady=4)

export_btn = make_flat_button(actions, "📤 Export Memories", export_memories, bg=CARD_BG, hover="#20242C", fg=TEXT_LIGHT)
export_btn.grid(row=4, column=0, columnspan=2, sticky="ew", pady=4)

# ---------------- Ask Section ----------------
ask_section = tk.Frame(root, bg=BG_DARK)
ask_section.grid(row=3, column=0, sticky="ew", padx=28, pady=(16, 0))
ask_section.grid_columnconfigure(0, weight=1)

ask_label = tk.Label(ask_section, text="ASK YOUR MEMORIES", font=("Segoe UI", 8, "bold"),
                      bg=BG_DARK, fg=TEXT_MUTED)
ask_label.grid(row=0, column=0, sticky="w", pady=(0, 6))

entry_frame = tk.Frame(ask_section, bg=CARD_BG, highlightbackground=BORDER, highlightthickness=1)
entry_frame.grid(row=1, column=0, sticky="ew")
entry_frame.grid_columnconfigure(0, weight=1)

question_entry = tk.Entry(entry_frame, font=normal_font, bg=CARD_BG, fg=TEXT_MUTED,
                           insertbackground=TEXT_LIGHT, relief="flat", bd=0)
question_entry.grid(row=0, column=0, sticky="ew", padx=12, ipady=10)
question_entry.insert(0, "Ask something... e.g. 'project'")
question_entry.bind("<FocusIn>", on_entry_focus_in)
question_entry.bind("<FocusOut>", on_entry_focus_out)
question_entry.bind("<Return>", on_enter_key)

ask_btn = tk.Button(entry_frame, text="🔍 Ask", command=ask_question, font=button_font,
                     bg=ACCENT, fg="white", activebackground=ACCENT_HOVER, activeforeground="white",
                     relief="flat", bd=0, padx=18, cursor="hand2")
ask_btn.grid(row=0, column=1, sticky="ns", padx=(0, 4), pady=4)
ask_btn.bind("<Enter>", lambda e: ask_btn.config(bg=ACCENT_HOVER))
ask_btn.bind("<Leave>", lambda e: ask_btn.config(bg=ACCENT))

# ---------------- Activity Log ----------------
log_section = tk.Frame(root, bg=BG_DARK)
log_section.grid(row=4, column=0, sticky="nsew", padx=28, pady=(20, 0))
log_section.grid_rowconfigure(1, weight=1)
log_section.grid_columnconfigure(0, weight=1)

log_header = tk.Frame(log_section, bg=BG_DARK)
log_header.grid(row=0, column=0, sticky="ew", pady=(0, 8))

log_label = tk.Label(log_header, text="ACTIVITY LOG", font=("Segoe UI", 8, "bold"),
                      bg=BG_DARK, fg=TEXT_MUTED)
log_label.pack(side="left")

clear_link = tk.Label(log_header, text="Clear", font=("Segoe UI", 8, "underline"),
                       bg=BG_DARK, fg=TEXT_MUTED, cursor="hand2")
clear_link.pack(side="right")
clear_link.bind("<Button-1>", lambda e: clear_log())

output_frame = tk.Frame(log_section, bg=CARD_BG, highlightbackground=BORDER, highlightthickness=1)
output_frame.grid(row=1, column=0, sticky="nsew")
output_frame.grid_rowconfigure(0, weight=1)
output_frame.grid_columnconfigure(0, weight=1)

output_box = scrolledtext.ScrolledText(output_frame, font=("Consolas", 9),
                                        bg=CARD_BG, fg=TEXT_LIGHT, relief="flat",
                                        insertbackground=TEXT_LIGHT, state="disabled",
                                        wrap="word", bd=0, padx=12, pady=10)
output_box.grid(row=0, column=0, sticky="nsew")

# ---------------- Footer ----------------
footer = tk.Label(root, text="Powered by Whisper AI  ·  On-Device  ·  Private",
                   font=("Segoe UI", 8), bg=BG_DARK, fg="#4B5060")
footer.grid(row=5, column=0, pady=16)

root.after(1000, check_due_reminders)
root.mainloop() 