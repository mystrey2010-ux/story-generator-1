from flask import Flask, render_template, request, jsonify
import requests
import re
import json
import os

app = Flask(__name__)

# Load environment variables from .env file
env_file = '.env'
if os.path.exists(env_file):
    with open(env_file, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#') and '=' in line:
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

# Load configuration from config.json
with open('config.json', 'r') as f:
    config = json.load(f)

# Override LMStudio host/port from environment variables if available
if os.getenv('LMSTUDIO_HOST'):
    config['lmstudio']['host'] = os.getenv('LMSTUDIO_HOST')
if os.getenv('LMSTUDIO_PORT'):
    config['lmstudio']['port'] = os.getenv('LMSTUDIO_PORT')
if os.getenv('LMSTUDIO_API_VERSION'):
    config['lmstudio']['api_version'] = os.getenv('LMSTUDIO_API_VERSION')

# Configuration for AI models
GEMMA_MODEL = config['default_model']

def get_available_models():
    """
    Fetch available models from LMStudio API
    Returns a list of model objects or empty list if error
    """
    try:
        # Get LMStudio base URL from config
        host = config['lmstudio']['host']
        port = config['lmstudio']['port']
        api_version = config['lmstudio']['api_version']
        
        # Try the native v1 REST API endpoint first
        lmstudio_url = f"http://{host}:{port}/api/{api_version}/models"
        
        response = requests.get(lmstudio_url, timeout=10)
        
        if response.status_code == 200:
            models_data = response.json()
            # Return the models list from the response
            return models_data.get('models', [])
        else:
            print(f"Error fetching models from native API: {response.status_code}")
            
        # If native API fails, try OpenAI-compatible endpoint
        lmstudio_url = f"http://{host}:{port}/v1/models"
        
        response = requests.get(lmstudio_url, timeout=10)
        
        if response.status_code == 200:
            models_data = response.json()
            # For OpenAI-compatible API, models are in the 'data' field
            return models_data.get('data', [])
        else:
            print(f"Error fetching models from OpenAI-compatible API: {response.status_code}")
            
    except Exception as e:
        print(f"Exception while fetching models: {str(e)}")
        
    # Return empty list if all attempts fail
    return []

def refine_prompt(original_prompt, word_count, model_name=None):
    """
    Review the original prompt and provide expert novelist suggestions for improvement.
    Returns the original prompt with suggestions, not an enhanced prompt.
    """
    # Get LMStudio base URL from config
    host = config['lmstudio']['host']
    port = config['lmstudio']['port']
    
    # Base URL for LMStudio API at specific IP address
    lmstudio_url = f"http://{host}:{port}/v1/chat/completions"
    
    # Create a prompt that asks AI to review and suggest improvements (not to enhance the prompt itself)
    refinement_prompt = f"""You are a renowned expert novelist. Review this story prompt and provide ONLY a bullet list of improvements:

"{original_prompt}"

Provide exactly 4-6 bullet points with specific suggestions. Do NOT write explanations or thinking. Just list what would make this prompt better:

- [Suggestion 1 for improving the prompt]
- [Suggestion 2 for adding detail]
- [Suggestion 3 for character/setting/conflict]
- [Suggestion 4 for tone/engagement]
- [Suggestion 5 - optional]
- [Suggestion 6 - optional]
"""
    
    try:
        # Use the specified model for refinement if provided, otherwise use default gemma model
        model_to_use = model_name if model_name else GEMMA_MODEL
        
        response = requests.post(
            lmstudio_url,
            json={
                "model": model_to_use,
                "messages": [
                    {"role": "user", "content": refinement_prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 300,  # More tokens for detailed feedback
            },
            timeout=config['application']['timeout']  # Use configured timeout (5 minutes)
        )
        
        if response.status_code == 200:
            result = response.json()
            # Handle different response structures
            if 'choices' in result and len(result['choices']) > 0:
                message = result['choices'][0].get('message', {})
                # Check for content first, then reasoning_content (some models use this)
                suggestions = message.get('content', '') or message.get('reasoning_content', 'No suggestions available')
                suggestions = suggestions.strip() if suggestions else 'No suggestions available'
                print(f"Refinement suggestions received: {suggestions[:100]}...")
                # Return the original prompt with the suggestions appended
                return f"{original_prompt}\n\n--- Expert Novelist Suggestions ---\n{suggestions}"
            else:
                print(f"Unexpected response structure: {result}")
                return f"{original_prompt}\n\n--- Expert Novelist Suggestions ---\nNo suggestions received from AI model. Please try again."
        else:
            print(f"Error refining prompt: {response.status_code}")
            # Return a helpful error message
            return f"{original_prompt}\n\n--- Expert Novelist Suggestions ---\nUnable to connect to AI model for feedback. Please ensure LMStudio is running at {host}:{port}."
            
    except Exception as e:
        print(f"Exception in prompt refinement: {str(e)}")
        return f"{original_prompt}\n\n--- Expert Novelist Suggestions ---\nError connecting to AI service. Showing your original prompt unchanged."

def generate_story(original_prompt, word_count, selected_model=None):
    """
    Generate a story using AI with the specified prompt and word count.
    First refines the prompt for clarity/grammar, then generates the story using the original prompt.
    Uses the selected model if provided, otherwise uses the default model.
    """
    # Get LMStudio base URL from config
    host = config['lmstudio']['host']
    port = config['lmstudio']['port']
    
    # Base URL for LMStudio API 
    lmstudio_url = f"http://{host}:{port}/v1/chat/completions"
    
    # First step: refine the prompt using the selected model or default gemma model for clarity/grammar
    refined_prompt = refine_prompt(original_prompt, word_count, selected_model)
    
    # Create the story generation prompt with the ORIGINAL prompt (not the refined one)
    # This ensures we generate a story based on what the user actually requested
    story_prompt = f"""Write ONLY the story now - no thinking, no analysis. Just the story:

{original_prompt}

Exactly {word_count} words. Begin the story immediately:"""
    
    print(f"Starting story generation with model: {selected_model or GEMMA_MODEL}")
    print(f"Prompt: {original_prompt[:50]}...")
    
    try:
        # Use the selected model for story generation if provided, otherwise use the default
        model_to_use = selected_model if selected_model else GEMMA_MODEL
        
        response = requests.post(
            lmstudio_url,
            json={
                "model": model_to_use,
                "messages": [
                    {"role": "user", "content": story_prompt}
                ],
                "temperature": 0.7,
                "max_tokens": int(word_count * 1.5),  # Estimate tokens needed
            },
            timeout=config['application']['timeout']
        )
        
        print(f"API Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            # Handle different response structures
            if 'choices' in result and len(result['choices']) > 0:
                message = result['choices'][0].get('message', {})
                # Check for content first, then reasoning_content (some models use this)
                story_text = message.get('content', '') or message.get('reasoning_content', 'No story generated')
                story_text = story_text.strip() if story_text else 'No story generated'
                print(f"Story generated successfully, length: {len(story_text)} chars")
                
                # Count actual words in the generated story
                actual_word_count = len(re.findall(r'\b\w+\b', story_text))
                
                return {
                    "story": story_text,
                    "actual_word_count": actual_word_count,
                    "model_used": model_to_use,  # Show which model was used
                    "refined_prompt": refined_prompt  # Include the refined prompt that was used for clarity
                }
            else:
                print(f"Unexpected response structure: {result}")
                return {
                    "story": "No story content received from AI model. Please try again with a different model or prompt.",
                    "actual_word_count": 0,
                    "model_used": model_to_use,
                    "refined_prompt": refined_prompt
                }
        else:
            error_msg = f"Primary model API error: {response.status_code}"
            print(error_msg)
            raise Exception(error_msg)
            
    except Exception as e:
        print(f"Error in story generation: {str(e)}")
        # Provide a helpful error message
        return {
            "story": f"Error generating story: {str(e)}. Please ensure LMStudio is running and the selected model is available.",
            "actual_word_count": 0,
            "model_used": selected_model or GEMMA_MODEL,
            "refined_prompt": refined_prompt
        }

@app.route('/models')
def get_models():
    """Serve the list of available models from LMStudio"""
    try:
        models = get_available_models()
        return jsonify({
            'models': models
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Generate a story based on prompt and word count"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        word_count = int(data.get('word_count', 100))
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        result = generate_story(prompt, word_count, data.get('model'))
        
        return jsonify({
            'story': result['story'],
            'actual_word_count': result['actual_word_count'],
            'model_used': result['model_used'],
            'refined_prompt': result['refined_prompt']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/refine', methods=['POST'])
def refine():
    """Refine a prompt for better grammar, spelling and clarity"""
    prompt = ''
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        selected_model = data.get('model')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required', 'refined_prompt': ''}), 400
        
        # Refine the prompt using the selected model or default
        refined = refine_prompt(prompt, 100, selected_model)  # word_count not used for refinement
        
        return jsonify({
            'refined_prompt': refined or prompt  # Fallback to original if refinement fails
        })
    except Exception as e:
        print(f"Error in /refine endpoint: {str(e)}")
        return jsonify({'error': str(e), 'refined_prompt': prompt}), 500

if __name__ == '__main__':
    # Ensure the application is accessible from Windows host
    app.run(debug=True, host=config['application']['host'], port=config['application']['port'], threaded=True)
