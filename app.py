from flask import Flask, render_template, request, jsonify, session
import requests
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuration
LMSTUDIO_HOST = os.getenv('LMSTUDIO_HOST', '192.168.50.2')
LMSTUDIO_PORT = os.getenv('LMSTUDIO_PORT', '1234')
MODEL_NAME = 'dirty-muse-writer-v01-uncensored-erotica-nsfw-i1'

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
    return [MODEL_NAME]

@app.route('/')
def index():
    models = get_available_models()
    chat_history = session.get('chat_history', [])
    return render_template('index.html', models=models, chat_history=chat_history)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        model = data.get('model', MODEL_NAME)
        word_count = data.get('word_count', '')
        clear_history = data.get('clear_history', False)
        
        if clear_history:
            session['chat_history'] = []
            session.modified = True
        
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400
        
        # Get chat history
        chat_history = session.get('chat_history', [])
        
        # Build messages from history
        messages = []
        
        # Always add system message for word count if provided (per prompt basis)
        if word_count:
            system_msg = f"IMPORTANT: Aim for approximately {word_count} words total. This is a PRIMARY GOAL for your response length."
            messages.append({"role": "system", "content": system_msg})
        
        # Add conversation history
        for msg in chat_history:
            messages.append({"role": "user", "content": msg['prompt']})
            if msg.get('response'):
                messages.append({"role": "assistant", "content": msg['response']})
        
        # Add current prompt
        messages.append({"role": "user", "content": prompt})
        
        # Send to LMStudio
        url = f"http://{LMSTUDIO_HOST}:{LMSTUDIO_PORT}/v1/chat/completions"
        
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
            
            combined_text = content or reasoning_content or ''
            actual_word_count = len(combined_text.split()) if combined_text else 0
            
            # Store in history
            chat_entry = {
                'prompt': prompt,
                'response': content,
                'actual_word_count': actual_word_count
            }
            chat_history.append(chat_entry)
            session['chat_history'] = chat_history
            session.modified = True
            
            return jsonify({
                'original_prompt': prompt,
                'analysis': reasoning_content if reasoning_content else 'No analysis/thinking section',
                'final_output': content if content else 'No final output received',
                'actual_word_count': actual_word_count,
                'chat_history': chat_history
            })
        else:
            return jsonify({'error': f'API error: {response.status_code}'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/models')
def models():
    """Endpoint to get available models"""
    return jsonify({'models': get_available_models()})

@app.route('/clear', methods=['POST'])
def clear():
    """Clear chat history"""
    session['chat_history'] = []
    session.modified = True
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)