from flask import (Flask, render_template, request,
                   redirect, url_for, Blueprint)

from database import getMysqlConnection

buku = Blueprint('buku', __name__)


@buku.route('/buku')
def show_buku():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from buku"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('buku.html', data=output_json)


@buku.route('/tambah_buku/', methods=['GET', 'POST'])
def tambah_buku():
    if request.method == 'POST':
        kd_buku = request.form['kd_buku']
        judul = request.form['judul_buku']
        penulis = request.form['penulis_buku']
        penerbit = request.form['penerbit_buku']
        tahun_terbit = request.form['tahun_penerbit']
        stok = request.form['stok']

        db = getMysqlConnection()
        try:
            cur = db.cursor()
            sqlstr = f"INSERT INTO buku (kode_buku, judul_buku, penulis_buku, penerbit_buku, tahun_penerbit, stok) VALUES({kd_buku}, '{judul}', '{penulis}', '{penerbit}', '{tahun_terbit}', {stok})"
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            print('sukses')
            #output_json = cur.fetchall()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('buku.show_buku'))
    return render_template('form_buku.html')


@buku.route('/update_buku/<int:id_buku>/', methods=['GET', 'POST'])
def update_buku(id_buku):
    db = getMysqlConnection()
    try:
        sqlstr = f"SELECT * from buku where id_buku={id_buku}"
        cur = db.cursor()
        cur.execute(sqlstr)
        old_data = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    if request.method == 'POST':
        kd_buku = request.form['kd_buku']
        judul = request.form['judul_buku']
        penulis = request.form['penulis_buku']
        penerbit = request.form['penerbit_buku']
        tahun_terbit = request.form['tahun_penerbit']
        stok = request.form['stok']

        if len(kd_buku) == 0:
            kd_buku = old_data[0][1]
        if len(judul) == 0:
            judul = old_data[0][2]
        if len(penulis) == 0:
            penulis = old_data[0][3]
        if len(penerbit) == 0:
            penerbit = old_data[0][4]
        if len(tahun_terbit) == 0:
            tahun_terbit = old_data[0][5]
        if len(stok) == 0:
            stok = old_data[0][6]

        try:
            cur = db.cursor()
            sqlstr = f"update buku set kode_buku = {kd_buku}, judul_buku='{judul}', penulis_buku='{penulis}', penerbit_buku='{penerbit}', tahun_penerbit='{tahun_terbit}', stok='{stok}' where id_buku={id_buku}"
            cur.execute(sqlstr)
            db.commit()
            print('sukses')
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('buku.show_buku'))
    return render_template('update_form_buku.html', data=old_data)


@buku.route('/delete_buku/<int:id_buku>', methods=['GET', 'POST'])
def delete_buku(id_buku):
    db = getMysqlConnection()
    try:
        cur = db.cursor()
        sqlstr = f"delete from buku where id_buku={id_buku}"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        print('sukses')
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return redirect(url_for('buku.show_buku'))
