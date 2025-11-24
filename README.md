<H1 align="center">Text-To-Speech (TTS) — Django Project</H1>
<img src="/tts/images/Interface.png">
<img src="/tts/images/Interface2.png">
Le dépôt contient une petite application Django qui convertit du texte anglais en audio à l'aide de modèles Piper (fichiers `.onnx`). L'application expose une page web de démonstration et une API REST pour générer et récupérer l'audio.

**Prérequis**
- Python 3.13 (le projet utilise `Pipfile` / `pipenv`) ou un environnement virtuel équivalent
- `pipenv` (optionnel) ou `venv` + `pip`
- Sur Windows : activez PowerShell et assurez-vous que la variable d'environnement `PATH` contient l'exécutable Python

**Structure importante**
- **App Django**: `tts_api/`
- **Template de la page**: `templates/tts_api/tts_api.html`
- **Fichiers voix (modèles)**: `tts_api/voices/` (ex.: `en_GB-aru-medium.onnx` et `en_GB-aru-medium.onnx.json`)
- **Fichier de configuration Django**: `tts/tts/settings.py`

**Installation (avec pipenv — PowerShell)**

- Installer les dépendances et créer/actualiser l'environnement :

```powershell
pipenv install
```

- Si vous préférez `venv` + `pip` :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# ou installer manuellement les paquets listés dans Pipfile
```

Remarque : certains paquets (ex. `piper`, `onnxruntime`) peuvent nécessiter des roues spécifiques pour votre plateforme. En cas d'erreurs d'installation, copiez/collez l'erreur ici et je vous aiderai.

**Exécuter le serveur**

```powershell
# depuis le dossier contenant manage.py (ex: texttospeech/tts)
pipenv run python manage.py runserver
# ou si vous utilisez venv activé
python manage.py runserver
```

Ouvrez dans le navigateur : `http://127.0.0.1:8000/api/`

**Pages et endpoints**
- Page de démonstration (formulaire) : `GET /api/` — affiche le formulaire pour entrer le texte, choisir la voix et régler les paramètres audio.
- API de génération audio : `POST /api/get_audio/` — reçoit les champs form-data suivants :
  - `text` : texte à convertir (requis)
  - `voice_name` : nom de la voix (requis) — options disponibles depuis la page
  - `volume` (float) — défaut `1.0`
  - `length_scale` (float) — défaut `1.0`
  - `noise_scale` (float) — défaut `0.667`
  - `noise_w_scale` (float) — défaut `0.8`

Exemple `curl` pour générer et sauvegarder la sortie :

```powershell
curl -X POST "http://127.0.0.1:8000/api/get_audio/" -F "text=Hello world" -F "voice_name=GB-Aru" --output sample.wav
```

La page web utilise JavaScript pour poster le formulaire et lire le `Blob` retourné dans un élément `<audio>`.

**Comment ajouter / gérer des voix**
- Placez les paires de fichiers modèle dans `tts_api/voices/` :
  - le modèle ONNX : `en_US-xxx.onnx`
  - le fichier JSON de configuration associé : `en_US-xxx.onnx.json`
- Ajoutez la clé correspondante dans `tts_api/core_api.py` dans la constante `VOICE_PATHS` si vous voulez exposer un nouveau label sur la page.

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

**Contact / suite**
- Si vous voulez que je génère automatiquement un modèle de voix, télécharge et place l'onnx + .json dans `tts_api/voices/` et je peux :
  - ajouter l'entrée dans `VOICE_PATHS`
  - fournir un exemple curl/JS personnalisé

---
Fichier principal du projet : `manage.py`
Template d'exemple : `templates/tts_api/tts_api.html`
Voices folder : `tts_api/voices/` 

Si vous voulez, j'ajoute aussi un petit script de test (exécutable séparément) qui appelle `core_api.text_to_speech()` hors du serveur pour vérifier la synthèse localement. Voulez-vous que je l'ajoute ?
