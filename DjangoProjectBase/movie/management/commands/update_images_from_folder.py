import os
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Assign images from media/movie/images/ folder to each movie based on filename"

    def handle(self, *args, **kwargs):
        images_folder = os.path.join('media', 'movie', 'images')
        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies")

        updated_count = 0
        for movie in movies:
            expected_filename = f"m_{movie.title}.png"
            expected_path_full = os.path.join(images_folder, expected_filename)

            if os.path.exists(expected_path_full):
                movie.image = os.path.join('movie/images', expected_filename)
                movie.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"Image assigned: {movie.title}"))
            else:
                self.stderr.write(f"Image not found for: {movie.title} (expected {expected_filename})")

        self.stdout.write(self.style.SUCCESS(f"Finished. {updated_count}/{movies.count()} movies updated."))