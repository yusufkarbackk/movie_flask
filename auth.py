from flask import Blueprint, request, render_template, redirect, render_template, url_for, flash, get_flashed_messages, session
import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash


def getMysqlConnection():
    return mysql.connector.connect(user='root', host='localhost', port=8889, password='root', database='perpustakaan')


auth = Blueprint('auth', __name__,)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    db = getMysqlConnection()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = db.cursor()
        sqlstr = f"select * from anggota where nama_anggota='{username}'"
        cur.execute(sqlstr)
        account = cur.fetchall()
        print('sukses')
        if account:
            if check_password_hash(account[0][3], password):
                flash('login sukses', category='success')
                session['logged_in'] = True
                session['id'] = account[0][0]
                session['username'] = account[0][2]
                print('berhasil login')
                return redirect(url_for('index'))
            else:
                flash('password salah', category='danger')
                return redirect(url_for('auth.login'))
        else:
            flash('email salah', category='danger')
            return redirect(url_for('auth.login'))
    else:
        return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        kode_anggota = request.form['kode_anggota']
        nama = request.form['nama']
        password = request.form['password']
        jk_anggota = request.form['jk_anggota']
        jurusan_anggota = request.form['jurusan_anggota']
        telpon = request.form['telpon']
        alamat = request.form['alamat']

        hashed_password = generate_password_hash(password, method='sha256')

        db = getMysqlConnection()
        cur = db.cursor()
        sqlstr = f"select * from anggota where nama_anggota='{nama}'"
        cur.execute(sqlstr)
        account = cur.fetchone()
        if account is not None:
            flash('user sudah ada', category='danger')
            return redirect(url_for('auth.login'))

        else:
            cur = db.cursor()
            sqlstr = f"INSERT INTO anggota (kode_anggota, nama_anggota, password, jk_anggota, jurusan_anggota, no_telepon_anggota, alamat_anggota) VALUES('{kode_anggota}', '{nama}', '{hashed_password}', '{jk_anggota}', '{jurusan_anggota}', '{telpon}', '{alamat}')"
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            db.close()

            flash('berhasil register', category='success')
            return redirect(url_for('auth.login'))
    else:
        return render_template('registration.html')


@auth.route('/logout/')
def logout():
    session.pop('username', None)
    print('berhasil logout')
    return redirect(url_for('index'))
