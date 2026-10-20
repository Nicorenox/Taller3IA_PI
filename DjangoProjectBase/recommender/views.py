from django.shortcuts import render


def recommend(request):
    # La recomendacion por descripcion esta desactivada:
    # anteriormente dependia de la API de OpenAI.
    return render(request, 'recommend.html', {
        'prompt': None,
        'movie': None,
        'similarity': None,
        'recommendations_disabled': True,
    })
