<H1 align="center">Text-To-Speech (TTS) — Django Project</H1>
<p align="center"> 
  <b>Text To Speech Application For Educational Purposes and Pedagogy matters</b></p>
<p align="center">
<p align="center">
  
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Django-5.1-092E20?logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/DRF-3.15-EF4444?logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/Piper%20TTS-0.0.2-0EA5E9" />
</p>

---
<p align="center">
  <img src="/tts/images/Interface.png" width="100%" />
  
</p>
<p align="center">
  <img src="/tts/images/Interface2.png" width="100%" /></p>
<h2><b>Project Overview</b></h2>
The repository contains a small Django application that converts English text into audio using Piper models (.onnx files). The application exposes a demo web page and a REST API to generate and retrieve the audio.

<h2><b>Project Structure</b></h2>

<img width="223" height="280" alt="image" src="https://github.com/user-attachments/assets/3713a930-582c-4d6e-8334-3d7fe5f951be" />
 
- <B>App Django</B>: tts_api/
- <b>Template de la page</b>: templates/tts_api/tts_api.html
- <b>Fichiers voix (modèles)</b>: tts_api/voices/ (ex.: "en_GB-aru-medium.onnx" et "en_GB-aru-medium.onnx.json")
- <b>Fichier de configuration Django</b>: "tts/tts/settings.py"


<h2><b>Requirements</b></h2>

- First we need audio piper models, you can find it <a href="https://huggingface.co/rhasspy/piper-voices">here</a>.
- Second run these commands in powershell


```powershell 
pipenv shell
pipenv install -r requirements.txt
```

<h2><b>Run Project</b></h2>

```powershell
# From the directory containing manage.py (ex: texttospeech/tts)
pipenv run python manage.py runserver
```

Open the browser on : `http://127.0.0.1:8000/api/`

**Endpoint 'API'**
- **Demo page (form)**: `GET /api/` — displays the form to enter text, choose the voice and adjust audio parameters.
- **Audio generation API**: `POST /api/get_audio/` — expects the following `form-data` fields:
  - `text`: text to convert (**required**)
  - `voice_name`: voice name (**required**) — options available from the page
  - `volume` Controls loudness of the generated audio.
  - `length_scale` Controls speaking speed / duration
  - `noise_scale` Controls how “expressive” / variable the voice is.
  - `noise_w_scale` focus on timing / prosody randomness.

**How to add / manage voices**

- Place the model file pairs in `tts_api/voices/`:
  - ONNX model: `en_US-xxx.onnx`
  - Associated JSON configuration file: `en_US-xxx.onnx.json`
- Add the corresponding key in `tts_api/core_api.py` in the `VOICE_PATHS` constant if you want to expose a new label on the page.

**Troubleshooting**

- **`TemplateDoesNotExist` error**: Make sure that `TEMPLATES.DIRS` in `tts/tts/settings.py` contains `BASE_DIR / "templates"` (already configured).
- **`FileNotFoundError: Voice model not found` error**: Check that the `.onnx` and `.onnx.json` files exist in `tts_api/voices/` and that `VOICE_PATHS` references the correct name.
- **`KeyError: 'num_symbols'` or similar error**: This comes from calling Piper without providing the model’s JSON config; the project code now loads the `.json` file and passes it to `PiperVoice`.
- **Installation issues (native package compilation)**: Prefer precompiled `piper` / `onnxruntime` wheels for Windows, or use a Python version compatible with the available wheels.

**Security & production**

- This project is intended for local development (`DEBUG=True`). Do not deploy it to production without:
  - disabling `DEBUG` and configuring `ALLOWED_HOSTS`
  - securing access to models and resources
  - handling request queuing / rate limiting (to avoid CPU/GPU memory overload during synthesis)


---
This project can be only used in educational purposes. Enjoy it. 

