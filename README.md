# Story Generator Flask Application

This is a Flask web application that generates stories using AI. It accepts a story prompt and target word count, then produces a story using LMStudio with the specified models.

## Features

- Web interface for generating stories
- Configurable word count target
- Support for primary and fallback AI models
- Fully accessible from Windows 11 host browser via WSL

## Setup Instructions

### Prerequisites
- WSL Fedora Linux installed
- Python 3.9+ available in WSL
- Windows 11 with browser access

### Environment Setup
The conda environment `story-generator-1` has been created for you.

To activate the environment:
```bash
conda activate story-generator-1
```

Alternatively, you can use the provided setup script to create and configure the environment:
```bash
./conda_setup.sh
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

### Method 1: Using the final run script (Recommended)
```bash
./final_run_story_generator.sh
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

## Configuration

The application is configured to use:
- Primary model: `lmstudio/qwen/qwen3-coder-30b`
- Fallback model: `openrouter/poolside/laguna-m.1:free gemma-4-e4b-uncensored-hauhaucs-aggressive`

## Usage

1. Enter a story prompt in the text area
2. Specify the target word count
3. Click "Generate Story"
4. View your generated story

## Implementation Details

The application has two main components:
- `app.py`: Main Flask application with story generation endpoint
- `templates/index.html`: HTML interface for user input

The AI story generation is implemented using LMStudio API calls. The implementation includes error handling and fallback mechanisms when the primary model is unavailable.

Note: This implementation provides a framework for connecting to LMStudio. Actual API integration would require running an LMStudio server and adapting the API calls accordingly.

## File Structure
```
story-generator-1/
├── app.py                 # Main Flask application
├── requirements.txt  # Python dependencies
├── run.sh              # Simple run script
├── run_app.sh              # Enhanced run script with setup
├── final_run_story_generator.sh  # Direct execution script for conda environment
├── conda_setup.sh          # Script to create and configure conda environment
├── README.md              # This file
└── templates/
    └── index.html         # Web interface
```