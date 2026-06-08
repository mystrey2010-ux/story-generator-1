# Simple Chat Application

A simple Flask web application that sends prompts to a QWEN LLM model and displays responses with clear section separation.

## Features

- Simple chat interface
- Clear separation of Analysis/Thinking and Final Output
- Direct integration with LMStudio API
- Single model configuration

## Setup

1. Ensure LMStudio is running at 192.168.50.2:1234
2. Load model: `qwen3.5-4b-nsfw-ara-heretic-literotica-i1`
3. Copy `.env.example` to `.env`
4. Install dependencies: `pip install -r requirements.txt`

## Running

```bash
python app.py
```

Then open `http://localhost:5000` in your browser.

## Display Sections

1. **Your Prompt** - The original input
2. **Analysis / Thinking Process** - Model's reasoning (from `reasoning_content` field)
3. **Final Output** - Model's response (from `content` field)