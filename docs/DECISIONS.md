# Technical Decisions

## Model Selection
- Single model: `qwen3.5-4b-nsfw-ara-heretic-literotica-i1`
- Hardcoded for simplicity in this rebuild

## API Integration
- Single chat completion endpoint
- No model selection complexity
- Clear response parsing for reasoning and content fields

## Response Handling
- Display both `reasoning_content` and `content` fields
- Separate sections for clarity
- No filtering or processing of responses
- Show exactly what LMStudio returns

## Configuration
- Environment variables via `.env` file
- Simple configuration structure
- Clear documentation of required settings