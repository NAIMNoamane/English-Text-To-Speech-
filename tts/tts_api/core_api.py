import wave 
from piper import PiperVoice, SynthesisConfig
import io 
import os
import json
from pathlib import Path

VOICE_PATHS = { 
        'GB-Aru': 'en_GB-aru-medium.onnx',
        'GB-Cori': 'en_GB-cori-high.onnx',
        'GB-Jenny': 'en_GB-jenny_dioco-medium.onnx',
        'GB-North_Male': 'en_GB-northern_english_male-medium.onnx',
        'GB-Semaine': 'en_GB-semaine-medium.onnx',
        'GB-South-Female': 'en_GB-southern_english_female-low.onnx',
        'US-Bryce': 'en_US-bryce-medium.onnx',
        'US-Norman': 'en_US-norman-medium.onnx'
    }


VOICES_DIR = Path(os.environ.get("TTS_VOICES_DIR", Path(__file__).parent / "voices")).resolve()

def get_voice_path(voice_name: str):
    model_rel = VOICE_PATHS[voice_name]
    model_path = VOICES_DIR / model_rel
    config_path = Path(str(model_path) + ".json")

    if not model_path.is_file():
        raise FileNotFoundError(f"Missing model for {voice_name}: {model_path}")
    if not config_path.is_file():
        raise FileNotFoundError(
            f"Missing config JSON for {voice_name}: {config_path}\n"
            f"Place the matching .onnx.json next to the model."
        )
    return str(model_path), str(config_path)

def set_configurations(config):
    # Handle None or missing config
    if config is None:
        config = {}
    
    return SynthesisConfig(
        volume=float(config.get('volume', 1.0)),
        length_scale=float(config.get('length_scale', 1.0)),  # Speed
        noise_scale=float(config.get('noise_scale', 0.667)),  # audio variation
        noise_w_scale=float(config.get('noise_w_scale', 0.8)),  # speaking variation
        normalize_audio=False,
    )

def _sr_from(voice):
    cfg = getattr(voice, "config", None)
    # some builds: voice.config.audio.sample_rate; others: voice.config.sample_rate
    return (getattr(getattr(cfg, "audio", None), "sample_rate", None)
            or getattr(cfg, "sample_rate", None)
            or 22050)

def _chunk_to_bytes(chunk):
    # Handles multiple Piper variants
    if isinstance(chunk, (bytes, bytearray)):
        return chunk
    if hasattr(chunk, "audio_int16_bytes"):       # common field in recent builds
        return chunk.audio_int16_bytes
    if hasattr(chunk, "audio_bytes"):             # some builds
        return chunk.audio_bytes
    a = getattr(chunk, "audio", None)             # numpy/int16 array in some builds
    if a is not None and hasattr(a, "tobytes"):
        return a.tobytes()
    raise TypeError(f"Unsupported chunk type: {type(chunk)}")




def text_to_speech(text, config, voice_name):
     # Get paths to model and config
    model_path, config_path = get_voice_path(voice_name)
    syn_cfg = set_configurations(config)

    try:
        # Load voice with model config
        voice = PiperVoice.load(model_path, config_path=config_path)
        # --- Fallback: stream PCM chunks and wrap into WAV ourselves ---
        sr = _sr_from(voice)
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(1)           # Piper voices are mono
            wf.setsampwidth(2)           # 16-bit PCM
            wf.setframerate(sr)
            for chunk in voice.synthesize(text, syn_config=syn_cfg):   # NOTE: config= (not syn_config=)
                wf.writeframes(_chunk_to_bytes(chunk))

        buf.seek(0)
        return buf

    except Exception as e:
        print(f"Error in text_to_speech: {e}")
        raise  # Re-raise the exception so views can handle it