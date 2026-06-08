# Story Generator Flask Application

This is a Flask web application that generates stories using AI. It accepts a story prompt and target word count, then produces a story using LMStudio with the specified models.

## Features

- Web interface for generating stories
- Two-step workflow: Refine Prompt and Generate Story
- Configurable word count target
- Support for multiple AI models via dropdown selection
- Fully accessible from Windows 11 host browser via WSL
- External configuration via .env and config.json

## Setup Instructions

### Prerequisites
- WSL Fedora Linux installed
- Python 3.9+ available in WSL
- Windows 11 with browser access
- LMStudio server running

### Environment Setup
The conda environment `story-generator-1` has been created for you.

To activate the environment:
```bash
conda activate story-generator-1
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configuration
1. Copy `.env.example` to `.env`
2. Update `LMSTUDIO_HOST` to your LMStudio server address
3. Review `config.json` for application settings

## Running the Application

### Method 1: Using run script (Recommended)
```bash
./run.sh
```

### Method 2: Manual execution
```bash
# Activate environment
conda activate story-generator-1

# Run Flask app (accessible from Windows host)
python app.py
```

## Accessing from Windows 11 Browser

Since this application is running on WSL Fedora Linux, access it from your Windows 11 browser using:

```
http://localhost:5000
```

Or if that doesn't work:
```
http://127.0.0.1:5000
```

## Troubleshooting Windows Connectivity

If you cannot access the application from Windows:

### 1. Check WSL Firewall Settings
In Windows PowerShell (as Administrator):
```powershell
netsh advfirewall firewall add rule name="WSL Flask" dir=in action=allow protocol=TCP localport=5000
```

### 2. Verify WSL Network Configuration
Check that WSL is running:
```bash
wsl --list --verbose
```

### 3. Check Port Usage
Ensure no other process is using port 5000:
```bash
lsof -i :5000
```

## Application Details

The Flask application is configured to run on:
- Host: `0.0.0.0` (all interfaces)
- Port: `5000`
- Debug mode: Enabled

This configuration ensures the application is accessible from external hosts, including your Windows 11 browser.

## Usage

1. Enter a story prompt in the text area
2. Click "Refine Prompt" to improve grammar/spelling/clarity
3. Optionally check "Use refined prompt for story generation"
4. Select your preferred AI model from dropdown
5. Specify the target word count
6. Click "Generate Story"
7. View your generated story with model and word count information

## Implementation Details

The application has two main components:
- `app.py`: Main Flask application with `/generate` and `/refine` endpoints
- `templates/index.html`: HTML interface with two-step workflow

The AI story generation uses LMStudio API calls with configurable timeout and model selection. Configuration is loaded from `.env` (for sensitive data) and `config.json` (for general settings).