import requests
import os
from dotenv import load_dotenv
load_dotenv() 


API_KEY = os.getenv('api_key')

def fetch_poster(movie_name):
    url = f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}'
    response = requests.get(url)
    data = response.json()

    if data['results']:
        poster_path = data['results'][0]['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500" + poster_path
        return full_path
    else:
        return "https://via.placeholder.com/300x450?text=No+Image"
