# Story Generator Application Architecture

## Overview
A Flask web application with chat memory for LLM interactions via LMStudio. **Status: Working well with modern UI.**

## Components

### Main Application
- `app.py`: Flask application with chat history, session management, and memory

### User Interface
- `templates/index.html`: Modern webchat interface with:
  - Chat bubble design (similar to Gemini/ChatGPT/Copilot)
  - Model dropdown selection
  - Target Word Count input field
  - NEW Chat button (clears session)
  - Auto-expanding textarea
  - Scrollable chat history
  - Message labels ("You" / "Assistant")
  - Word count per response

## Chat Flow
1. User types in modern input area (auto-expands)
2. User selects model and optional target word count
3. Response appears in chat bubble format
4. Chat history maintained with sessions
5. NEW Chat clears all session data

## API Endpoints
- `GET /`: Chat interface with history
- `POST /chat`: Send prompt with system message for word count
- `POST /clear`: Clear session
- `GET /models`: Get available models

## Configuration
- Host: `LMSTUDIO_HOST` environment variable
- Port: `LMSTUDIO_PORT` environment variable
- Timeout: 600 seconds (10 minutes)
- No max_tokens (uses model default)

## Important Notes
- Target word count prioritized via system message per prompt
- Each prompt can have different word count target
- System message ensures goal stays in context
- Actual word count calculated from response text
- LLMs still may vary significantly from targets