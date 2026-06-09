# Story Generator Application Architecture

## Overview
A Flask web application with encrypted server-side sessions for LLM interactions via LMStudio. **Status: Working.**

## Components

### Main Application
- `app.py`: Flask application with:
  - Encrypted filesystem sessions
  - Chat history with memory
  - System message prioritization for word count
  - NIST 800-88 secure file deletion

### User Interface
- `templates/index.html`: Modern webchat interface with:
  - Chat bubble design (similar to Gemini/ChatGPT/Copilot)
  - Model dropdown selection
  - Target Word Count input field
  - NEW Chat button
  - Auto-expanding textarea
  - Animated loading indicator

## Session Architecture
- **Cookie**: Only stores `sid` (64-char hex session ID)
- **Server Storage**: `/tmp/flask_session/{sid}` - encrypted with Fernet (AES-128)
- **Encryption Key**: `/tmp/flask_session_key`
- **No Cookie Size Limit**: All chat history in encrypted server files

## Chat Flow
1. Browser gets/sets `sid` cookie
2. Session data loaded from encrypted file `/tmp/flask_session/{sid}`
3. Prompts appended to chat history
4. Full conversation sent to LMStudio API
5. Response added to history and saved encrypted
6. NEW Chat triggers secure file deletion (3-pass overwrite)

## API Endpoints
- `GET /`: Load session and render chat interface
- `POST /chat`: Send prompt, receive response, update encrypted session
- `POST /clear`: Secure delete session file (NIST 800-88)
- `GET /models`: Get available LMStudio models

## Configuration
- Host: `LMSTUDIO_HOST` environment variable
- Port: `LMSTUDIO_PORT` environment variable
- Timeout: 600 seconds (10 minutes)
- Secret key: `SECRET_KEY` for signing cookies

## Security
- ✅ NIST 800-88 compliant cryptographic erase
- ✅ Server-side encrypted session storage (Fernet/AES-128)
- ✅ Session files cleared on startup
- ✅ httponly and samesite cookies