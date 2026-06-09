# Changelog

## [1.1.0] - Enhanced Configuration

### Added
- Model dropdown selection from available LMStudio models
- Target Word Count input field for story generation
- `/models` endpoint to fetch available models
- Dynamic model loading from LMStudio API

### Removed
- Hardcoded max_tokens parameter (now uses model default)

## [1.0.0] - Simple Chat App Release

### Added
- Simple Flask web application
- Single chat endpoint (`/chat`)
- Clear section separation for API responses
- Analysis/Thinking section display
- Final Output section display
- Environment configuration via `.env`

### Changed
- Completely rebuilt from previous complex implementation
- Simplified to basic chat functionality
- Streamlined interface