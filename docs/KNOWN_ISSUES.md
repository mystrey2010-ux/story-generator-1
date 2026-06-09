# Known Issues

## Connectivity
- Requires LMStudio running at configured IP address
- May timeout on slow systems (5 minute timeout configured)
- Model list endpoint may fail silently (falls back to default)

## Model Behavior
- Model uses extensive reasoning/thinking mode
- `content` field may be empty for complex prompts
- `reasoning_content` contains both analysis and final output

## Configuration
- Using model default max_tokens (no specified limit)
- Response times vary by model and prompt complexity

## Status Notes
✅ All features working well in current implementation
- Actual word count now calculated programmatically