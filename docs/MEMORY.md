# Project Memory

## Key Insights
- ✅ QWEN3.5 model returns responses in `reasoning_content` field
- ✅ `content` field may be empty for complex prompts
- ✅ Both fields displayed as-is without processing
- ✅ No max_tokens ensures model uses full default context

## Configuration Notes
- ✅ Token limit now uses model default
- ✅ Response times working well
- ✅ 5-minute timeout appropriate for this model
- ✅ Model dropdown successfully fetching from LMStudio API

## Working Features
- Dynamic model selection from LMStudio
- Target word count targeting functionality
- Clean section separation in UI
- Robust error handling