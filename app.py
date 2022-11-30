from flask import (Flask, render_template, request,
                   redirect, url_for, jsonify)
from database import getMysqlConnection
from auth import auth
from petugas import petugas
from buku import buku
from rak import rak
from genre import genre
from peminjaman import peminjaman
from pengembalian import pengembalian
import json
import urllib.request

app = Flask(__name__)

app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.register_blueprint(auth)
app.register_blueprint(rak)
app.register_blueprint(petugas)
app.register_blueprint(buku)
app.register_blueprint(peminjaman)
app.register_blueprint(pengembalian)
app.register_blueprint(genre)

app.secret_key = 'totalsecret123'


key = '6765b9ea37def7ce46ee426d105bc4d8'


@app.route('/person/')
def hello():
    return jsonify({
        'name': 'yusuf',
        'address': 'Tangsel'
    })


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form['search_movie']
        return redirect(url_for('search_movie', keyword=f"{keyword}"))
    else:
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={key}&language=en-US&page=1"

        response = urllib.request.urlopen(url)
        data = response.read()
        dict = json.loads(data)

        return render_template('index.html', movies=dict['results'])


@app.route('/search_movie/<keyword>')
def search_movie(keyword):
    url = f'https://api.themoviedb.org/3/search/movie?api_key={key}&language=en-US&query={keyword}&page=1&include_adult=false'
    response = urllib.request.urlopen(url)
    data = response.read()
    movies = json.loads(data)

    return render_template('search_result.html', movies=movies['results'])


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
        sqlstr = "SELECT * from anggota"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('users.html', data=output_json)


@app.route('/update_user/<int:user_id>/', methods=['GET', 'POST'])
def update_user(user_id):
    db = getMysqlConnection()
    try:
        sqlstr = f"SELECT * from anggota where id_anggota={user_id}"
        cur = db.cursor()
        cur.execute(sqlstr)
        old_data = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    if request.method == 'POST':
        kode_anggota = request.form['kode_anggota']
        nama = request.form['nama']
        jk_anggota = request.form['jk_anggota']
        jurusan_anggota = request.form['jurusan_anggota']
        telpon = request.form['telpon']
        alamat = request.form['alamat']

        if len(kode_anggota) == 0:
            kode_anggota = old_data[0][1]
        if len(nama) == 0:
            nama = old_data[0][2]
        if len(jk_anggota) == 0:
            jk_anggota = old_data[0][3]
        if len(jurusan_anggota) == 0:
            jurusan_anggota = old_data[0][4]
        if len(telpon) == 0:
            telpon = old_data[0][5]
        if len(alamat) == 0:
            alamat = old_data[0][6]

        try:
            cur = db.cursor()
            sqlstr = f"update anggota set kode_anggota = '{kode_anggota}', nama_anggota='{nama}', jk_anggota='{jk_anggota}', jurusan_anggota='{jurusan_anggota}', no_telepon_anggota='{telpon}', alamat_anggota='{alamat}' where id_anggota={user_id}"
            cur.execute(sqlstr)
            db.commit()
            print('sukses')
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('users'))


@app.route('/user_form/<int:user_id>')
def user_update_form(user_id):
    db = getMysqlConnection()
    try:
        sqlstr = f"SELECT * from anggota where id_anggota={user_id}"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('user_update_form.html', data=output_json)


@app.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
def deleteUser(user_id):
    db = getMysqlConnection()
    try:
        cur = db.cursor()
        sqlstr = f"delete from anggota where id_anggota={user_id}"
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
