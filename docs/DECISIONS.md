# Technical Decisions

## Model Selection
- Dynamic model selection via dropdown
- Models fetched from LMStudio `/v1/models` endpoint
- Falls back to default model if API unavailable
- ✅ Working well

## API Integration
- No max_tokens parameter (uses model default)
- Temperature: 0.7 for balanced creativity
- Timeout: 300 seconds for long-running requests
- ✅ Working well

## Response Handling
- Display `content` field as Final Output
- Display `reasoning_content` field as Analysis/Thinking
- Calculate actual word count from response text
- No filtering or processing of responses
- Show exactly what LMStudio returns
- ✅ Working well

## User Interface
- Model dropdown populated on page load
- Target Word Count is optional instruction to AI
- Actual Word Count is programmatic calculation
- Clean section separation with color coding
- ✅ Working well

## Configuration
- Environment variables via `.env` file
- Simple configuration structure
- ✅ Working well