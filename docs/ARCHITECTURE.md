# Story Generator Application Architecture

## Overview
A Flask web application with chat memory for LLM interactions via LMStudio. **Status: Working well with upgrades.**

## Components

### Main Application
- `app.py`: Flask application with:
  - Session-based chat history (`/chat` with memory)
  - New Chat functionality (`/clear`)
  - Models endpoint (`/models`)
  - System message priority for word count goals

### User Interface
- `templates/index.html`: Webchat interface with:
  - Model dropdown selection
  - Target Word Count input
  - NEW Chat button (clears session)
  - Scrollable chat history
  - Four display sections per message:
    - Your Prompt
    - Final Output
    - Word Count
    - Timestamp

## Chat Flow
1. User selects model
2. User enters optional target word count (becomes system priority)
3. User enters prompt
4. Response added to chat history (scrollable)
5. Additional prompts aware of previous responses
6. NEW Chat clears all session data

## API Endpoints
- `GET /`: Chat interface with history
- `POST /chat`: Send prompt, get response, update history
- `POST /clear`: Clear session
- `GET /models`: Get available models

## Configuration
- Host: `LMSTUDIO_HOST` environment variable
- Port: `LMSTUDIO_PORT` environment variable
- Timeout: 600 seconds (10 minutes)
- No max_tokens (uses model default)

## Environment Setup
- `.env` file with SECRET_KEY for sessions
- `.env.example` for setup guidance