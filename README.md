
# AzureFuncVAD

## Overview
AzureFuncVAD is an Azure Function App that performs Voice Activity Detection (VAD) on audio files. It accepts a POST request containing an audio file URL or raw audio payload, downloads or processes the audio, runs the Silero VAD model, and returns a JSON response indicating whether speech was detected.

## Endpoints

### HTTP Trigger
```
POST https://<YOUR_FUNCTION_APP>.azurewebsites.net/api/SileroVAD?code=<FUNCTION_KEY>
```

- **Content-Type:** 
  - `application/json` when sending a URL payload.
  - `audio/wav` when sending raw WAV binary.
- **JSON Body (URL mode):**
  ```json
  {
    "url": "https://example.com/path/to/audio.wav"
  }
  ```
- **Response (JSON):**
  ```json
  {
    "has_speech": true,
    "speech_segments": [
      [start_time_seconds, end_time_seconds],
      ...
    ]
  }
  ```

## Local Development

1. **Install Azure Functions Core Tools**
   ```bash
   brew tap azure/functions
   brew install azure-functions-core-tools@4
   ```
2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run locally**
   ```bash
   func start
   ```
4. **Test**
   ```bash
   curl -X POST -H "Content-Type: application/json"      -d '{"url":"https://example.com/audio.wav"}'      http://localhost:7071/api/SileroVAD
   ```

## Deployment

1. **Log in to Azure**
   ```bash
   az login
   az account set --subscription "<YOUR_SUBSCRIPTION>"
   ```
2. **Deploy ZIP package**
   ```bash
   func pack
   az functionapp deployment source config-zip      --resource-group <RESOURCE_GROUP>      --name <FUNCTION_APP_NAME>      --src function.zip
   ```

## Git / GitHub Setup

1. **Remove any mistaken origin**
   ```bash
   git remote remove origin  # if it exists
   ```
2. **Add GitHub origin**
   ```bash
   git remote add origin https://github.com/mikeceleste/AzureFuncVAD.git
   ```
3. **Push and track master**
   ```bash
   git push -u origin master
   ```

## License
MIT
