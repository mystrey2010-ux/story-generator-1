# Project Memory

## Session Architecture
- Cookie stores only session ID (sid) - 64 hex chars
- Session files in `/tmp/flask_session/{sid}` are encrypted
- Encryption key in `/tmp/flask_session_key`
- No Flask-Session dependency needed

## Implementation Notes
- Custom encrypted session implementation
- Fernet library for AES-128 encryption
- Secrets module for secure random generation
- Secure overwrite before file deletion