from flask import Blueprint, request, render_template, redirect, render_template, url_for, flash, get_flashed_messages
import mysql.connector


def getMysqlConnection():
    return mysql.connector.connect(user='root', host='localhost', port=8889, password='root', database='perpustakaan')


auth = Blueprint('auth', __name__,)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        kode_anggota = request.form['kode_anggota']
        nama = request.form['nama']
        jk_anggota = request.form['jk_anggota']
        jurusan_anggota = request.form['jurusan_anggota']
        telpon = request.form['telpon']
        alamat = request.form['alamat']

        db = getMysqlConnection()
        try:
            cur = db.cursor()
            sqlstr = f"INSERT INTO anggota (kode_anggota, nama_anggota, jk_anggota, jurusan_anggota, no_telepon_anggota, alamat_anggota) VALUES('{kode_anggota}', '{nama}', '{jk_anggota}', '{jurusan_anggota}', '{telpon}', '{alamat}')"
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            print('sukses')
            #output_json = cur.fetchall()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('index'))
    else:
        return render_template('registration.html')
