# Story Generator Application Architecture

## Overview
A simple Flask web application that sends prompts to a QWEN LLM model running on LMStudio and displays the response with clear section separation.

## Components

### Main Application
- `app.py`: Core Flask application with:
  - Web interface rendering (`/`)
  - Chat endpoint (`/chat`)
  - LMStudio API integration
  - Clear separation of analysis and output sections

### User Interface
- `templates/index.html`: Simple interface with:
  - Prompt input textarea
  - Send button
  - Three clearly separated display sections:
    - Your Prompt
    - Analysis / Thinking Process
    - Final Output

## Data Flow
1. User enters prompt in textarea
2. User clicks Send button
3. Application sends prompt to LMStudio API
4. Response is parsed into sections
5. All sections displayed with clear visual separation

## API Endpoint
- `POST /chat`: Send prompt and receive structured response

## Configuration
- Model: `qwen3.5-4b-nsfw-ara-heretic-literotica-i1`
- Host: Configurable via `LMSTUDIO_HOST` environment variable
- Port: Configurable via `LMSTUDIO_PORT` environment variable
- Max tokens: 262144 (full context length)
- Timeout: 300 seconds (5 minutes)

## Environment Setup
- `.env` file for sensitive configuration
- `.env.example` for setup guidance