# Technical Decisions

## Model Selection
- Single model: `qwen3.5-4b-nsfw-ara-heretic-literotica-i1`
- Hardcoded for simplicity in this implementation

## API Integration
- Single chat completion endpoint
- No model selection complexity
- Clear response parsing for reasoning and content fields

## Response Handling
- Display `content` field as Final Output
- Display `reasoning_content` field as Analysis/Thinking
- No filtering or processing of responses
- Show exactly what LMStudio returns

## Token Configuration
- max_tokens: 262144 (full context length)
- timeout: 300 seconds (5 minutes)
- Appropriate for local LLM processing

## Configuration
- Environment variables via `.env` file
- Simple configuration structure
- Clear documentation of required settings