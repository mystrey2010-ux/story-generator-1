# Technical Decisions

## Model Selection
- Dynamic model selection via dropdown
- Models fetched from LMStudio `/v1/models` endpoint
- Falls back to default model if API unavailable

## API Integration
- No max_tokens parameter (uses model default)
- Temperature: 0.7 for balanced creativity
- Timeout: 300 seconds for long-running requests
- Support for both model selection and word count targets

## Response Handling
- Display `content` field as Final Output
- Display `reasoning_content` field as Analysis/Thinking
- No filtering or processing of responses
- Show exactly what LMStudio returns

## User Interface
- Model dropdown populated on page load
- Target Word Count is optional
- If word count provided, appended to prompt automatically

## Configuration
- Environment variables via `.env` file
- Simple configuration structure
- Clear documentation of required settings