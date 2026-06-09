# Known Issues

## Fixes Applied
- ✅ Session cookie size issue FIXED with Flask-Session
- Sessions now stored on filesystem (no 4KB limit)

## Limitations
- LLMs do NOT perfectly enforce target word counts (best effort via system message)
- Actual word count will often differ from target

## Connectivity
- Requires LMStudio at configured IP
- May timeout on slow systems (10-minute timeout)
- Network issues show as connection errors

## Model Behavior
- Models generate based on context and priority
- Response length influenced but not strictly controlled