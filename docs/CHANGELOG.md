# Changelog

## [1.0.0] - Simple Chat App Release

### Added
- Simple Flask web application
- Single chat endpoint (`/chat`)
- Clear section separation for API responses
- Analysis/Thinking section display
- Final Output section display
- Environment configuration via `.env`

### Configuration
- Model: `qwen3.5-4b-nsfw-ara-heretic-literotica-i1`
- Max tokens: 262144 (full context length)
- Timeout: 300 seconds

### Changed
- Completely rebuilt from previous complex implementation
- Simplified to basic chat functionality
- Streamlined interface

### Removed
- Previous two-step story generation workflow
- Multiple model selection
- Complex refinement features