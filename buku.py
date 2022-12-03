from flask import (render_template, request,
                   redirect, url_for, Blueprint)
from database import getMysqlConnection
import urllib.request
import json
buku = Blueprint('buku', __name__)


@buku.route('/buku')
def show_buku():
    url = f"http://127.0.0.1:8000/perpustakaan/api/show_buku/"

    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)

    print(dict)
    return render_template('buku.html', data=dict['results'])


@buku.route('/tambah_buku/', methods=['GET', 'POST'])
def tambah_buku():
    db = getMysqlConnection()

    try:
        sqlstr = "SELECT * from genre"
        cur = db.cursor()
        cur.execute(sqlstr)
        genre = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)

    if request.method == 'POST':
        kd_buku = request.form['kd_buku']
        judul = request.form['judul_buku']
        penulis = request.form['penulis_buku']
        penerbit = request.form['penerbit_buku']
        tahun_terbit = request.form['tahun_penerbit']
        genre = request.form.getlist('genre')
        stok = request.form['stok']

        try:
            cur = db.cursor()
            sqlstr = f"INSERT INTO buku (kode_buku, judul_buku, penulis_buku, penerbit_buku, tahun_penerbit, stok) VALUES({kd_buku}, '{judul}', '{penulis}', '{penerbit}', '{tahun_terbit}', {stok})"
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            print('sukses')
            # output_json = cur.fetchall()
        except Exception as e:
            print("Error in SQL:\n", e)

        for i in genre:
            try:
                cur = db.cursor()
                sqlstr = f"INSERT INTO relasi_buku_genre (kode_buku, id_genre) VALUES({kd_buku}, {i})"
                cur.execute(sqlstr)
                db.commit()
                cur.close()
                print('sukses')
            # output_json = cur.fetchall()
            except Exception as e:
                print("Error in SQL:\n", e)

        db.close()
        return redirect(url_for('buku.show_buku'))
    return render_template('form_buku.html', genre=genre)


@buku.route('/update_buku/<int:kode_buku>/', methods=['GET', 'POST'])
def update_buku(kode_buku):
    url = f"http://127.0.0.1:8000/perpustakaan/api/update_buku/{kode_buku}/"

    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)

    buku = dict['results']

    if request.method == 'POST':
        kd_buku = request.form['kd_buku']
        judul = request.form['judul_buku']
        penulis = request.form['penulis_buku']
        penerbit = request.form['penerbit_buku']
        tahun_terbit = request.form['tahun_penerbit']
        stok = request.form['stok']
        genre = request.form.getlist('genre')

        # if len(kd_buku) == 0:
        #     kd_buku = old_data[0][1]
        # if len(judul) == 0:
        #     judul = old_data[0][2]
        # if len(penulis) == 0:
        #     penulis = old_data[0][3]
        # if len(penerbit) == 0:
        #     penerbit = old_data[0][4]
        # if len(tahun_terbit) == 0:
        #     tahun_terbit = old_data[0][5]
        # if len(stok) == 0:
        #     stok = old_data[0][6]
        # if len(genre) == 0:
        #     genre = joined_genre_relation

        # try:
        #     cur = db.cursor()
        #     sqlstr = f"update buku set kode_buku = {kd_buku}, judul_buku='{judul}', penulis_buku='{penulis}', penerbit_buku='{penerbit}', tahun_penerbit='{tahun_terbit}', stok='{stok}' where kode_buku={kode_buku}"
        #     cur.execute(sqlstr)
        #     db.commit()
        #     print('sukses')
        #     cur.close()
        # except Exception as e:
        #     print("Error in SQL:\n", e)

        # try:
        #     cur = db.cursor()
        #     sqlstr = f"delete from relasi_buku_genre where kode_buku = {kode_buku}"
        #     cur.execute(sqlstr)
        #     db.commit()
        #     print('sukses')
        #     cur.close()
        # except Exception as e:
        #     print("Error in SQL:\n", e)
        # for i in genre:
        #     try:
        #         cur = db.cursor()
        #         sqlstr = f"INSERT INTO relasi_buku_genre (kode_buku, id_genre) VALUES({kode_buku}, {i})"
        #         cur.execute(sqlstr)
        #         db.commit()
        #         print('sukses')
        #         cur.close()
        #     except Exception as e:
        #         print("Error in SQL:\n", e)

        # db.close()
        # return redirect(url_for('buku.show_buku'))
    return render_template('update_form_buku.html', data=buku, genres=genres, genre_relations=joined_genre_relation)


@buku.route('/delete_buku/<int:kode_buku>', methods=['GET', 'POST'])
def delete_buku(kode_buku):
    db = getMysqlConnection()
    try:
        cur = db.cursor()
        sqlstr = f"delete from buku where kode_buku={kode_buku}"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        print('sukses')
    except Exception as e:
        print("Error in SQL:\n", e)
    try:
        cur = db.cursor()
        sqlstr = f"delete from relasi_buku_genre where kode_buku={kode_buku}"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        print('sukses')
    except Exception as e:
        print("Error in SQL:\n", e)
    db.close()
    return redirect(url_for('buku.show_buku'))
