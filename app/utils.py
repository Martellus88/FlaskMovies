import os
from flask_login import current_user
from flask import abort
from functools import wraps
import requests
import json


def admin_required(foo):
    @wraps(foo)
    def decorated(*args, **kwargs):
        if current_user.is_anonymous or current_user.email != os.environ.get('FLASK_MOVIE_ADMIN'):
            abort(403)
        return foo(*args, **kwargs)

    return decorated


def get_response(url_request):
    get_api = {
        'www.kinopoisk.ru': kinopoisk_api,
        'www.imdb.com': imdb_api,
    }

    id_ = url_request.replace('/', ' ').split()[-1]
    source = url_request.replace('/', ' ').split()[1]

    return get_api[source](id_)


def imdb_api(cinema_id):
    url = "https://mdblist.p.rapidapi.com/"

    querystring = {"i": f"{cinema_id}"}

    headers = {
        "X-RapidAPI-Host": "mdblist.p.rapidapi.com",
        "X-RapidAPI-Key": "45dd416a91mshccbc6a4542d7713p129dc4jsn3793d620983f"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        print(e)

    json_response = json.loads(response.text)

    title = json_response['title']
    year = json_response['year']
    type = json_response['type'] if json_response['type'] == 'movie' else 'series'
    description = json_response['description']
    runtime = json_response['runtime']
    poster = json_response['poster']

    return title, year, type, description, runtime, poster


def kinopoisk_api(cinema_id):
    url = f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{cinema_id}"

    headers = {
        "X-API-KEY": "9b021ac4-0f7b-4c61-9f20-bc63a5415416",
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers)

    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        print(e)

    json_response = json.loads(response.text)

    title = json_response['nameRu']
    year = json_response['year']
    type = 'movie' if json_response['type'] == 'FILM' else 'series'
    description = json_response['description']
    runtime = json_response['filmLength']
    poster = json_response['posterUrl']

    return title, year, type, description, runtime, poster
