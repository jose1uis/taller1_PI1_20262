from django.core.management.base import BaseCommand
from movie.models import Movie
import os
import json


class Command(BaseCommand):
    help = 'Load movies from movie_descriptions.json into the Movie model'

    def handle(self, *args, **kwargs):

        # Construir la ruta completa al archivo JSON
        # Recuerda que la consola está ubicada en la carpeta raíz del proyecto
        json_file_path = 'movie/management/commands/movies.json'

        # Cargar datos desde el archivo JSON
        with open(json_file_path, 'r', encoding='utf-8') as file:
            movies = json.load(file)

        # Agregar productos a la base de datos
        for i in range(len(movies)):
            movie = movies[i]

            # Verifica que la película no exista ya en la base de datos
            exist = Movie.objects.filter(title=movie['title']).first()

            if not exist:
                Movie.objects.create(
                    title=movie['title'],
                    image='movie/images/default.jpg',
                    genre=movie['genre'],
                    year=movie['year'],
                    description=movie['plot'],
                )

        self.stdout.write(self.style.SUCCESS('Movies loaded successfully!'))