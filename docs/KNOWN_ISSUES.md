# Known Issues

## Connectivity
- Requires LMStudio running at configured IP address (default: 192.168.50.2)
- May timeout on slow systems (5 minute timeout configured)

## Model Behavior
- Model uses extensive reasoning/thinking mode
- `content` field may be empty for complex prompts
- `reasoning_content` contains both analysis and final output

## Token Usage
- max_tokens set to 262144 (full context)
- May result in very long response times
- Ensure adequate timeout configured