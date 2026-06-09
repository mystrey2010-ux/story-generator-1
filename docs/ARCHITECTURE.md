# Story Generator Application Architecture

## Overview
A simple Flask web application that sends prompts to LLM models running on LMStudio and displays the response with clear section separation.

## Components

### Main Application
- `app.py`: Core Flask application with:
  - Web interface rendering (`/`)
  - Chat endpoint (`/chat`)
  - Models endpoint (`/models`)
  - LMStudio API integration
  - Model selection support
  - Word count target support
  - Clear separation of analysis and output sections

### User Interface
- `templates/index.html`: Simple interface with:
  - Model dropdown selection
  - Target Word Count input field
  - Prompt input textarea
  - Send button
  - Three clearly separated display sections:
    - Your Prompt
    - Analysis / Thinking Process
    - Final Output

## Data Flow
1. User selects model from dropdown
2. User enters optional target word count
3. User enters prompt in textarea
4. User clicks Send button
5. Application sends prompt to LMStudio API
6. Response is parsed into sections
7. All sections displayed with clear visual separation

## API Endpoints
- `GET /`: Main interface with model dropdown
- `POST /chat`: Send prompt and receive structured response
- `GET /models`: Get list of available models

## Configuration
- Host: Configurable via `LMSTUDIO_HOST` environment variable
- Port: Configurable via `LMSTUDIO_PORT` environment variable
- Timeout: 300 seconds
- No max_tokens specified (uses model default)

## Environment Setup
- `.env` file for sensitive configuration
- `.env.example` for setup guidance