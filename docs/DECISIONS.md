# Technical Decisions

## Model Selection Strategy
- Primary model: Default configured model in config.json - selected for its specific capabilities in story generation
- Fallback model: Same model used as fallback to ensure consistent behavior
- The application allows users to select from available models but defaults to the configured default model

## API Integration Approach
- Uses LMStudio API for both model discovery and story generation
- Attempts both native v1 REST API (`/api/v1/models`) and OpenAI-compatible endpoint (`/v1/models`)
- Implements timeout handling for API requests using configuration file

## Error Handling
- Primary error handling with fallback to the default model when primary fails
- Graceful degradation: if all attempts fail, returns error message instead of crashing
- All exceptions are caught and logged appropriately

## User Experience
- Prompt refinement step before story generation to improve AI output quality
- Word count estimation for token calculation
- Display of actual word count and model used in results
- Responsive web interface with loading indicators

## Environment Management
- Uses conda environment for isolation
- Provides single setup script `run.sh`:
  - Activates conda environment 
  - Runs Flask application using Flask CLI

## Deployment Considerations
- Application configured to run on host for external access
- Requires LMStudio server to be running
- Assumes the default model is available in LMStudio
- Configuration now loaded from external config.json file instead of hardcoded values

## Configuration Approach
- All configuration values (LMStudio host/port, default model, application settings) are now stored in config.json
- This makes the application more portable and easier to configure for different environments
- Reduces code duplication and improves maintainability