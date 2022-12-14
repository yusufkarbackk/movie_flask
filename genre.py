from flask import (render_template, request,
                   redirect, url_for, Blueprint)

from database import getMysqlConnection
import urllib.request
import json
import requests
from url import BASE_URL
genre = Blueprint('genre', __name__)

@genre.route('/genre')
def show_genre():
    url = f"https://{BASE_URL}-139-192-155-189.ap.ngrok.io/perpustakaan/api/genre/"

    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)

    return render_template('genre.html', data=dict['results'])


@genre.route('/tambah_genre/', methods=['GET', 'POST'])
def tambah_genre():
    if request.method == 'POST':
        nama_genre = request.form['genre']
        data = request.form.to_dict()
        url = f"http://127.0.0.1:8000/perpustakaan/api/genre/"
        requests.post(url, json=data)
        print(dict)
        print(request.form.to_dict())
        
        return redirect(url_for('genre.show_genre'))
    return render_template('form_genre.html')


@genre.route('/update_genre/<int:id_genre>/', methods=['GET', 'POST'])
def update_genre(id_genre):
    db = getMysqlConnection()

    try:
        sqlstr = f"SELECT * from genre where id_genre={id_genre}"
        cur = db.cursor()
        cur.execute(sqlstr)
        old_data = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)

    if request.method == 'POST':
        nama_genre = request.form['genre']

        if len(nama_genre) == 0:
            nama_genre = old_data[0][1]

        try:
            cur = db.cursor()
            sqlstr = f"update genre set genre = '{nama_genre}' where id_genre={id_genre}"
            cur.execute(sqlstr)
            db.commit()
            print('sukses')
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('genre.show_genre'))
    return render_template('update_form_genre.html', data=old_data)


@genre.route('/delete_genre/<int:id_genre>', methods=['GET', 'POST'])
def delete_genre(id_genre):
    db = getMysqlConnection()
    try:
        cur = db.cursor()
        sqlstr = f"delete from genre where id_genre={id_genre}"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        print('sukses')
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return redirect(url_for('genre.show_genre'))
