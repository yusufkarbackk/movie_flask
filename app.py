from crypt import methods
from flask import (Flask, render_template, request,
                   redirect, url_for, session, flash, abort)
from auth import auth
import json
import urllib.request
import mysql.connector

app = Flask(__name__)
app.register_blueprint(auth)

def getMysqlConnection():
    return mysql.connector.connect(user='root', host='localhost', port=8889, password='root', database='layar_tancep')


key = '6765b9ea37def7ce46ee426d105bc4d8'


@app.route('/')
def index():
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={key}&language=en-US&page=1"

    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)

    return render_template('index.html', movies=dict['results'])


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


@app.route('/dashboard')
def dashboard():
    return render_template('finance.html')


@app.route('/users')
def users():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from users"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('users.html', data=output_json)


@app.route('/transaksi')
def transaksi():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from transaksi"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('transaksi.html', data=output_json)





@app.route('/update/<int:user_id>/', methods=['GET', 'POST'])
def update(user_id):
    db = getMysqlConnection()
    status = request.form['status']
    if request.method == 'POST':
        try:
            cur = db.cursor()
            sqlstr = f"update transaksi set status = '{status}' where id={user_id}"
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            print('sukses')
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('transaksi'))


@app.route('/update_form/<int:user_id>/')
def update_form(user_id):
    db = getMysqlConnection()
    try:
        sqlstr = f"SELECT * from transaksi where id={user_id}"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('update.html', data=output_json)


@app.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
def deleteUser(user_id):
    db = getMysqlConnection()
    try:
        cur = db.cursor()
        sqlstr = f"delete from users where id={user_id}"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        print('sukses')
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
