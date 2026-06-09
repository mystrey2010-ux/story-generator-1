# Changelog

## [1.3.0] - Chat History & Webchat Interface

### Added
- Session-based chat history (persists across prompts)
- NEW Chat button to clear session
- Scrollable chat display
- System message prioritized BEFORE user prompts
- Word count as system-level priority

### Changed
- Upgraded to webchat-style interface
- Removed separate analysis section for cleaner chat flow
- Chat history maintained via Flask sessions

### Fixed
- Word count goal now emphasized as system instruction

## [1.2.0] - Added Actual Word Count
- Programmatic word count calculation

## [1.1.0] - Enhanced Configuration
- Model dropdown, word count input

## [1.0.0] - Simple Chat App Release