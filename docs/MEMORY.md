# Project Memory

## Key Insights
- QWEN3.5 model returns responses in `reasoning_content` field
- `content` field may be empty for complex prompts
- Both fields displayed as-is without processing
- No max_tokens ensures model uses full default context
- Word count calculated as: `len(combined_text.split())`

## Configuration Notes
- Token limit uses model default
- Response times working well
- 5-minute timeout appropriate for this model
- Model dropdown successfully fetching from LMStudio API

## Features Implemented
- ✅ Dynamic model selection
- ✅ Target word count (AI instruction)
- ✅ Actual word count (programmatic calculation)
- ✅ Clean section separation in UI
- ✅ Robust error handling