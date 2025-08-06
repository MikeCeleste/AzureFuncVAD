# SileroVAD/__init__.py

import logging
import io
import json
import torch
import torchaudio
import azure.functions as func
from urllib.request import urlopen

# Load model once on cold start
MODEL, utils = torch.hub.load(
    repo_or_dir='snakers4/silero-vad',
    model='silero_vad',
    force_reload=False
)
get_speech_timestamps, *_ = utils

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("SileroVAD: received URL-based VAD request")
    try:
        data = req.get_json()
        url = data.get("url")
        if not url:
            return func.HttpResponse("JSON must include a 'url' field", status_code=400)

        # Download the audio
        resp = urlopen(url)
        audio_bytes = resp.read()

        # Load via torchaudio
        waveform, sample_rate = torchaudio.load(io.BytesIO(audio_bytes))
        if sample_rate != 16000:
            waveform = torchaudio.transforms.Resample(
                orig_freq=sample_rate, new_freq=16000
            )(waveform)
        waveform = waveform.mean(dim=0)

        # Run VAD
        speech_ts = get_speech_timestamps(
            waveform, MODEL, sampling_rate=16000
        )
        has_voice = len(speech_ts) > 0

        return func.HttpResponse(
            body=json.dumps({
                "speech_timestamps": speech_ts,
                "has_voice": has_voice
            }),
            status_code=200,
            mimetype="application/json"
        )

    except json.JSONDecodeError:
        return func.HttpResponse("Invalid JSON", status_code=400)
    except Exception as e:
        logging.exception("SileroVAD failed")
        return func.HttpResponse(f"Internal error: {e}", status_code=500)

