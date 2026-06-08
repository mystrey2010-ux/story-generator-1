# Changelog

## [0.1.0] - Initial Release

### Added
- Flask web application for story generation
- HTML interface with prompt input and word count selector
- Model selection dropdown populated from LMStudio API
- Story generation using LMStudio API
- Fallback mechanism using specific gemma model
- Conda environment setup scripts
- Multiple execution methods (direct script, Flask CLI)
- Windows 11 WSL connectivity support

### Changed
- None

### Removed
- None

## [0.1.1] - Documentation Update

### Added
- ARCHITECTURE.md documentation
- DECISIONS.md documentation  
- PROJECT_STATE.md documentation
- KNOWN_ISSUES.md documentation

### Changed
- Updated README with complete documentation structure
- Improved error handling and logging in app.py
- Configured application to use external config.json file instead of hardcoded values
- Reduced shell scripts to only run.sh

### Removed
- Conda setup and direct execution scripts (conda_setup.sh, final_run_story_generator.sh, setup_and_run.sh)