# Project Memory

## Key Insights
- QWEN3.5 model returns responses in `reasoning_content` field
- `content` field may be empty for complex prompts
- Both fields displayed as-is without processing
- 262144 max_tokens ensures sufficient output space

## Configuration Notes
- Token limit matches model's context length
- Response times may vary significantly
- 5-minute timeout appropriate for this model