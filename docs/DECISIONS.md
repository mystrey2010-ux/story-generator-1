# Technical Decisions

## UI Design
- Modern chat bubble interface (Gemini/ChatGPT style)
- Auto-expanding textarea for better UX
- "You" / "Assistant" labels for clear context
- Word count per message in small text
- ✅ Working well

## Chat Memory
- Flask sessions store chat history
- System message added per prompt
- NEW Chat button clears session
- ✅ Working well

## Performance
- No max_tokens (uses model default)
- 10-minute timeout for long generations
- Optimized for readability