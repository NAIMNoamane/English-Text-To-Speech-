from django.urls import path 
from . import views


urlpatterns = [
    path('get_audio/',views.get_audio,name='get_audio'),  # Changed to match template
    path('',views.get_tts_voice_names,name='tts_page'),  # Root shows the form
]