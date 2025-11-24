from piper import PiperVoice
import io, os, json, wave

voice_paths = { 
    'GB-Aru': 'en_GB-aru-medium.onnx',
    'GB-Cori': 'en_GB-cori-high.onnx',
    'GB-Jenny': 'en_GB-jenny_dioco-medium.onnx',
    'GB-North_Male': 'en_GB-northern_english_male-medium.onnx',
    'GB-Semaine': 'en_GB-semaine-medium.onnx',
    'GB-South-Female': 'en_GB-southern_english_female-low.onnx',
    'US-Bryce': 'en_US-bryce-medium.onnx',
    'US-Norman': 'en_US-norman-medium.onnx'
}

BASE = r"C:/Users/HP/Desktop/texttospeech/tts/tts_api/voices/"

def get_voice_paths(voice_name: str):
    model_path = os.path.join(BASE, voice_paths[voice_name])
    config_path = model_path + ".json"  
    if not os.path.isfile(config_path):
        raise FileNotFoundError(
            f"Missing config JSON for {voice_name}: {config_path}\n"
            "Download the matching .onnx.json for this voice and place it next to the model."
        )
    return model_path, config_path

def text_to_speech(text, voice_name):
    model_path, config_path = get_voice_paths(voice_name)
    try:
        voice = PiperVoice.load(model_path, config_path=config_path)
        with wave.open("test.wav", "wb") as wav_file:
            return voice.synthesize_wav("Welcome to the world of speech synthesis!", wav_file)
        
    except Exception as e:
        print(f"Error in text_to_speech: {e}")
        raise

# test
text_to_speech("hello my name is eminem", "GB-Aru")
