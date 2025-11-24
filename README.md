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
  <img src="/tts/images/Interface.png" width="120%" />
  
</p>
<p align="center">
  <img src="/tts/images/Interface2.png" width="120%" /></p>
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
  - `volume` (float) — default `1.0`
  - `length_scale` (float) — default `1.0`
  - `noise_scale` (float) — default `0.667`
  - `noise_w_scale` (float) — default `0.8`

### How to add / manage voices

- Place the model file pairs in `tts_api/voices/`:
  - ONNX model: `en_US-xxx.onnx`
  - Associated JSON configuration file: `en_US-xxx.onnx.json`
- Add the corresponding key in `tts_api/core_api.py` in the `VOICE_PATHS` constant if you want to expose a new label on the page.

**Points importants du code**
- `tts_api/core_api.py` :
  - `get_voice_path(voice_name)` construit les chemins vers le `.onnx` et le `.onnx.json` et vérifie leur existence.
  - `text_to_speech(...)` charge la configuration JSON et utilise `PiperVoice` pour synthétiser le WAV, retourné comme `BytesIO` prêt pour `FileResponse`.
- `tts_api/views.py` :
  - `get_audio` valide les champs, construit le dictionnaire `config` et renvoie le `FileResponse` avec `content_type='audio/wav'`.
  - `get_tts_voice_names` rend le template et passe la liste des voix disponibles.

**Dépannage**
- Erreur `TemplateDoesNotExist`: assurez-vous que `TEMPLATES.DIRS` dans `tts/tts/settings.py` contient `BASE_DIR / "templates"` (déjà configuré).
- Erreur `FileNotFoundError: Voice model not found`: vérifiez que les fichiers `.onnx` et `.onnx.json` existent dans `tts_api/voices/` et que `VOICE_PATHS` référence le bon nom.
- Erreur `KeyError: 'num_symbols'` ou équivalente : cela vient de l'appel à Piper sans fournir la config JSON du modèle ; le code du projet charge maintenant le `.json` et le passe à `PiperVoice`.
- Problèmes d'installation (compilation de paquets natifs) : préférez `piper`/`onnxruntime` précompilés pour Windows ou utilisez une version de Python compatible avec les roues disponibles.

**Sécurité & production**
- Ce projet est prévu pour développement local (DEBUG=True). Ne pas mettre en production sans :
  - désactiver `DEBUG`, configurer `ALLOWED_HOSTS`
  - sécuriser l'accès aux modèles et aux ressources
  - gérer la mise en file/limitation des requêtes (pour éviter surcharge mémoire CPU/GPU lors de la synthèse)

---
Fichier principal du projet : `manage.py`
Template d'exemple : `templates/tts_api/tts_api.html`
Voices folder : `tts_api/voices/` 

