import os
import base64
from openai import OpenAI
from django.core.management.base import BaseCommand
from movie.models import Movie
from dotenv import load_dotenv

class Command(BaseCommand):
    help = "Generate images with OpenAI and update movie image field"

    def handle(self, *args, **kwargs):
        load_dotenv('../openAI.env')
        client = OpenAI(api_key=os.environ.get('openai_apikey'))

        images_folder = 'media/movie/images/'
        os.makedirs(images_folder, exist_ok=True)

        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies")

        for movie in movies:
            try:
                image_relative_path = self.generate_and_download_image(client, movie.title, images_folder)
                movie.image = image_relative_path
                movie.save()
                self.stdout.write(self.style.SUCCESS(f"Saved and updated image for: {movie.title}"))
            except Exception as e:
                self.stderr.write(f"Failed for {movie.title}: {e}")

            # 🚫 NO QUITES ESTE BREAK: solo se genera la imagen de la primera película
            break

        self.stdout.write(self.style.SUCCESS("Process finished (only first movie updated)."))

    def generate_and_download_image(self, client, movie_title, save_folder):
        """
        Genera una imagen con gpt-image-1 (que devuelve base64, no URL)
        y la guarda directamente en disco.
        """
        prompt = f"Movie poster of {movie_title}"

        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024",   # tamaños válidos: 1024x1024, 1024x1536, 1536x1024
            quality="low",       # low / medium / high / auto — usa "low" para ahorrar costo
            n=1,
        )

        # gpt-image-1 siempre devuelve la imagen en base64 (b64_json), nunca una URL
        image_base64 = response.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        image_filename = f"m_{movie_title}.png"
        image_path_full = os.path.join(save_folder, image_filename)

        with open(image_path_full, 'wb') as f:
            f.write(image_bytes)

        return os.path.join('movie/images', image_filename)