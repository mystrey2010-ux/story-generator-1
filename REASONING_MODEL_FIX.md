# Enhanced Story Extraction for Reasoning Models

## Special Handling for qwen3.5-4b-nsfw-ara-heretic-literotica-i1

### Problem Identified:
This model operates in **reasoning mode by default**, putting analysis and thinking processes in the `reasoning_content` field instead of generating actual story content in the `content` field.

### Solution Implemented:
- **Enhanced filtering logic** to extract story content from reasoning processes
- Looks for **narrative indicators** like:
  - "Leo", "The boy", character names
  - Story starters: "Suddenly", "As he", "Once upon", "In the", "It was"
  - Narrative structures indicating story text
- **Separates story from analysis** even when both are in reasoning_content
- **Clean output** without thinking/analysis sections

### Result:
Even when the model returns thinking processes, the application now extracts and displays the actual story content to the user.

**Repository updated**: git@github.com:mystrey2010-ux/story-generator-1.git