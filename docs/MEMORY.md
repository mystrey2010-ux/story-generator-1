# Project Memory

## Key Insights
- System message BEFORE prompt helps prioritize word count goals
- Session storage enables multi-turn chat
- LLM still cannot perfectly enforce word counts
- Actual count calculated from response text
- Webchat interface improves UX significantly

## Configuration Notes
- SECRET_KEY needed for session security
- Chat history persists until explicit clear
- System message approach improves word count targeting

## Features Working
- ✅ Dynamic model selection
- ✅ Target word count (system priority)
- ✅ Actual word count calculation
- ✅ Session-based chat history
- ✅ NEW Chat button
- ✅ Scrollable interface