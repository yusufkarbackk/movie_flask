from flask import (Flask, render_template, request,
                   redirect, url_for, Blueprint)

from database import getMysqlConnection
import urllib.request
import json
rak = Blueprint('rak', __name__)


@rak.route('/rak')
def show_rak():
    url = f"http://127.0.0.1:8000/perpustakaan/api/show_rak/"

    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    return render_template('rak.html', data=dict['results'])


@rak.route('/tambah_rak/', methods=['GET', 'POST'])
def tambah_rak():
    db = getMysqlConnection()

    try:
        sqlstr = "SELECT * from buku"
        cur = db.cursor()
        cur.execute(sqlstr)
        buku = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)

    if request.method == 'POST':
        nama_rak = request.form['nama_rak']
        lokasi = request.form['lokasi_rak']
        id_buku = request.form['id_buku']

        try:
            cur = db.cursor()
            sqlstr = f"INSERT INTO rak (nama_rak, lokasi_rak, id_buku) VALUES('{nama_rak}', '{lokasi}', {id_buku})"
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            print('sukses')
            #output_json = cur.fetchall()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('rak.show_rak'))
    return render_template('form_rak.html', buku=buku)


@rak.route('/update_rak/<int:id_rak>/', methods=['GET', 'POST'])
def update_rak(id_rak):
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from buku"
        cur = db.cursor()
        cur.execute(sqlstr)
        buku = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)

    try:
        sqlstr = f"SELECT * from rak where id_rak={id_rak}"
        cur = db.cursor()
        cur.execute(sqlstr)
        old_data = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)

    if request.method == 'POST':
        nama_rak = request.form['nama_rak']
        lokasi = request.form['lokasi_rak']
        id_buku = request.form['id_buku']

        if len(nama_rak) == 0:
            nama_rak = old_data[0][1]
        if len(lokasi) == 0:
            lokasi = old_data[0][2]
        if len(id_buku) == 0:
            id_buku = old_data[0][3]

        try:
            cur = db.cursor()
            sqlstr = f"update rak set nama_rak = '{nama_rak}', lokasi_rak='{lokasi}', id_buku='{id_buku}' where id_rak={id_rak}"
            cur.execute(sqlstr)
            db.commit()
            print('sukses')
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('rak.show_rak'))
    return render_template('update_form_rak.html', data=old_data, buku=buku)


@rak.route('/delete_rak/<int:id_rak>', methods=['GET', 'POST'])
def delete_rak(id_rak):
    db = getMysqlConnection()
    try:
        cur = db.cursor()
        sqlstr = f"delete from rak where id_rak={id_rak}"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        print('sukses')
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return redirect(url_for('rak.show_rak'))
