from flask import Flask, render_template, request, jsonify, session
import requests
import os
import secrets
import string
import json
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer

load_dotenv()

def get_encryption_key():
    key_file = '/tmp/flask_session_key'
    if os.path.exists(key_file):
        with open(key_file, 'rb') as f:
            return f.read()
    os.makedirs(os.path.dirname(key_file), exist_ok=True)
    key = Fernet.generate_key()
    with open(key_file, 'wb') as f:
        f.write(key)
    return key

ENCRYPTION_KEY = get_encryption_key()
fernet = Fernet(ENCRYPTION_KEY)
serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production'))

def secure_delete_file(filepath):
    try:
        file_size = os.path.getsize(filepath)
        for _ in range(3):
            random_data = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(file_size))
            with open(filepath, 'w') as f:
                f.write(random_data)
            os.sync()
        os.remove(filepath)
    except FileNotFoundError:
        pass
    except Exception:
        try:
            os.remove(filepath)
        except:
            pass

def load_encrypted_session():
    session_id = session.get('_id', '')
    if session_id:
        session_file = f"/tmp/flask_session/{session_id}"
        if os.path.exists(session_file):
            try:
                with open(session_file, 'rb') as f:
                    encrypted_data = f.read()
                decrypted_data = fernet.decrypt(encrypted_data)
                session_data = json.loads(decrypted_data.decode())
                for k, v in session_data.items():
                    if k != '_id':
                        session[k] = v
            except Exception:
                pass

def save_encrypted_session():
    if 'chat_history' in session:
        session_id = session.get('_id') or secrets.token_hex(16)
        session['_id'] = session_id
        session_file = f"/tmp/flask_session/{session_id}"
        os.makedirs(os.path.dirname(session_file), exist_ok=True)
        data_to_encrypt = {k: v for k, v in dict(session).items() if k != '_id'}
        encrypted_data = fernet.encrypt(json.dumps(data_to_encrypt).encode())
        with open(session_file, 'wb') as f:
            f.write(encrypted_data)

def clear_session_files_on_startup():
    session_dir = '/tmp/flask_session'
    if os.path.exists(session_dir):
        for filename in os.listdir(session_dir):
            if not filename.endswith('_key'):
                filepath = os.path.join(session_dir, filename)
                secure_delete_file(filepath)

clear_session_files_on_startup()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

LMSTUDIO_HOST = os.getenv('LMSTUDIO_HOST', '192.168.50.2')
LMSTUDIO_PORT = os.getenv('LMSTUDIO_PORT', '1234')
MODEL_NAME = 'dirty-muse-writer-v01-uncensored-erotica-nsfw-i1'

def get_available_models():
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
    load_encrypted_session()
    models = get_available_models()
    chat_history = session.get('chat_history', [])
    return render_template('index.html', models=models, chat_history=chat_history)

@app.route('/chat', methods=['POST'])
def chat():
    load_encrypted_session()
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        model = data.get('model', MODEL_NAME)
        word_count = data.get('word_count', '')
        
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400

        chat_history = session.get('chat_history', [])
        messages = []

        if word_count:
            system_msg = f"IMPORTANT: Aim for approximately {word_count} words total. This is a PRIMARY GOAL for your response length."
            messages.append({"role": "system", "content": system_msg})

        for msg in chat_history:
            messages.append({"role": "user", "content": msg['prompt']})
            if msg.get('response'):
                messages.append({"role": "assistant", "content": msg['response']})

        messages.append({"role": "user", "content": prompt})

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

            chat_entry = {
                'prompt': prompt,
                'response': content,
                'actual_word_count': actual_word_count
            }
            chat_history.append(chat_entry)
            session['chat_history'] = chat_history
            save_encrypted_session()

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
    return jsonify({'models': get_available_models()})

@app.route('/clear', methods=['POST'])
def clear():
    session_id = session.get('_id', '')
    if session_id:
        filepath = f"/tmp/flask_session/{session_id}"
        if os.path.exists(filepath):
            secure_delete_file(filepath)

    session.clear()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)