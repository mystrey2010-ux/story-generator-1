# Technical Decisions

## Chat Memory
- Flask sessions store chat history
- **System message added PER PROMPT** (word count can change)
- History maintained across multiple prompts
- NEW Chat button clears session explicitly
- ✅ Working well

## API Integration
- Temperature: 0.7 for balanced creativity
- Timeout: 600 seconds (10 minutes)
- No max_tokens (uses model default)
- System message added each request for word count priority
- ✅ Working well

## User Interface
- Webchat-style interface
- Scrollable chat history
- CLEAR distinction between user/assistant messages
- Word count displayed per response
- NEW Chat button for fresh start
- ✅ Working well

## Session Management
- SECRET_KEY required for session security
- Session data cleared on NEW Chat click
- Chat persists until explicit clear