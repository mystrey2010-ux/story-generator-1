# Changelog

## [1.5.0] - Encrypted Filesystem Sessions

### Added
- Encrypted server-side session storage (Fernet/AES-128)
- Session ID cookie (no size limit)
- NIST 800-88 compliant secure file deletion
- Session files cleared on startup

### Changed
- Removed Flask-Session dependency (custom implementation)
- Chat history now stored encrypted in `/tmp/flask_session/`
- Cookie only stores 64-char sid (not session data)

## [1.4.0] - Modern Webchat UI Redesign
- Chat bubble design
- Auto-expanding textarea
- Animated loading indicator
- Fixed loading message visibility

## [1.3.0] - Chat History & NEW Chat
- Session-based chat history
- NEW Chat button
- System message per prompt for word count

## [1.2.0] - Actual Word Count
- Programmatic word count calculation

## [1.1.0] - Enhanced Configuration
- Model dropdown selection
- Target word count input
- Timeout increased to 600s

## [1.0.0] - Initial Release