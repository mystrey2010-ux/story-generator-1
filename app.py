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
    refinement_prompt = f"""You are a renowned expert novelist. Review the following story prompt and provide constructive suggestions that would help make the generated story better:

Original prompt: "{original_prompt}"

Analyze this prompt and provide:
1. Strengths of the prompt
2. Areas for improvement
3. Specific suggestions for making it more engaging and detailed
4. Questions to consider for better story development

Format your feedback as helpful guidance that the user could optionally incorporate, but DO NOT rewrite or enhance the prompt itself. Keep your feedback concise and actionable.

Return your expert review and suggestions:"""
    
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
            timeout=config['application']['timeout']
        )
        
        if response.status_code == 200:
            result = response.json()
            suggestions = result['choices'][0]['message']['content'].strip()
            # Return the original prompt with the suggestions appended
            return f"{original_prompt}\n\n--- Expert Novelist Suggestions ---\n{suggestions}"
        else:
            print(f"Error refining prompt: {response.status_code}")
            return original_prompt
            
    except Exception as e:
        print(f"Exception in prompt refinement: {str(e)}")
        return original_prompt

def generate_story(original_prompt, word_count, selected_model=None):
    """
    Generate a story using AI with the specified prompt and word count.
    First refines the prompt for clarity/grammar, then generates the story using the original prompt.
    Uses the selected model if provided, otherwise uses the specific gemma model.
    """
    # Get LMStudio base URL from config
    host = config['lmstudio']['host']
    port = config['lmstudio']['port']
    
    # Base URL for LMStudio API at specific IP address
    lmstudio_url = f"http://{host}:{port}/v1/chat/completions"
    
    # First step: refine the prompt using the selected model or default gemma model for clarity/grammar
    refined_prompt = refine_prompt(original_prompt, word_count, selected_model)
    
    # Create the story generation prompt with the ORIGINAL prompt (not the refined one)
    # This ensures we generate a story based on what the user actually requested
    story_prompt = f"""Generate a creative story about '{original_prompt}' with exactly {word_count} words. Make it engaging and well-structured.
    
    Important: 
    - The story must be as close to exactly {word_count} words as possible
    - Do not exceed {word_count + 20} words (allowing for some flexibility)
    - Format the story with clear paragraphs
    - Ensure proper grammar, spelling, and punctuation throughout
    """
    
    try:
        # Use the selected model for story generation if provided, otherwise use the specific gemma model
        model_to_use = selected_model if selected_model else GEMMA_MODEL
        
        # Use the specific gemma model for story generation
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
        
        if response.status_code == 200:
            result = response.json()
            story_text = result['choices'][0]['message']['content'].strip()
            
            # Count actual words in the generated story
            actual_word_count = len(re.findall(r'\b\w+\b', story_text))
            
            return {
                "story": story_text,
                "actual_word_count": actual_word_count,
                "model_used": model_to_use,  # Show which model was used
                "refined_prompt": refined_prompt  # Include the refined prompt that was used for clarity
            }
        else:
            raise Exception(f"Primary model API error: {response.status_code}")
            
    except Exception as e:
        # If there's an error, still use the gemma model for fallback
        try:
            print(f"Error in story generation, trying fallback. Error: {str(e)}")
            response = requests.post(
                lmstudio_url,
                json={
                    "model": GEMMA_MODEL,  # Use the specific gemma model throughout
                    "messages": [
                        {"role": "user", "content": story_prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": int(word_count * 1.5),  # Estimate tokens needed
                },
                timeout=config['application']['timeout']
            )
            
            if response.status_code == 200:
                result = response.json()
                story_text = result['choices'][0]['message']['content'].strip()
                
                # Count actual words in the generated story
                actual_word_count = len(re.findall(r'\b\w+\b', story_text))
                
                return {
                    "story": story_text,
                    "actual_word_count": actual_word_count,
                    "model_used": GEMMA_MODEL,  # Show that we tried the specific gemma model
                    "refined_prompt": refined_prompt  # Include the refined prompt that was used for clarity
                }
            else:
                raise Exception(f"Fallback model API error: {response.status_code}")
                
        except Exception as fallback_error:
            error_msg = f"Error generating story with both models: {str(fallback_error)}"
            print(error_msg)
            return {
                "story": error_msg,
                "actual_word_count": 0,
                "model_used": GEMMA_MODEL,  # Show that we tried the specific gemma model
                "refined_prompt": refined_prompt  # Include the refined prompt that was used for clarity
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
