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

## API Endpoints
- `GET /`: Serve main web interface
- `GET /models`: List available LMStudio models
- `POST /generate`: Generate story from prompt and parameters

## Configuration
- Default AI model: Configurable via config.json
- Host: `0.0.0.0` (accessible from external hosts)
- Port: `5000`
- Timeout: 300 seconds (5 minutes) for API calls

## Environment Setup
- `run.sh`: Script to activate conda environment and run the Flask application