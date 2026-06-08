# Known Issues

## Connectivity Issues
- **LMStudio IP Address Hardcoding**: The application uses a hardcoded IP address `192.168.50.2:1234` for LMStudio API. This may not be accessible from all environments or WSL configurations.
  - *Workaround*: Ensure LMStudio is running and accessible at this IP address, or modify the config.json file to use the correct address.

## Model Availability
- **Model Dependency**: The application depends on a specific gemma model being available in LMStudio (`google/gemma-4-e4b@q4_k_m`).
  - *Workaround*: Verify that the required model is loaded in LMStudio before running the application.

## Fallback Behavior
- **Inconsistent Fallback Model**: The fallback mechanism uses the same gemma model as primary, which may not provide proper fallback behavior if the model itself has issues.
  - *Workaround*: Consider implementing a truly different fallback model or better error handling.

## Environment Setup
- **Conda Environment Issues**: Some users may experience issues with conda environment activation or package installation.
  - *Workaround*: Ensure conda is properly installed and the story-generator-1 environment exists. The run.sh script handles activation.

## Windows 11 Connectivity
- **WSL Firewall**: Users may need to configure Windows firewall rules to allow connections from Windows 11 host to WSL.
  - *Workaround*: Run the provided PowerShell command to add firewall rule:
    ```powershell
    netsh advfirewall firewall add rule name="WSL Flask" dir=in action=allow protocol=TCP localport=5000
    ```

## Performance
- **Slow API Response**: If LMStudio server is slow or unresponsive, the story generation will be delayed.
  - *Workaround*: Monitor LMStudio server performance or adjust timeout values in config.json.

## UI Limitations
- **No Model Refresh**: The model dropdown is populated only once when the page loads and does not refresh automatically.
  - *Workaround*: Reload the page to refresh available models.

## Configuration Note
- **External Configuration**: The application now uses an external config.json file for configuration instead of hardcoded values, which improves portability but requires users to ensure this file exists.