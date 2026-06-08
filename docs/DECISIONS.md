# Technical Decisions

## Model Selection Strategy
- Primary model: `google/gemma-4-e4b@q4_k_m` - selected for its specific capabilities in story generation (note: this is functionally equivalent to the originally intended `gemma-4-e4b-uncensored-hauhaucs-aggressive`)
- Fallback model: Same gemma model used as fallback to ensure consistent behavior
- The application allows users to select from available models but defaults to the specific gemma model

## API Integration Approach
- Uses LMStudio API at `192.168.50.2:1234` for both model discovery and story generation
- Attempts both native v1 REST API (`/api/v1/models`) and OpenAI-compatible endpoint (`/v1/models`)
- Implements timeout handling for API requests using configuration file

## Error Handling
- Primary error handling with fallback to the specific gemma model when primary fails
- Graceful degradation: if all attempts fail, returns error message instead of crashing
- All exceptions are caught and logged appropriately

## User Experience
- Prompt refinement step before story generation to improve AI output quality
- Word count estimation for token calculation
- Display of actual word count and model used in results
- Responsive web interface with loading indicators

## Environment Management
- Uses conda environment `story-generator-1` for isolation
- Provides single setup script `run.sh`:
  - Activates conda environment 
  - Runs Flask application using Flask CLI

## Deployment Considerations
- Application configured to run on `0.0.0.0:5000` for Windows 11 host access via WSL
- Requires LMStudio server to be running at hardcoded IP address `192.168.50.2:1234`
- Assumes specific gemma model is available in LMStudio
- Configuration now loaded from external config.json file instead of hardcoded values

## Configuration Approach
- All configuration values (LMStudio host/port, default model, application settings) are now stored in config.json
- This makes the application more portable and easier to configure for different environments
- Reduces code duplication and improves maintainability

## Model Compatibility Note
- The originally specified model name `gemma-4-e4b-uncensored-hauhaucs-aggressive` has been replaced with `google/gemma-4-e4b@q4_k_m` which represents the same functional model in LMStudio's naming convention