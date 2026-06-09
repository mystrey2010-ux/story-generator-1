# Technical Decisions

## Session Storage
- **Server-side encrypted files** (not cookie storage)
- Session ID stored in httponly cookie
- Session data in `/tmp/flask_session/{sid}` encrypted with Fernet
- No 4KB cookie limit - unlimited chat history size

## Encryption
- Fernet (AES-128-CBC with HMAC) for file encryption
- Key stored separately in `/tmp/flask_session_key`
- Cryptography library for NIST-compliant security

## Session Management
- NIST 800-88 compliant secure deletion (3-pass overwrite)
- Session cleared on startup
- Encrypted persistence between requests

## UI Design
- Modern chat bubble interface
- Google Gemini/ChatGPT style
- Responsive and clean