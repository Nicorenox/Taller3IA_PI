import os
import numpy as np
from django.shortcuts import render
from openai import OpenAI
from movie.models import Movie
from dotenv import load_dotenv

from openai import OpenAI
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv('../openAI.env')

# Inicializa el cliente de OpenAI con la API Key
client = OpenAI(api_key=os.environ.get('openai_apikey'))
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def recommend(request):
    best_movie = None
    max_similarity = None
    prompt = None
    
    if request.method == 'GET' and request.GET.get('prompt'):
        prompt = request.GET.get('prompt')

        response = client.embeddings.create(
            input=[prompt],
            model="text-embedding-3-small"
        )
        prompt_emb = np.array(response.data[0].embedding, dtype=np.float32)

        best_similarity = -1
        for movie in Movie.objects.all():
            movie_emb = np.frombuffer(movie.emb, dtype=np.float32)
            similarity = cosine_similarity(prompt_emb, movie_emb)
            if similarity > best_similarity:
                best_similarity = similarity
                best_movie = movie

        max_similarity = best_similarity

    return render(request, 'recommend.html', {
        'prompt': prompt,
        'movie': best_movie,
        'similarity': max_similarity,
    })
    
