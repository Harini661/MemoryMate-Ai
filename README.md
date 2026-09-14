# 🧠 MemoryMate AI

**Your Personal On-Device Memory Assistant**

MemoryMate AI is a privacy-first, offline desktop application that lets you record voice memories, automatically transcribes them using AI, and lets you search and recall them anytime using natural language questions — all without an internet connection.

Built for the Snapdragon® AI Lab Build & Present Challenge (Qualcomm).

## Features

- Voice-to-Text Memory Capture — record a memory by speaking; Whisper AI transcribes it instantly
- Automatic Memory Storage — every memory is timestamped and saved locally
- Natural Language Search — ask "what did I do last week?" and get relevant answers
- Delete Memory — remove memories you no longer need
- Export Memories — export all saved memories to a text file
- Dashboard — view recent memories and usage insights
- Reminders — set task reminders with due-date-based desktop notifications
- Modern UI — clean, dark-themed, responsive interface built with Tkinter

## Tech Stack

- Language: Python
- AI Model: OpenAI Whisper (Base) — sourced from Qualcomm AI Hub, optimized for Snapdragon NPU (ONNX/QNN)
- GUI: Tkinter
- Audio: sounddevice, scipy
- Notifications: plyer
- Storage: Local JSON (fully on-device, no cloud dependency)

## Setup and Installation

1. Clone this repository
2. Install dependencies: pip install openai-whisper sounddevice scipy plyer numpy
3. Ensure FFmpeg is installed (required by Whisper)
4. Run the app: python app.py

## Snapdragon Optimization

The Whisper-Base model used in this project was downloaded directly from Qualcomm AI Hub (aihub.qualcomm.com), in its Snapdragon NPU-optimized (QNN/ONNX) format. The application architecture is designed for on-device inference acceleration on Snapdragon-powered HP PCs.

## Privacy

MemoryMate AI runs entirely on-device. No data is sent to the cloud — all voice recordings, transcriptions, and memories stay local to your machine.

## Author

Harini M — Individual Participant, Snapdragon AI Lab Build & Present Challenge
