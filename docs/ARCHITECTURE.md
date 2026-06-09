# Story Generator Application Architecture

## Overview
A simple Flask web application that sends prompts to LLM models running on LMStudio and displays the response with clear section separation. **Status: Working well.**

## Components

### Main Application
- `app.py`: Core Flask application (working) with:
  - Web interface rendering (`/`)
  - Chat endpoint (`/chat`)
  - Models endpoint (`/models`)
  - LMStudio API integration
  - Model selection support
  - Word count targeting (target and actual)
  - Clear separation of analysis and output sections

### User Interface
- `templates/index.html`: Simple interface (working) with:
  - Model dropdown selection (populated from LMStudio)
  - Target Word Count input field (guidance only, not enforced)
  - Prompt input textarea
  - Send button
  - Four display sections:
    - Your Prompt
    - Analysis / Thinking Process
    - Final Output
    - Actual Word Count (programmatically calculated)

## Data Flow
1. User selects model from dropdown
2. User enters optional target word count (AI guidance, not limit)
3. User enters prompt in textarea
4. User clicks Send button
5. Application sends prompt to LMStudio API
6. Response is parsed into sections
7. Actual word count calculated from response
8. All sections displayed with clear visual separation

## API Endpoints
- `GET /`: Main interface with model dropdown
- `POST /chat`: Send prompt and receive structured response (includes actual_word_count)
- `GET /models`: Get list of available models

## Configuration
- Host: Configurable via `LMSTUDIO_HOST` environment variable
- Port: Configurable via `LMSTUDIO_PORT` environment variable
- Timeout: 600 seconds (10 minutes)
- No max_tokens specified (uses model default)

## Important Notes
- **Target word count is not enforced** by the AI
- LLMs generate based on context and prompt instructions
- Actual word count is calculated from the response text
- Use word count as guidance, not a strict requirement

## Environment Setup
- `.env` file for sensitive configuration
- `.env.example` for setup guidance