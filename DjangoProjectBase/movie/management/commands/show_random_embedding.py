import random
import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Show the embedding of a random movie"

    def handle(self, *args, **kwargs):
        movies = list(Movie.objects.all())
        movie = random.choice(movies)
        embedding_vector = np.frombuffer(movie.emb, dtype=np.float32)

        self.stdout.write(f"🎬 Película: {movie.title}")
        self.stdout.write(f"📐 Longitud del embedding: {len(embedding_vector)}")
        self.stdout.write(f"🔢 Primeros 10 valores: {embedding_vector[:10]}")