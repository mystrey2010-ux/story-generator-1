# Known Issues

## Limitations
- ⚠️ LLMs do NOT enforce target word count (just an instruction)
- Actual word count will often differ significantly from target
- Model generates based on context and prompt, not strict limits
- Example: Target 2000 words may result in 6500+ words

## Connectivity
- Requires LMStudio running at configured IP address
- May timeout on slow systems (10-minute timeout configured)
- Model list endpoint may fail silently (falls back to default)

## Model Behavior
- Model uses extensive reasoning/thinking mode
- `content` field may be empty for complex prompts
- `reasoning_content` contains both analysis and final output