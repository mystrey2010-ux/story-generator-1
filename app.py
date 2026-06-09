from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Configuration
LMSTUDIO_HOST = os.getenv('LMSTUDIO_HOST', '192.168.50.2')
LMSTUDIO_PORT = os.getenv('LMSTUDIO_PORT', '1234')

def get_available_models():
    """Fetch available models from LMStudio"""
    try:
        url = f"http://{LMSTUDIO_HOST}:{LMSTUDIO_PORT}/v1/models"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            models = response.json()
            return [m['id'] for m in models.get('data', [])]
    except Exception:
        pass
    return ['dirty-muse-writer-v01-uncensored-erotica-nsfw-i1']

@app.route('/')
def index():
    models = get_available_models()
    return render_template('index.html', models=models)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        model = data.get('model', 'dirty-muse-writer-v01-uncensored-erotica-nsfw-i1')
        word_count = data.get('word_count', '')
        
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400
        
        # Append word count instruction if provided - make it a primary goal
        if word_count:
            prompt = f"{prompt}\n\nIMPORTANT: Aim for approximately {word_count} words total. This is a primary goal for your response length."
        
        # Send to LMStudio (no max_tokens - use model default)
        url = f"http://{LMSTUDIO_HOST}:{LMSTUDIO_PORT}/v1/chat/completions"
        
        messages = [{"role": "user", "content": prompt}]
        
        # Add system message to emphasize word count goal
        if word_count:
            system_msg = f"PRIMARY GOAL: Generate a response of approximately {word_count} words. This is a critical length requirement that should be your main priority when generating content."
            messages.insert(0, {"role": "system", "content": system_msg})
        
        response = requests.post(
            url,
            json={
                "model": model,
                "messages": messages,
                "temperature": 0.7
            },
            timeout=600
        )
        
        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']
            
            content = message.get('content', '').strip()
            reasoning_content = message.get('reasoning_content', '').strip()
            
            # Calculate actual word count from combined response
            combined_text = content or reasoning_content or ''
            actual_word_count = len(combined_text.split()) if combined_text else 0
            
            return jsonify({
                'original_prompt': prompt,
                'analysis': reasoning_content if reasoning_content else 'No analysis/thinking section',
                'final_output': content if content else 'No final output received',
                'actual_word_count': actual_word_count
            })
        else:
            return jsonify({'error': f'API error: {response.status_code}'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/models')
def models():
    """Endpoint to get available models"""
    return jsonify({'models': get_available_models()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)