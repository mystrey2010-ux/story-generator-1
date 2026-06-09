# Known Issues

## Limitations
- LLMs do NOT perfectly enforce target word counts (best effort via system message)
- Actual word count will often differ from target (though improved with priority)
- Very large chat histories may impact performance

## Connectivity
- Requires LMStudio at configured IP
- May timeout on slow systems (10-minute timeout)
- Network issues show as connection errors

## Model Behavior
- Models generate based on context and priority
- Response length influenced but not strictly controlled
- System message adds word count as priority