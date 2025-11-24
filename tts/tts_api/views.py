from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from . import core_api
from django.http import FileResponse


@api_view(['POST'])
def get_audio(request):
    # Validate required fields
    text = request.POST.get('text')
    if not text:
        return Response({'error': 'Text is required'}, status=400)
        
    voice_name = request.POST.get('voice_name')
    if not voice_name:
        return Response({'error': 'Voice name is required'}, status=400)

    # Build config from form fields with defaults
    config = {
        'volume': float(request.POST.get('volume', 1.0)),
        'length_scale': float(request.POST.get('length_scale', 1.0)),
        'noise_scale': float(request.POST.get('noise_scale', 0.667)),
        'noise_w_scale': float(request.POST.get('noise_w_scale', 0.8))
    }

    try: 
        audio = core_api.text_to_speech(text, config, voice_name)
        
        return FileResponse(
            audio,
            as_attachment=False,
            filename='generated_audio.wav',
            content_type='audio/wav'
        )
    except Exception as e:
        import traceback
        print(f"Error generating audio: {str(e)}")
        print(traceback.format_exc())
        return Response({'error': str(e)}, status=500)


def get_tts_voice_names(request):
    voices = list(core_api.VOICE_PATHS.keys())
    return render(request, 'tts_api/voice-settings-form.html', {'voices': voices})