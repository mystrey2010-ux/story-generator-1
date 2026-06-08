# Story Generator Application Architecture

## Overview
This is a Flask web application that generates stories using AI models via LMStudio API. The application provides a web interface for users to enter story prompts and target word counts, then generates stories using configured AI models.

## Components

### Main Application
- `app.py`: Core Flask application with:
  - Web interface rendering (`/`)
  - Model listing endpoint (`/models`) 
  - Story generation endpoint (`/generate`)
  - LMStudio API integration for model discovery and story generation
  - Fallback mechanism using specific gemma model
  - Configuration loading from config.json

### User Interface
- `templates/index.html`: HTML form with:
  - Story prompt input
  - Model selection dropdown (populated via `/models` endpoint)
  - Word count selector
  - Generate button
  - Display of refined prompt used for generation

### Configuration
- `config.json`: External configuration file containing:
  - LMStudio host and port settings
  - Default AI model specification
  - Application configuration (host, port, timeout)

## Data Flow
1. User accesses web interface at `/`
2. Frontend calls `/models` to populate model dropdown
3. User submits story prompt and parameters
4. Application calls `/generate` endpoint
5. Application refines prompt using selected model or default gemma model
6. Application generates story using selected model or fallback gemma model
7. Response returned to user with generated story, actual word count, model used, and refined prompt

## API Endpoints
- `GET /`: Serve main web interface
- `GET /models`: List available LMStudio models
- `POST /generate`: Generate story from prompt and parameters

## Configuration
- Default AI model: `google/gemma-4-e4b@q4_k_m`
- Host: `0.0.0.0` (accessible from external hosts)
- Port: `5000`
- Timeout: 300 seconds (5 minutes) for API calls

## Environment Setup
- `run.sh`: Script to activate conda environment and run the Flask application