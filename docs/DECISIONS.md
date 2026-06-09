# Technical Decisions

## Model Selection
- Dynamic model selection via dropdown
- Models fetched from LMStudio `/v1/models` endpoint
- Falls back to default model if API unavailable
- ✅ Working well

## API Integration
- No max_tokens parameter (uses model default)
- Temperature: 0.7 for balanced creativity
- Timeout: 600 seconds (10 minutes) for long-running requests
- ⚠️ Note: LLMs do not enforce target word counts

## Response Handling
- Display `content` field as Final Output
- Display `reasoning_content` field as Analysis/Thinking
- Calculate actual word count from response text
- Show both target and actual word counts
- No filtering or processing of responses
- ✅ Working well

## User Interface
- Model dropdown populated on page load
- Target Word Count: Suggestion to AI, not enforced
- Actual Word Count: Programmatic calculation
- Clean section separation with color coding
- ✅ Working well

## Known Limitations
- LLMs cannot be forced to match exact word counts
- Target word count is just an instruction in the prompt
- Actual count will vary significantly from target
- Best for guidance only