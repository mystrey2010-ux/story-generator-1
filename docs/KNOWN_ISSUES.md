# Known Issues

## Connectivity Issues
- **LMStudio IP Address Configuration**: The application requires LMStudio server to be accessible. Update the configuration file with the correct address for your environment.

## Model Availability
- **Model Dependency**: The application depends on a default model being available in LMStudio. Verify that the configured model is loaded before running the application.

## Fallback Behavior
- **Limited Fallback Model**: The fallback mechanism uses the same model as primary, which may not provide proper fallback behavior if the model has issues. Consider implementing a different fallback model or better error handling.

## Environment Setup
- **Conda Environment Issues**: Some users may experience issues with conda environment activation or package installation. Ensure the environment exists or use the fallback setup script.

## Windows 11 Connectivity
- **WSL Firewall**: Users may need to configure Windows firewall rules to allow connections from Windows 11 host to WSL.
  - *Workaround*: Run the provided PowerShell command to add firewall rule:
    ```powershell
    netsh advfirewall firewall add rule name="WSL Flask" dir=in action=allow protocol=TCP localport=5000
    ```

## Performance
- **Slow API Response**: If LMStudio server is slow or unresponsive, the story generation will be delayed. Adjust timeout values in configuration if needed.

## UI Limitations
- **No Model Refresh**: The model dropdown is populated only once when the page loads and does not refresh automatically. Reload the page to refresh available models.

## Configuration Note
- **External Configuration**: The application uses an external configuration file for configuration instead of hardcoded values, which improves portability.