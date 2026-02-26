from django.shortcuts import render
from django.http import HttpResponse
import matplotlib
import matplotlib.pyplot as plt
import io
import base64

from .models import Movie
# Create your views here.

def home(request):
    searchTerm = request.GET.get('searchMovie')

    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()

    return render(request, 'home.html', {
        'searchTerm': searchTerm,
        'movies': movies
    })

def statistics_view(request):
    matplotlib.use('Agg')

    # ==========================
    #  GRAFICA POR AÑO
    # ==========================
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {}

    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"

        movie_counts_by_year[year] = movies_in_year.count()

    # ==========================
    #  GRAFICA POR GENERO
    # ==========================
    movies = Movie.objects.all()
    movie_counts_by_genre = {}

    for movie in movies:
        if movie.genre:
            first_genre = movie.genre.split(",")[0].strip()
        else:
            first_genre = "Unknown"

        if first_genre in movie_counts_by_genre:
            movie_counts_by_genre[first_genre] += 1
        else:
            movie_counts_by_genre[first_genre] = 1

    # ==========================
    # CREAR FIGURA CON 2 GRAFICAS
    # ==========================
    plt.figure(figsize=(12, 5))

    # --- Subplot 1: Año ---
    plt.subplot(1, 2, 1)
    years_labels = [str(year) for year in movie_counts_by_year.keys()]
    plt.bar(years_labels, movie_counts_by_year.values())
    plt.title('Movies per Year')
    plt.xticks(rotation=90)

    # --- Subplot 2: Género ---
    plt.subplot(1, 2, 2)
    genre_labels = [str(g) for g in movie_counts_by_genre.keys()] # para que no haya problema enter int y string
    plt.bar(genre_labels, movie_counts_by_genre.values())
    plt.title('Movies per Genre')
    plt.xticks(rotation=90)

    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'statistics.html', {'graphic': graphic})


def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

def about(request):
    return render(request, 'about.html')

def signup_view(request):
    return render(request, 'signup.html')