# Known Issues

## Connectivity
- Requires LMStudio running at configured IP address (default: 192.168.50.2)
- May timeout on slow systems (5 minute timeout configured)

## Model Availability
- Requires specific model: `qwen3.5-4b-nsfw-ara-heretic-literotica-i1`
- Model must be loaded in LMStudio

## Response Fields
- Some models return responses in `reasoning_content` instead of `content`
- Both fields displayed - one may be empty
- No filtering applied to response text