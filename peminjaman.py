from flask import (Flask, render_template, request,
                   redirect, url_for, Blueprint)

from database import getMysqlConnection
import urllib.request
import json
peminjaman = Blueprint('peminjaman', __name__)


@peminjaman.route('/peminjaman')
def show_peminjaman():
    url = f"http://127.0.0.1:8000/perpustakaan/api/show_peminjaman/"

    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    return render_template('peminjaman.html', data=dict['results'])


@peminjaman.route('/tambah_peminjaman/', methods=['GET', 'POST'])
def tambah_peminjaman():
    db = getMysqlConnection()

    try:
        sqlstr = "SELECT * from buku"
        cur = db.cursor()
        cur.execute(sqlstr)
        buku = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)

    try:
        sqlstr = "SELECT * from petugas"
        cur = db.cursor()
        cur.execute(sqlstr)
        petugas = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)

    try:
        sqlstr = "SELECT * from anggota"
        cur = db.cursor()
        cur.execute(sqlstr)
        anggota = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)

    if request.method == 'POST':
        tgl_pinjam = request.form['tanggal_pinjam']
        tgl_kembali = request.form['tanggal_kembali']
        id_buku = request.form['id_buku']
        id_anggota = request.form['id_anggota']
        id_petugas = request.form['id_petugas']

        try:
            cur = db.cursor()
            sqlstr = f"INSERT INTO peminjaman (tanggal_pinjam, tanggal_kembali, id_buku, id_anggota, id_petugas) VALUES('{tgl_pinjam}', '{tgl_kembali}', {id_buku}, {id_anggota}, {id_petugas})"
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            print('sukses')
            #output_json = cur.fetchall()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('peminjaman.show_peminjaman'))
    return render_template('form_peminjaman.html', buku=buku, anggota=anggota, petugas=petugas)


@peminjaman.route('/update_peminjaman/<int:id_peminjaman>/', methods=['GET', 'POST'])
def update_peminjaman(id_peminjaman):
    db = getMysqlConnection()
    try:
        sqlstr = f"SELECT * from peminjaman where id_peminjaman={id_peminjaman}"
        cur = db.cursor()
        cur.execute(sqlstr)
        old_data = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    try:
        sqlstr = "SELECT * from buku"
        cur = db.cursor()
        cur.execute(sqlstr)
        buku = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)

    try:
        sqlstr = "SELECT * from petugas"
        cur = db.cursor()
        cur.execute(sqlstr)
        petugas = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)

    try:
        sqlstr = "SELECT * from anggota"
        cur = db.cursor()
        cur.execute(sqlstr)
        anggota = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)

    if request.method == 'POST':
        tgl_pinjam = request.form['tanggal_pinjam']
        tgl_kembali = request.form['tanggal_kembali']
        id_buku = request.form['id_buku']
        id_anggota = request.form['id_anggota']
        id_petugas = request.form['id_petugas']

        if len(tgl_pinjam) == 0:
            tgl_pinjam = old_data[0][1]
        if len(tgl_kembali) == 0:
            tgl_kembali = old_data[0][2]
        if len(id_buku) == 0:
            id_buku = old_data[0][3]
        if len(id_anggota) == 0:
            id_anggota = old_data[0][4]
        if len(id_petugas) == 0:
            id_petugas = old_data[0][5]

        try:
            cur = db.cursor()
            sqlstr = f"update peminjaman set tanggal_pinjam = '{tgl_pinjam}', tanggal_kembali='{tgl_kembali}', id_buku={id_buku}, id_anggota={id_anggota}, id_petugas={id_petugas} where id_peminjaman={id_peminjaman}"
            cur.execute(sqlstr)
            db.commit()
            print('sukses')
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('peminjaman.show_peminjaman'))
    return render_template('update_form_peminjaman.html', data=old_data, buku=buku, anggota=anggota, petugas=petugas)


@peminjaman.route('/delete_peminjaman/<int:id_peminjaman>', methods=['GET', 'POST'])
def delete_peminjaman(id_peminjaman):
    db = getMysqlConnection()
    try:
        cur = db.cursor()
        sqlstr = f"delete from peminjaman where id_peminjaman={id_peminjaman}"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        print('sukses')
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return redirect(url_for('peminjaman.show_peminjaman'))
