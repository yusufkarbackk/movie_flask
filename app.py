from flask import (Flask, render_template, request,
                   redirect, url_for, session, flash, abort)
import json
import urllib.request


app = Flask(__name__)

key = '6765b9ea37def7ce46ee426d105bc4d8'


@app.route('/')
def index():
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={key}&language=en-US&page=1'
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)

    return render_template('home.html', movies=dict['results'])


@app.route('/search_movie/')
def search_movie():
    keyword = request.args.get('search')
    url = f'https://api.themoviedb.org/3/search/movie?api_key={key}&language=en-US&query={keyword}&page=1&include_adult=false'
    response = urllib.request.urlopen(url)
    data = response.read()
    movies = json.loads(data)

    return render_template('movie_search.html', movies=movies['results'])


@app.route('/movie_detail/<int:movieId>')
def movie_detail(movieId):
    url = f'https://api.themoviedb.org/3/movie/{movieId}?api_key=6765b9ea37def7ce46ee426d105bc4d8&language=en-US'

    response = urllib.request.urlopen(url)
    data = response.read()
    movie = json.loads(data)

    return render_template('detail.html', movie=movie)


if __name__ == '__main__':
    app.run(debug=True)
